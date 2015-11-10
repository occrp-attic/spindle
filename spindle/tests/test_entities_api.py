import json

from loom.db import Collection, CollectionSubject, session
from spindle.model import Permission, Role
from spindle.tests.util import TestCase


class EntitiesApiTestCase(TestCase):

    def setUp(self):
        super(EntitiesApiTestCase, self).setUp()
        self.coll = Collection()
        self.coll.title = "Test Collection"
        session.add(self.coll)
        session.flush()
        permission = Permission()
        permission.role_id = Role.SYSTEM_USER
        permission.read = True
        permission.write = True
        permission.resource_id = self.coll.id
        permission.resource_type = Permission.COLLECTION
        session.add(permission)
        self.schema_uri = 'https://schema.occrp.org/generic/organization.json#'
        self.entity = {'id': 'foo', 'name': 'Foobar'}
        self.config.entities.save(self.schema_uri, self.entity,
                                  collection_id=self.coll.id)
        cs = CollectionSubject(self.coll, self.entity['id'])
        session.add(cs)
        entity = {'id': 'test', 'name': 'Testing'}
        self.config.entities.save(self.schema_uri, entity,
                                  collection_id=self.coll.id)
        cs = CollectionSubject(self.coll, entity['id'])
        session.add(cs)
        session.commit()

    def test_view(self):
        res = self.client.get('/api/entities/foo')
        assert res.status_code == 404, res

        self.login()
        res = self.client.get('/api/entities/foo')
        assert res.status_code == 200, res
        data = res.json['data']
        assert 'name' in data, data
        assert data['name'] == 'Foobar', data

    def test_view_not_found(self):
        self.login()
        res = self.client.get('/api/entities/foobar')
        assert res.status_code == 404, res

    def test_collection_index(self):
        url = '/api/collections/%s/entities' % self.coll.id
        res = self.client.get(url)
        assert res.status_code == 403, res

        self.login()
        url = '/api/collections/%s/entities' % self.coll.id
        res = self.client.get(url)
        assert res.status_code == 200, res
        results = res.json['results']
        assert len(results) == 2, res.json
        assert 'name' in results[0], res.json
        assert '$schema' in results[0], res.json

        res = self.client.get(url, query_string={'$schema': self.schema_uri})
        assert res.status_code == 200, res
        results = res.json['results']
        assert len(results) == 2, res.json

        res = self.client.get(url, query_string={'$schema': 'foo'})
        assert res.status_code == 200, res
        results = res.json['results']
        assert len(results) == 0, res.json

    def test_create_entity(self):
        self.login()
        url = '/api/collections/%s/entities' % self.coll.id
        ent = {
            '$schema': self.schema_uri,
            'name': 'Mother Superior'
        }
        res = self.client.post(url, data=json.dumps(ent),
                               content_type='application/json')
        assert res.status_code == 201, res
        data = res.json['data']
        assert 'id' in data, res.json
        assert 'name' in data, res.json
        assert data['name'] == ent['name'], res.json
        assert 'tester' in data['$authors'], res.json

        ent = {'name': 'Mother Superior'}
        res = self.client.post(url, data=json.dumps(ent),
                               content_type='application/json')
        assert res.status_code == 400, res

        ent = {'name': 'Mother Superior', '$schema': 'foo'}
        res = self.client.post(url, data=json.dumps(ent),
                               content_type='application/json')
        assert res.status_code == 400, res

        ent = {'$schema': self.schema_uri}
        res = self.client.post(url, data=json.dumps(ent),
                               content_type='application/json')
        assert res.status_code == 400, res

    def test_entity_update_dedupe(self):
        self.login()
        config = self.app.loom_config
        type_num = len(config.types)
        prop_num = len(config.properties)
        # assert False, (type_num, prop_num)
        url = '/api/collections/%s/entities' % self.coll.id
        ent = {
            'id': 'foo',
            '$schema': self.schema_uri,
            'name': 'New name'
        }
        res = self.client.post(url, data=json.dumps(ent),
                               content_type='application/json')
        assert res.status_code == 200, res
        assert len(config.types) == type_num, (len(config.types), type_num)
        assert len(config.properties) == prop_num + 1, len(config.properties)
