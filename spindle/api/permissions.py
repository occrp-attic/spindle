from flask import Blueprint, request
from apikit import jsonify

from loom.db import session
from spindle.model import Role, Permission

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


@permissions_api.route('/api/permissions')
def index():
    q = session.query(Permission)
    # TODO: authz
    if 'collection' in request.args:
        q = q.filter(Permission.resource_type == Permission.COLLECTION)
        q = q.filter(Permission.resource_id == request.args.get('collection'))
    elif 'source' in request.args:
        q = q.filter(Permission.resource_type == Permission.SOURCE)
        q = q.filter(Permission.resource_id == request.args.get('source'))
    else:
        return jsonify({
            'status': 'error',
            'message': 'You need to specify either a source or a collection.'
        }, status=400)
    return jsonify({
        'total': q.count(),
        'results': q
    })


@permissions_api.route('/api/permissions', methods=['POST', 'PUT'])
@permissions_api.route('/api/permissions/<id>', methods=['POST', 'PUT'])
def create_or_update(id=None):
    pass
