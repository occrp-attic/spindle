import os

DEBUG = False
ASSETS_DEBUG = False
SECRET_KEY = os.environ.get('SPINDLE_SECRET_KEY')

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

MAIL_FROM = os.environ.get('MAIL_FROM')
MAIL_HOST = os.environ.get('MAIL_HOST')
MAIL_ADMINS = [os.environ.get('MAIL_ADMIN')]
MAIL_CREDENTIALS = (os.environ.get('MAIL_USERNAME'),
                    os.environ.get('MAIL_PASSWORD'))
