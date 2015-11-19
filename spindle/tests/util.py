import os
import yaml
import unicodecsv

from flask.ext.testing import TestCase as FlaskTestCase
from jsonmapping import Mapper

from loom.db import Source, Base, session
from spindle.model import Role, Permission
from spindle.core import get_es, get_loom_indexer, load_local_schema
from spindle.cli import configure_app

FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')
ES_INDEX = 'spindle_test_idx_'
BA_SOURCE = 'ba_parliament'
BA_FIXTURES = {'entities': [], 'resolver': None}


def load_schemas(resolver):
    schema_dir = os.path.join(FIXTURES, 'schema')
    for fn in os.listdir(schema_dir):
        with open(os.path.join(schema_dir, fn), 'r') as fh:
            schema = yaml.load(fh)
            resolver.store[schema.get('id')] = schema


def load_ba_fixtures(config):
    # This is messy. Would be cool to do it more cleanly, but how?
    if not len(BA_FIXTURES['entities']):
        with open(os.path.join(FIXTURES, 'ba.mapping.yaml'), 'rb') as fh:
            mapping = yaml.load(fh)
        mapper = Mapper(mapping, config.resolver, scope=config.base_uri)
        with open(os.path.join(FIXTURES, 'ba.csv'), 'rb') as csvfh:
            reader = unicodecsv.DictReader(csvfh)
            for row in reader:
                _, data = mapper.apply(row)
                BA_FIXTURES['entities'].append(data)

    source = Source.ensure({
        'slug': BA_SOURCE,
        'title': 'BiH Parliament',
        'url': 'http://foo.ba/'
    })
    permission = Permission()
    permission.role_id = Role.SYSTEM_USER
    permission.read = True
    permission.write = False
    permission.resource_id = source.id
    permission.resource_type = Permission.SOURCE
    session.add(permission)
    session.commit()
    for entity in BA_FIXTURES['entities']:
        config.entities.save(entity['$schema'], entity, source_id=source.id)
    get_loom_indexer().index(source=BA_SOURCE)


class TestCase(FlaskTestCase):

    def create_app(self):
        return configure_app({
            'DEBUG': True,
            'TESTING': True,
            'ELASTICSEARCH_INDEX': ES_INDEX,
            'DATABASE_URI': 'sqlite:///:memory:',
            'PRESERVE_CONTEXT_ON_EXCEPTION': False,
            'CELERY_ALWAYS_EAGER': True
        })

    def create_user(self, id='tester', name=None, email=None, is_admin=False):
        role = Role.load_or_create(id, Role.USER, name or id, email=email,
                                   is_admin=is_admin)
        session.commit()
        return role

    def login(self, id='tester', name=None, email=None, is_admin=False):
        self.create_user(id=id, name=name, email=email, is_admin=is_admin)
        with self.client.session_transaction() as sess:
            sess['roles'] = [Role.SYSTEM_GUEST, Role.SYSTEM_USER, id]
            sess['user'] = id
            sess['is_admin'] = is_admin

    def setUp(self):
        Role.create_defaults()
        self.config = self.app.loom_config
        if not BA_FIXTURES['resolver']:
            schema_dir = os.path.join(FIXTURES, 'schema')
            load_local_schema(self.config.resolver, schema_dir=schema_dir)
            BA_FIXTURES['resolver'] = self.config.resolver
        self.config._resolver = BA_FIXTURES['resolver']
        self.es = get_es()
        get_loom_indexer().configure()

    def setUpFixtures(self):
        load_ba_fixtures(self.app.loom_config)

    def tearDown(self):
        self.es.indices.delete(index=ES_INDEX, ignore=[400, 404])
        session.close()
        Base.metadata.drop_all()
        Base.metadata.create_all()
