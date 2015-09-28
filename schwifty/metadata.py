import requests

from schwifty.core import app, es, es_index, cache


def get_sources():
    """ Get a list of all sources stored in the index, then resolve and
    return them. """
    sources = cache.get('sources')
    if sources is None:
        doc_type = app.config.get('SOURCE_DOC_TYPE')
        res = es.search(index=es_index, doc_type=doc_type)
        sources = {}
        for hit in res.get('hits', {}).get('hits'):
            data = hit.get('_source')
            sources[data['slug']] = data
        cache.set('sources', sources)
    return sources


def get_schemas():
    """ Get a list of all JSON schemas used to describe entities in the
    index, then resolve and return them. """
    schemas = cache.get('schemas')
    if schemas is None:
        q = {
            'size': 0,
            'aggregations': {
                'schema': {'terms': {'field': 'schema'}}
            }
        }
        res = es.search(index=es_index, body=q)
        schemas = {}
        for agg in res.get('aggregations').get('schema').get('buckets'):
            url = agg.get('key')
            schemas[url] = requests.get(url).json()
        cache.set('schemas', schemas)
    return schemas


def get_countries():
    """ Return a list of all countries, indexed by ISO 2-letter code.
    Includes ``ZZ`` for global scope. """
    from pycountry import countries
    data = {
        'ZZ': {'title': 'Global'},
        'XK': {'title': 'Kosovo'},
        'GB-SCT': {'title': 'Scotland'},
        'GB-NIR': {'title': 'Northern Ireland'},
        'GB-WLS': {'title': 'Wales'},
        'CY-TRNC': {'title': 'Northern Cyprus'}
    }
    for country in countries:
        data[country.alpha2] = {
            'title': country.name
        }
    return data


def get_metadata():
    return {
        'sources': get_sources(),
        'schemas': get_schemas(),
        'countries': get_countries()
    }
