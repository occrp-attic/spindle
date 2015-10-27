from flask.ext.testing import TestCase as FlaskTestCase

from spindle.core import get_es, db
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

    def login(self, id='tester', name=None, email=None):
        with self.client.session_transaction() as session:
            session['user_id'] = 'test:%s' % id
            session['user'] = {
                'name': name or id.capitalize(),
                'email': email or id + '@example.com'
            }

    def setUp(self):
        self.es = get_es()
        self.es.indices.create(index=self.ES_INDEX, ignore=400)
        db.create_all()

    def tearDown(self):
        self.es.indices.delete(index=self.ES_INDEX, ignore=[400, 404])
        db.session.remove()
        db.drop_all()
