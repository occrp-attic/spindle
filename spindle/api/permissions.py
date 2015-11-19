from flask import Blueprint
from werkzeug.exceptions import BadRequest
from apikit import jsonify, request_data

from loom.db import session
from spindle import authz
from spindle.validation import validate
from spindle.model import Role, Permission

permissions_schema = 'https://schema.occrp.org/operational/permission.json#'
permissions_api = Blueprint('permissions', __name__)


@permissions_api.route('/api/roles')
def list_roles():
    # Not using a pager because in most places this wouldn't make sense to
    # paginate. Need to review this later.
    q = session.query(Role)
    return jsonify({
        'total': q.count(),
        'results': q
    })


@permissions_api.route('/api/collections/<int:collection>/permissions')
@permissions_api.route('/api/sources/<int:source>/permissions')
def index(collection=None, source=None):
    q = session.query(Permission)
    if collection is not None:
        authz.require(authz.collection(authz.WRITE, collection))
        q = q.filter(Permission.resource_type == Permission.COLLECTION)
        q = q.filter(Permission.resource_id == collection)
    elif source is not None:
        authz.require(authz.source(authz.WRITE, source))
        q = q.filter(Permission.resource_type == Permission.SOURCE)
        q = q.filter(Permission.resource_id == source)
    return jsonify({
        'total': q.count(),
        'results': q
    })


@permissions_api.route('/api/collections/<int:collection>/permissions',
                       methods=['POST', 'PUT'])
@permissions_api.route('/api/sources/<int:source>/permissions',
                       methods=['POST', 'PUT'])
def create_or_update(collection=None, source=None):
    if collection is not None:
        authz.require(authz.collection(authz.WRITE, collection))
    if source is not None:
        authz.require(authz.source(authz.WRITE, source))

    resource_type = Permission.COLLECTION if collection else Permission.SOURCE
    resource_id = collection or source
    data = request_data()
    validate(data, permissions_schema)

    # check that the role exists.
    rq = session.query(Role).filter(Role.id == data['role'])
    if rq.first() is None:
        raise BadRequest()

    q = session.query(Permission)
    q = q.filter(Permission.role_id == data['role'])
    q = q.filter(Permission.resource_type == resource_type)
    q = q.filter(Permission.resource_id == resource_id)
    permission = q.first()
    if permission is None:
        permission = Permission()
        permission.role_id = data['role']
        permission.resource_type = resource_type
        permission.resource_id = resource_id
    permission.read = data['read']
    permission.write = data['write']
    session.add(permission)
    session.commit()
    return jsonify({
        'status': 'ok',
        'updated': permission
    })
