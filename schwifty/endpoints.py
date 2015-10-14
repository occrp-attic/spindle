from flask import render_template, jsonify, request
from elasticsearch import ElasticsearchException

from schwifty.core import app, es, es_index
from schwifty.search import query
from schwifty.metadata import get_metadata
from schwifty.mlt import more_like_this
from schwifty.util import angular_templates, result_entity

# TODO: support OAuth against ID
# TODO: make notes, bookmarks, links


@app.errorhandler(ElasticsearchException)
def handle_error(err):
    res = jsonify({'status': 'error', 'message': unicode(err)})
    res.status_code = 500
    return res


@app.route('/api/entity/<path:id>')
def entity(id):
    data = es.get(index=es_index, id=id, _source_exclude=['$text', '$latin'])
    return jsonify({'status': 'ok', 'data': result_entity(data)})


@app.route('/api/like/<path:id>')
def like(id):
    ent = es.get(index=es_index, id=id, _source=False)
    return jsonify(more_like_this(ent))


@app.route('/api/search')
def search():
    result = query(request.args)
    return jsonify(result)


@app.route('/api/metadata')
def metadata():
    return jsonify(get_metadata())


@app.route('/')
def index():
    templates = angular_templates()
    return render_template('index.html', templates=templates)
