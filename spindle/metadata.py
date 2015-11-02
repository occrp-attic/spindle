from flask import current_app
from pycountry import countries

from loom.db import session, Source


def get_sources():
    """ Get a list of all sources stored in the index, then resolve and
    return them. """
    sources = {}
    for source in session.query(Source):
        sources[source.slug] = source.to_dict()
    return sources


def get_schemas():
    """ Get a list of all JSON schemas used to describe entities in the
    index, then resolve and return them. """
    return current_app.config.get('SCHEMAS', {})


def get_countries():
    """ Return a list of all countries, indexed by ISO 2-letter code.
    Includes ``ZZ`` for global scope. """
    # These are local overrides. May want to drop pycountry at some point and
    # just use our own fixture.
    data = {
        'ZZ': {'title': 'Global'},
        'XK': {'title': 'Kosovo'},
        'GB-SCT': {'title': 'Scotland (UK)'},
        'GB-NIR': {'title': 'Northern Ireland (UK)'},
        'GB-WLS': {'title': 'Wales (UK)'},
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
