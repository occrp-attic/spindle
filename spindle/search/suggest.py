from spindle.core import get_es, get_es_index
from spindle.reflect import implied_schemas
from spindle.search.common import authz_filter, add_filter


def suggest_entity(args):
    """ Auto-complete API. """
    text = args.get('text')
    options = []
    if text is not None and len(text.strip()):
        q = authz_filter({'match': {'$suggest': text}})
        schema = args.get('$schema')
        if schema is not None:
            # Find matching sub-schemas as well.
            schemas = implied_schemas(schema)
            q = add_filter(q, {"terms": {"$schema": schemas}})
        collection = args.get('collection')
        if collection is not None:
            q = {
                'function_score': {
                    'query': q,
                    'functions': [{
                        'boost_factor': 2,
                        'filter': {'term': {'$collections': collection}}
                    }]
                }
            }
        q = {
            'size': 5,
            'query': q,
            '_source': ['name', 'id', '$schema']
        }
        result = get_es().search(index=get_es_index(), body=q)
        for res in result.get('hits', {}).get('hits', []):
            options.append(res.get('_source'))
    return {
        'text': text,
        'options': options
    }
