from flask import render_template, jsonify, abort
from elasticsearch import ElasticsearchException

from schwifty.core import app, es, es_index

# TODO: support OAuth against ID
# TODO: make notes, bookmarks, links


@app.errorhandler(ElasticsearchException)
def handle_error(err):
    res = jsonify({'status': 'error', 'message': unicode(err)})
    res.status_code = 500
    return res


@app.route('/api/entity/<doc_type>/<id>')
def entity(doc_type, id):
    data = es.get(index=es_index, doc_type=doc_type, id=id)
    return jsonify({'status': 'ok', 'data': data.get('_source')})


@app.route('/')
def index():
    return render_template('index.html')
