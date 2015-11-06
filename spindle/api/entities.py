from flask import Blueprint
from apikit import jsonify, obj_or_404

from spindle import authz
from spindle.core import get_loom_config
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
    # FIXME: this is a performance nightmare. Think about how to fix it.
    results = []
    for cs in collection.subjects:
        schema = entities.get_schema(cs.subject, right=authz.entity_right())
        if schema is None:
            continue
        data = entities.get(cs.subject, schema=schema, depth=2,
                            right=authz.entity_right())
        results.append(data)
    return jsonify({
        'results': results
    })
