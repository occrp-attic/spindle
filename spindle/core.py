from flask import Flask, current_app
from flask.ext.assets import Environment
from flask_oauthlib.client import OAuth
from elasticsearch import Elasticsearch
from werkzeug.contrib.cache import SimpleCache

from loom.config import Config
from loom.indexer import Indexer
from spindle import default_settings

assets = Environment()
cache = SimpleCache(default_timeout=3600)
oauth = OAuth()
oauth_provider = oauth.remote_app('provider', app_key='OAUTH')


def create_app(config={}):
    app = Flask('spindle')
    app.config.from_object(default_settings)
    app.config.from_envvar('SPINDLE_SETTINGS', silent=True)
    app.config.update(config)

    config = {
        'schemas': app.config.get('SCHEMAS'),
        'database': app.config.get('DATABASE_URI'),
        'elastic_host': app.config.get('ELASTICSEARCH_HOST'),
        'elastic_index': app.config.get('ELASTICSEARCH_INDEX')
    }
    app.loom_config = Config(config)
    app.loom_config.setup()

    assets.init_app(app)
    oauth.init_app(app)
    return app


def get_es():
    return current_app.loom_config.elastic_client


def get_es_index():
    return current_app.loom_config.elastic_index


def get_loom_config():
    return current_app.loom_config


def get_loom_indexer():
    if not hasattr(current_app, 'loom_indexer'):
        current_app.loom_indexer = Indexer(get_loom_config())
    return current_app.loom_indexer
