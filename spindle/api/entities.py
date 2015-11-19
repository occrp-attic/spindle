from flask import Blueprint, request
from apikit import jsonify, obj_or_404, request_data, arg_int
from werkzeug.exceptions import BadRequest

from spindle import authz
from spindle.core import get_loom_config, get_loom_indexer
from spindle.util import result_entity
from spindle.validation import validate
from spindle.api.collections import get_collection
from spindle.logic.entities import collection_entities
from spindle.logic.collections import collection_add_entity


entities_api = Blueprint('entities', __name__)


def get_depth(default):
    return max(1, min(arg_int('depth', default=default), 3))


@entities_api.route('/api/entities/<path:id>')
def view(id):
    entities = get_loom_config().entities
    data = obj_or_404(entities.get(id, depth=get_depth(3),
                                   right=authz.entity_right()))
    return jsonify({'status': 'ok', 'data': result_entity(data)})


@entities_api.route('/api/collections/<int:collection>/entities')
def collection_index(collection):
    collection = get_collection(collection, authz.READ)
    results = collection_entities(collection, depth=get_depth(2),
                                  filter_schema=request.args.get('$schema'))
    return jsonify({
        'results': results
    })


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
    collection_add_entity(collection, subject)
    get_loom_indexer().index_one(subject, schema=schema)
    entity = entities.get(subject, schema=schema, depth=2,
                          right=authz.entity_right())
    return jsonify({
        'status': 'ok',
        'data': entity
    }, status=200 if update_operation else 201)
