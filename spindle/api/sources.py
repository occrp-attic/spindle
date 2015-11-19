from flask import Blueprint
from apikit import obj_or_404, Pager, jsonify, request_data

from loom.db import session, Source
from spindle import authz
from spindle.validation import validate

sources_schema = 'https://schema.occrp.org/operational/source.json#'
sources_api = Blueprint('sources', __name__)


@sources_api.route('/api/sources')
def index():
    collections = authz.collections(authz.READ)
    if not len(collections):
        return jsonify(Pager([]))
    q = session.query(Source)
    q = q.filter(Source.id.in_(collections))
    q = q.order_by(Source.title.asc())
    return jsonify(Pager(q))


@sources_api.route('/api/sources/<int:id>')
def view(id):
    source = session.query(Source).filter(Source.id == id).first()
    source = obj_or_404(source)
    authz.require(authz.source(authz.READ, source.id))
    return jsonify({'status': 'ok', 'data': source})


@sources_api.route('/api/sources/<int:id>', methods=['POST', 'PUT'])
def update(id):
    source = session.query(Source).filter(Source.id == id).first()
    source = obj_or_404(source)
    authz.require(authz.source(authz.WRITE, source.id))
    data = request_data()
    validate(data, sources_schema)
    source.title = data.get('title')
    source.url = data.get('url')
    session.add(source)
    session.commit()
    return jsonify({'status': 'ok', 'data': source})
