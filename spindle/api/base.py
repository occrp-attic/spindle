from flask import render_template, jsonify, request, Blueprint
from elasticsearch import ElasticsearchException

from loom.db import session
from spindle.core import get_es, get_es_index
from spindle.search import query, more_like_this
from spindle.metadata import get_metadata
from spindle.util import angular_templates

# TODO: make notes, bookmarks, links

base_api = Blueprint('base', __name__)


@base_api.app_errorhandler(ElasticsearchException)
def handle_error(err):
    res = jsonify({'status': 'error', 'message': unicode(err)})
    res.status_code = 500
    return res


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
