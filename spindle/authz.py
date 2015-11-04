from flask import request
from werkzeug.exceptions import Forbidden

from loom.db import session
from spindle.model import Permission

READ = 'read'
WRITE = 'write'


def request_resources():
    q = session.query(Permission)
    q = q.filter(Permission.role_id.in_(request.auth_roles))
    request.authz_collections = {READ: [], WRITE: []}
    for perm in q:
        if perm.resource_type == Permission.COLLECTION:
            if perm.read:
                request.authz_collections[READ].append(perm.resource_id)
            if perm.write:
                request.authz_collections[WRITE].append(perm.resource_id)


def collections(right):
    if not hasattr(request, 'authz_collections'):
        return []
    return request.authz_collections.get(right, [])


def collection(right, collection_id):
    """ Can the user exercise ``right`` on ``collection_id``? """
    try:
        return int(collection_id) in collections(right)
    except (ValueError, TypeError):
        return False


def logged_in():
    return request.logged_in


def require(pred):
    if not pred:
        raise Forbidden("Sorry, you're not permitted to do this!")
