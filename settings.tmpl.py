DEBUG = True
ASSETS_DEBUG = True
APP_NAME = 'OCCRP Search'

ELASTICSEARCH_HOST = '127.0.0.1:9200'
ELASTICSEARCH_INDEX = 'graph'
SOURCE_DOC_TYPE = 'source'

SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/loom'

OAUTH = {
    'consumer_key': None,
    'consumer_secret': None,
    'request_token_params': {
        'scope': 'https://www.googleapis.com/auth/userinfo.email'
    },
    'base_url': 'https://www.googleapis.com/oauth2/v1/',
    'request_token_url': None,
    'access_token_method': 'POST',
    'access_token_url': 'https://accounts.google.com/o/oauth2/token',
    'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
}
