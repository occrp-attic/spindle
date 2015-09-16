from flask import url_for
from werkzeug.datastructures import MultiDict

from schwifty.core import es, es_index

QUERY_FIELDS = ['raw.*']
DEFAULT_FIELDS = ['source.*', 'id', 'schema', 'entity.*']


def query(args):
    """ Parse a user query string, compose and execute a query. """
    if not isinstance(args, MultiDict):
        args = MultiDict(args)
    q = text_query(args.get('q'))
    q = {
        'query': q,
        'aggregations': {},
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
    return execute_query(q)


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


def execute_query(q):
    """ Execute the query and return a set of results. """
    result = es.search(index=es_index, body=q)
    hits = result.get('hits', {})
    output = {
        'status': 'ok',
        'results': [],
        'offset': q['from'],
        'limit': q['size'],
        'total':  hits.get('total')
    }
    for doc in hits.get('hits', []):
        data = doc.get('_source')
        data['uri'] = url_for('entity', doc_type=doc.get('_type'),
                              id=doc.get('_id'), _external=True)
        output['results'].append(data)
    return output
