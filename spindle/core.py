from flask import Flask, current_app
from flask.ext.assets import Environment
from flask.ext.sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth
from elasticsearch import Elasticsearch
from werkzeug.contrib.cache import SimpleCache

from spindle import default_settings

db = SQLAlchemy()
assets = Environment()
cache = SimpleCache(default_timeout=3600)
oauth = OAuth()
oauth_provider = oauth.remote_app('provider', app_key='OAUTH')


def create_app(config={}):
    app = Flask('spindle')
    app.config.from_object(default_settings)
    app.config.from_envvar('SPINDLE_SETTINGS', silent=True)
    app.config.update(config)

    assets.init_app(app)
    db.init_app(app)
    oauth.init_app(app)
    return app


def get_es():
    if not hasattr(current_app, '_spindle_es'):
        host = current_app.config.get('ELASTICSEARCH_HOST')
        current_app._spindle_es = Elasticsearch(host)
    return current_app._spindle_es


def get_es_index():
    return current_app.config.get('ELASTICSEARCH_INDEX')
