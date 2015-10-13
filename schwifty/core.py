from flask import Flask
from flask.ext.assets import Environment
from flask.ext.sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch
from werkzeug.contrib.cache import SimpleCache

from schwifty import default_settings

app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar('SCHWIFTY_SETTINGS', silent=True)

es = Elasticsearch(app.config.get('ELASTICSEARCH_HOST'))
es_index = app.config.get('ELASTICSEARCH_INDEX')

db = SQLAlchemy(app)

assets = Environment(app)
cache = SimpleCache(default_timeout=3600)
