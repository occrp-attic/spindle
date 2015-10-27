from flask.ext.testing import TestCase as FlaskTestCase

from spindle.core import get_es, get_es_index
from spindle.cli import configure_app


class TestCase(FlaskTestCase):

    ES_INDEX = 'spindle_test_idx_'

    def create_app(self):
        app = configure_app({
            'DEBUG': True,
            'TESTING': True,
            'ELASTICSEARCH_INDEX': self.ES_INDEX,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'PRESERVE_CONTEXT_ON_EXCEPTION': False,
            'CELERY_ALWAYS_EAGER': True
        })
        return app

    def setUp(self):
        self.es = get_es()
        self.es.indices.create(index=self.ES_INDEX, ignore=400)

    def tearDown(self):
        self.es.indices.delete(index=self.ES_INDEX, ignore=[400, 404])
