from flask import Blueprint
from apikit import jsonify, obj_or_404

from spindle import authz
from spindle.core import get_loom_config
from spindle.util import result_entity

entities_api = Blueprint('entities', __name__)


@entities_api.route('/api/entities/<path:id>')
def view(id):
    data = get_loom_config().entities.get(id, depth=3,
                                          right=authz.entity_right())
    data = obj_or_404(data)
    return jsonify({'status': 'ok', 'data': result_entity(data)})
