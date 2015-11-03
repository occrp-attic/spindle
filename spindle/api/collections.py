from flask import Blueprint
from apikit import obj_or_404, Pager, jsonify, request_data
from werkzeug.exceptions import BadRequest
from sqlalchemy.orm import subqueryload

from loom.db import session, Collection, CollectionSubject
from spindle.core import validate, get_loom_config

collections_schema = 'https://schema.occrp.org/operational/collection.json#'
collections_api = Blueprint('collections', __name__)


def update_subjects(collection, data):
    """ There must be a nicer way to do this in SQLA. """
    # TODO: authz
    subjects = data.get('subjects', [])
    for cs in collection.subjects:
        if cs.subject in subjects:
            subjects.remove(cs.subject)
        else:
            session.delete(cs)
    for subject in subjects:
        # TODO: check the subjects exist
        if get_loom_config().entities.get_schema(subject):
            cs = CollectionSubject(collection, subject)
            session.add(cs)
        else:
            raise BadRequest()


@collections_api.route('/api/collections')
def index():
    # FIXME: authz
    collections = session.query(Collection)
    collections = collections.options(subqueryload('subjects'))
    collections = collections.order_by(Collection.updated_at.desc())
    return jsonify(Pager(collections))


@collections_api.route('/api/collections', methods=['POST', 'PUT'])
def create():
    # FIXME: authz
    data = request_data()
    validate(data, collections_schema)
    collection = Collection()
    collection.title = data.get('title')
    session.add(collection)
    update_subjects(collection, data)
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
    update_subjects(collection, data)
    session.commit()
    return jsonify({'status': 'ok', 'data': collection})
