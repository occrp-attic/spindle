from flask import request
from werkzeug.exceptions import Forbidden

from loom.db import Collection, Source, session
from spindle.model import Permission

READ = 'read'
WRITE = 'write'


def admin_resources():
    for coll_id, in session.query(Collection.id):
        request.authz_collections[READ].add(coll_id)
        request.authz_collections[WRITE].add(coll_id)
    for source_id, in session.query(Source.id):
        request.authz_sources[READ].add(source_id)
        request.authz_sources[WRITE].add(source_id)


def request_resources():
    request.authz_collections = {READ: set(), WRITE: set()}
    request.authz_sources = {READ: set(), WRITE: set()}
    if request.auth_admin:
        return admin_resources()
    q = session.query(Permission)
    q = q.filter(Permission.role_id.in_(request.auth_roles))
    for perm in q:
        if perm.resource_type == Permission.COLLECTION:
            if perm.read:
                request.authz_collections[READ].add(perm.resource_id)
            if perm.write and request.logged_in:
                request.authz_collections[WRITE].add(perm.resource_id)
        if perm.resource_type == Permission.SOURCE:
            if perm.read:
                request.authz_sources[READ].add(perm.resource_id)
            if perm.write and request.logged_in:
                request.authz_sources[WRITE].add(perm.resource_id)


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


def sources(right):
    if not hasattr(request, 'authz_sources'):
        return []
    return request.authz_sources.get(right, [])


def source(right, source_id):
    """ Can the user exercise ``right`` on ``source_id``? """
    try:
        return int(source_id) in sources(right)
    except (ValueError, TypeError):
        return False


def logged_in():
    return request.logged_in


def require(pred):
    if not pred:
        raise Forbidden("Sorry, you're not permitted to do this!")
