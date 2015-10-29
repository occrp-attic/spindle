import os
import yaml
import logging
import unicodecsv

from flask.ext.testing import TestCase as FlaskTestCase
from jsonmapping import Mapper

from spindle.core import get_es, get_loom_config, get_loom_indexer, db
from spindle.cli import configure_app

FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')
BA_SOURCE = 'ba_parliament'
BA_FIXTURES = {'entities': [], 'resolver': None}

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('elasticsearch').setLevel(logging.WARNING)


def load_ba_fixtures():
    # This is messy. Would be cool to do it more cleanly, but how?
    config = get_loom_config()
    if not BA_FIXTURES['resolver']:
        BA_FIXTURES['resolver'] = config.resolver
    config._resolver = BA_FIXTURES['resolver']

    if not len(BA_FIXTURES['entities']):
        with open(os.path.join(FIXTURES, 'ba.mapping.yaml'), 'rb') as fh:
            mapping = yaml.load(fh)
        mapper = Mapper(mapping, config.resolver, scope=config.base_uri)
        with open(os.path.join(FIXTURES, 'ba.csv'), 'rb') as csvfh:
            reader = unicodecsv.DictReader(csvfh)
            for row in reader:
                _, data = mapper.apply(row)
                BA_FIXTURES['entities'].append(data)

    config.sources.upsert({
        'slug': BA_SOURCE,
        'title': 'BiH Parliament',
        'url': 'http://foo.ba/'
    })
    for entity in BA_FIXTURES['entities']:
        config.entities.save(entity['$schema'], entity, BA_SOURCE)
    get_loom_indexer().index(source=BA_SOURCE)


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
            session['user'] = {
                'id': 'test:%s' % id,
                'name': name or id.capitalize(),
                'email': email or id + '@example.com'
            }

    def setUp(self):
        self.es = get_es()
        self.es.indices.create(index=self.ES_INDEX, ignore=400)
        db.create_all()

    def setUpFixtures(self):
        load_ba_fixtures()

    def tearDown(self):
        self.es.indices.delete(index=self.ES_INDEX, ignore=[400, 404])
        db.session.remove()
        db.drop_all()
