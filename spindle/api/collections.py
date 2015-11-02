from flask import Blueprint
from apikit import obj_or_404, Pager, jsonify, request_data

from loom.db import session, Collection
from spindle.core import validate

collections_schema = 'https://schema.occrp.org/operational/collection.json#'
collections_api = Blueprint('collections', __name__)


@collections_api.route('/api/collections')
def index():
    # FIXME: authz
    collections = session.query(Collection)
    return jsonify(Pager(collections))


@collections_api.route('/api/collections', methods=['POST', 'PUT'])
def create():
    # FIXME: authz
    data = request_data()
    validate(data, collections_schema)
    collection = Collection()
    collection.title = data.get('title')
    session.add(collection)
    session.commit()
    return jsonify({'status': 'ok', 'data': collection}, status=201)


@collections_api.route('/api/collections/<id>')
def view(id):
    # FIXME: authz
    collection = session.query(Collection).filter(Collection.id == id).first()
    collection = obj_or_404(collection)
    return jsonify({'status': 'ok', 'data': collection})


@collections_api.route('/api/collections/<id>', methods=['POST', 'PUT'])
def update(id):
    # FIXME: authz
    collection = session.query(Collection).filter(Collection.id == id).first()
    collection = obj_or_404(collection)
    data = request_data()
    validate(data, collections_schema)
    collection.title = data.get('title')
    session.add(collection)
    session.commit()
    return jsonify({'status': 'ok', 'data': collection})
