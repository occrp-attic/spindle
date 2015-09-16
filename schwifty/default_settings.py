import os

DEBUG = True
VERSION = "0.0.1"
PORT = os.environ.get('PORT', 6174)

ELASTICSEARCH_HOST = 'localhost:9200'
ELASTICSEARCH_INDEX = 'datavault'
SOURCE_DOC_TYPE = 'source'
