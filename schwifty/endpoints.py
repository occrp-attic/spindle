from flask import render_template, jsonify

from schwifty.core import app

# TODO: support OAuth against ID
# TODO: make notes, bookmarks, links


@app.route('/api/entity/<doc_type>/<id>')
def entity(doc_type, id):
    return jsonify({'status': 'ok'})


@app.route('/')
def index():
    return render_template('index.html')
