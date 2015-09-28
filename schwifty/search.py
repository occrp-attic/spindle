from copy import deepcopy
from pprint import pprint  # noqa
from collections import defaultdict

from flask import url_for
from werkzeug.datastructures import MultiDict

from schwifty.core import es, es_index

QUERY_FIELDS = ['raw.*']
DEFAULT_FIELDS = ['source', 'id', 'schema', 'entity.*']

# Scoped facets are facets where the returned facet values are returned such
# that any filter against the same field will not be applied in the sub-query
# used to generate the facet values.
OR_FIELDS = ['schema', 'source']


def query(args):
    """ Parse a user query string, compose and execute a query. """
    if not isinstance(args, MultiDict):
        args = MultiDict(args)
    q = text_query(args.get('q', ''))

    # Extract filters, given in the form: &filter:foo_field=bla_value
    filters = []
    for key in args.keys():
        for value in args.getlist(key):
            if not key.startswith('filter:'):
                continue
            _, field = key.split(':', 1)
            filters.append((field, value))

    # Generate aggregations. They are a generalized mechanism to do facetting
    # in ElasticSearch. Anything placed inside the "scoped" sub-aggregation
    # is made to be ``global``, ie. it'll have to bring it's own filters.
    facets = args.getlist('facet')
    aggs = {
        'scoped': {
            'global': {},
            'aggs': {}
        }
    }
    for facet in facets:
        agg = {facet: {'terms': {'field': facet, 'size': 200}}}
        if facet in OR_FIELDS:
            aggs['scoped']['aggs'][facet] = {
                'filter': {
                    'query': filter_query(q, filters, skip=facet)
                },
                'aggs': agg
            }
        else:
            aggs.update(agg)

    q = {
        'query': filter_query(q, filters),
        'aggregations': aggs,
        '_source': DEFAULT_FIELDS
    }
    q = paginate(q, args.get('limit'), args.get('offset'))
    return execute_query(q, facets)


def filter_query(q, filters, skip=None):
    """ Apply a list of filters to the given query. """
    or_filters = defaultdict(list)
    for field, value in filters:
        if field == skip:
            continue
        if field in OR_FIELDS:
            or_filters[field].append(value)
        else:
            q = add_filter(q, {'term': {field: value}})
    for field, value in or_filters.items():
        q = add_filter(q, {'terms': {field: value}})
    print q
    return q


def add_filter(q, filter_):
    """ Add the filter ``filter_`` to the given query. """
    q = deepcopy(q)
    if 'filtered' not in q:
        return {
            'filtered': {
                'query': q,
                'filter': filter_
            }
        }

    if 'and' in q['filtered']['filter']:
        q['filtered']['filter']['and'].append(filter_)
    else:
        q['filtered']['filter'] = \
            {'and': [filter_, q['filtered']['filter']]}
    return q


def paginate(q, limit, offset):
    """ Apply pagination to the query, based on limit and offset. """
    try:
        q['from'] = max(0, int(offset))
    except (TypeError, ValueError):
        q['from'] = 0
    try:
        q['size'] = min(10000, int(limit))
    except (TypeError, ValueError):
        q['size'] = 75

    if q['from'] > 0:
        # When requesting a second page of the results, the client will not
        # need to be returned facet results a second time.
        del q['aggregations']
    return q


def text_query(text):
    """ Construct the part of a query which is responsible for finding a
    piece of thext in the selected documents. """
    text = text.strip()
    if len(text):
        q = {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": text,
                        "fields": QUERY_FIELDS,
                        "type": "best_fields",
                        "cutoff_frequency": 0.0007,
                        "operator": "and",
                    },
                },
                "should": {
                    "multi_match": {
                        "query": text,
                        "fields": QUERY_FIELDS,
                        "type": "phrase"
                    },
                }
            }
        }
    else:
        q = {'match_all': {}}
    return q


def execute_query(q, facets):
    """ Execute the query and return a set of results. """
    result = es.search(index=es_index, body=q)
    hits = result.get('hits', {})
    output = {
        'status': 'ok',
        'results': [],
        'offset': q['from'],
        'limit': q['size'],
        'took': result.get('took'),
        'total': hits.get('total'),
        'facets': {}
    }
    for doc in hits.get('hits', []):
        data = doc.get('_source')
        # FIXME: potential layer fuckery
        data['uri'] = url_for('entity', doc_type=doc.get('_type'),
                              id=doc.get('_id'), _external=True)
        output['results'].append(data)

    # traverse and get all facets.
    aggs = result.get('aggregations')
    for facet in facets:
        scoped = aggs.get('scoped').get(facet, {})
        value = aggs.get(facet, scoped.get(facet, {}))
        data = {
            'total': scoped.get('doc_count', hits.get('total')),
            'values': value.get('buckets', [])
        }
        output['facets'][facet] = data

    return output
