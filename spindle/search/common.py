from copy import deepcopy

from spindle import authz


def authz_filter(q):
    return add_filter(q, {
        "or": [
            {"terms": {"$sources": list(authz.sources(authz.READ))}},
            {"terms": {"$collections": list(authz.collections(authz.READ))}}
        ]
    })


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
