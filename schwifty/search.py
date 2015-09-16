from copy import deepcopy
from pprint import pprint  # noqa

from flask import url_for
from werkzeug.datastructures import MultiDict

from schwifty.core import es, es_index

QUERY_FIELDS = ['raw.*']
DEFAULT_FIELDS = ['source.*', 'id', 'schema', 'entity.*']

# Scoped facets are facets where the returned facet values are returned such
# that any filter against the same field will not be applied in the sub-query
# used to generate the facet values.
SCOPED_FACETS = ['schema', 'source.slug']


def query(args):
    """ Parse a user query string, compose and execute a query. """
    if not isinstance(args, MultiDict):
        args = MultiDict(args)
    q = text_query(args.get('q'))

    facets = args.getlist('facet')
    print 'FACETS', facets
    # TODO: filters on jurisdiction, source, schema
    # semantics: source, schema facets are unaffected by source & schema
    #            filters

    aggs = {
        'scoped': {
            'global': {},
            'aggs': {}
        }
    }
    for facet in facets:
        agg = {facet: {'terms': {'field': facet}}}
        if facet in SCOPED_FACETS:
            aggs['scoped']['aggs'][facet] = {
                'filter': {'query': q},
                'aggs': agg
            }
        else:
            aggs.update(agg)

    # TODO: return facets for the above.
    q = {
        'query': q,
        'aggregations': aggs,
        '_source': DEFAULT_FIELDS
    }

    try:
        q['from'] = max(0, int(args.get('offset')))
    except (TypeError, ValueError):
        q['from'] = 0
    try:
        q['size'] = min(10000, int(args.get('limit')))
    except (TypeError, ValueError):
        q['size'] = 50

    if q['from'] > 0:
        # When requesting a second page of the results, the client will not
        # need to be returned facet results a second time.
        del q['aggregations']

    return execute_query(q, facets)


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
        data['uri'] = url_for('entity', doc_type=doc.get('_type'),
                              id=doc.get('_id'), _external=True)
        output['results'].append(data)

    # traverse and get all facets.
    aggs = result.get('aggregations')
    for facet in facets:
        scoped = aggs.get('scoped', {}).get(facet, {})
        value = aggs.get(facet, scoped.get(facet, {}))
        data = {
            'total': scoped.get('doc_count', hits.get('total')),
            'values': value.get('buckets', [])
        }
        output['facets'][facet] = data

    return output
