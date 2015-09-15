from flask import render_template, jsonify, request
from elasticsearch import ElasticsearchException

from schwifty.core import app, es, es_index
from schwifty.search import query
from schwifty.util import angular_templates

# TODO: support OAuth against ID
# TODO: make notes, bookmarks, links


@app.errorhandler(ElasticsearchException)
def handle_error(err):
    res = jsonify({'status': 'error', 'message': unicode(err)})
    res.status_code = 500
    return res


@app.route('/api/entity/<doc_type>/<path:id>')
def entity(doc_type, id):
    data = es.get(index=es_index, doc_type=doc_type, id=id)
    return jsonify({'status': 'ok', 'data': data.get('_source')})


@app.route('/api/search')
def search():
    result = query(request.args.get('q', ''))
    return jsonify(result)


@app.route('/')
def index():
    templates = angular_templates()
    return render_template('index.html', templates=templates)
