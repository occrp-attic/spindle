from flask import Blueprint, request
from apikit import jsonify, obj_or_404, request_data
from werkzeug.exceptions import BadRequest

from loom.db import CollectionSubject, session
from spindle import authz
from spindle.core import get_loom_config, get_loom_indexer
from spindle.validation import validate
from spindle.util import result_entity
from spindle.api.collections import get_collection

entities_api = Blueprint('entities', __name__)


@entities_api.route('/api/entities/<path:id>')
def view(id):
    entities = get_loom_config().entities
    data = obj_or_404(entities.get(id, depth=3, right=authz.entity_right()))
    return jsonify({'status': 'ok', 'data': result_entity(data)})


@entities_api.route('/api/collections/<int:collection>/entities')
def collection_index(collection):
    collection = get_collection(collection, authz.READ)
    entities = get_loom_config().entities
    schema_filter = request.args.get('$schema')
    if schema_filter is not None:
        config = get_loom_config()
        schema_filter = config.implied_schemas(schema_filter)
    # FIXME: this is a performance nightmare. Think about how to fix it.
    results = []
    for cs in collection.subjects:
        schema = entities.get_schema(cs.subject, right=authz.entity_right())
        if schema is None:
            continue
        if schema_filter is not None and schema not in schema_filter:
            continue
        data = entities.get(cs.subject, schema=schema, depth=2,
                            right=authz.entity_right())
        results.append(result_entity(data))
    return jsonify({
        'results': results
    })


def add_to_collection(collection, subject):
    q = session.query(CollectionSubject).filter_by(subject=subject)
    q = q.filter_by(collection_id=collection.id)
    cs = q.first()
    if cs is None:
        cs = CollectionSubject(collection, subject)
    session.add(cs)
    session.commit()


@entities_api.route('/api/collections/<int:collection>/entities',
                    methods=['POST', 'PUT'])
def collection_entity_save(collection):
    collection = get_collection(collection, authz.WRITE)
    data = request_data()
    update_operation = 'id' in data

    entities = get_loom_config().entities
    if update_operation:
        schema = entities.get_schema(data['id'], right=authz.entity_right())
    else:
        schema = data.get('$schema')

    if schema not in get_loom_config().schemas.values():
        raise BadRequest()

    # this will raise if it fails:
    validate(data, schema)

    subject = entities.save(schema, data, collection_id=collection.id,
                            author=request.auth_user,
                            right=authz.entity_right())
    add_to_collection(collection, subject)
    get_loom_indexer().index_one(subject, schema=schema)
    entity = entities.get(subject, schema=schema, depth=2,
                          right=authz.entity_right())
    return jsonify({
        'status': 'ok',
        'data': entity
    }, status=200 if update_operation else 201)
