from schwifty.core import es, es_index
from schwifty.util import result_entity


def more_like_this(entity):
    query = {
        'query': {
            'more_like_this': {
                'fields': ['name', '$text', '$latin'],
                'docs': [
                    {'_id': entity['_id'], '_type': entity['_type']}
                ],
            },
        },
        '_source': {
            'excludes': ['$text', '$latin', '*.*']
        }
    }
    results = es.search(index=es_index, body=query)
    similar = {'status': 'ok', 'results': []}
    for result in results.get('hits', {}).get('hits', []):
        similar['results'].append(result_entity(result))
    return similar
