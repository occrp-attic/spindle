import os

DEBUG = False
ASSETS_DEBUG = False

ELASTICSEARCH_HOST = 'elasticsearch:9200'
ELASTICSEARCH_INDEX = 'graph'

DATABASE_URI = os.environ.get('SPINDLE_DATABASE_URI')
PREFERRED_URL_SCHEME = 'https'

OAUTH = {
    'consumer_key': os.environ.get('SPINDLE_OAUTH_KEY'),
    'consumer_secret': os.environ.get('SPINDLE_OAUTH_SECRET'),
    'base_url': 'https://investigativedashboard.org/',
    'request_token_url': None,
    'access_token_method': 'POST',
    'access_token_url': 'https://investigativedashboard.org/o/token/',
    'authorize_url': 'https://investigativedashboard.org/o/authorize',
}
