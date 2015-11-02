from flask import Blueprint
from apikit import obj_or_404, Pager, jsonify

from loom.db import session, Collection


collections_api = Blueprint('collections', __name__)


@collections_api.route('/api/collections')
def index():
    # FIXME: authz
    collections = session.query(Collection)
    return jsonify(Pager(collections))


@collections_api.route('/api/collections/<id>')
def view(id):
    # FIXME: authz
    collection = session.query(Collection).filter(Collection.id == id).first()
    collection = obj_or_404(collection)
    return jsonify({'status': 'ok', 'data': collection})
