from flask import jsonify, Blueprint

from spindle.core import get_es, get_es_index
from spindle.util import result_entity

entities_api = Blueprint('entities', __name__)


@entities_api.route('/api/entities/<path:id>')
def view(id):
    data = get_es().get(index=get_es_index(), id=id,
                        _source_exclude=['$text', '$latin'])
    return jsonify({'status': 'ok', 'data': result_entity(data)})
