from spindle.core import get_es, get_es_index
from spindle.search.common import authz_filter


def suggest_entity(args):
    text = args.get('text')
    options = []
    if text is not None and len(text.strip()):
        q = {
            'size': 5,
            'query': authz_filter({
                'match': {
                    '$suggest': text
                }
            }),
            '_source': ['name', 'id', '$schema']
        }
        result = get_es().search(index=get_es_index(), body=q)
        for res in result.get('hits', {}).get('hits', []):
            options.append(res.get('_source'))
    return {
        'text': text,
        'options': options
    }
