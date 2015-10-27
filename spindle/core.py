from flask import Flask, g, current_app
from flask.ext.assets import Environment
from flask.ext.sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch
from werkzeug.contrib.cache import SimpleCache

from spindle import default_settings

db = SQLAlchemy()
assets = Environment()
cache = SimpleCache(default_timeout=3600)


def create_app(config={}):
    app = Flask('spindle')
    app.config.from_object(default_settings)
    app.config.from_envvar('SPINDLE_SETTINGS', silent=True)
    app.config.update(config)

    assets.init_app(app)
    db.init_app(app)
    return app


def get_es():
    if not hasattr(g, 'spindle_es'):
        host = current_app.config.get('ELASTICSEARCH_HOST')
        g.spindle_es = Elasticsearch(host)
    return g.spindle_es


def get_es_index():
    return current_app.config.get('ELASTICSEARCH_INDEX')
