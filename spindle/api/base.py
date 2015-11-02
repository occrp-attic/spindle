from flask import render_template, request, Blueprint
from elasticsearch import ElasticsearchException
from jsonschema import ValidationError
from apikit import jsonify

from loom.db import session
from spindle.core import get_es, get_es_index
from spindle.search import query, more_like_this
from spindle.metadata import get_metadata
from spindle.util import angular_templates

# TODO: make notes, bookmarks, links

base_api = Blueprint('base', __name__)


@base_api.app_errorhandler(ElasticsearchException)
def handle_es_error(err):
    return jsonify({'status': 'error', 'message': unicode(err)}, status=500)


@base_api.app_errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify({
        'status': 'error',
        'message': err.message,
        'cause': err.cause,
        'value': err.validator_value,
        'instance': err.instance,
        'schema': err.schema,
        'parent': err.parent
    }, status=400)


@base_api.after_app_request
def clear_session(resp):
    session.close()
    return resp


@base_api.route('/api/like/<path:id>')
def like(id):
    ent = get_es().get(index=get_es_index(), id=id, _source=False)
    return jsonify(more_like_this(ent))


@base_api.route('/api/search')
def search():
    result = query(request.args)
    return jsonify(result)


@base_api.route('/api/metadata')
def metadata():
    return jsonify(get_metadata())


@base_api.route('/')
def index():
    templates = angular_templates()
    return render_template('index.html', templates=templates)
