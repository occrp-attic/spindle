from flask import Flask
from flask.ext.assets import Environment
from elasticsearch import Elasticsearch

from schwifty import default_settings

app = Flask(__name__)
app.config.from_object(default_settings)

es = Elasticsearch(app.config.get('ELASTICSEARCH_HOST'))
es_index = app.config.get('ELASTICSEARCH_INDEX')

assets = Environment(app)
