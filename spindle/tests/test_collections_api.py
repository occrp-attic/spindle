import json

from loom.db import Collection, session
from spindle.model import Permission, Role
from spindle.tests.util import TestCase


class CollectionsApiTestCase(TestCase):

    def setUp(self):
        super(CollectionsApiTestCase, self).setUp()
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
        session.commit()
        self.schema_uri = 'https://schema.occrp.org/generic/organization.json#'
        self.entity = {'id': 'foo', 'name': 'Foobar'}
        self.config.entities.save(self.schema_uri, self.entity,
                                  collection_id=self.coll.id)

    def test_index(self):
        res = self.client.get('/api/collections')
        assert res.status_code == 200, res
        assert res.json['total'] == 0, res.json
        self.login()
        res = self.client.get('/api/collections')
        assert res.status_code == 200, res
        assert res.json['total'] >= 1, res.json

    def test_view(self):
        res = self.client.get('/api/collections/%s' % self.coll.id)
        assert res.status_code == 403, res
        self.login()
        res = self.client.get('/api/collections/%s' % self.coll.id)
        assert res.status_code == 200, res.json
        data = res.json['data']
        assert data['title'] == self.coll.title

    def test_view_not_found(self):
        res = self.client.get('/api/collections/8388')
        assert res.status_code == 404, res

    def test_create(self):
        self.login()
        data = json.dumps({'title': "Hannah Banana"})
        res = self.client.post('/api/collections', data=data,
                               content_type='application/json')
        assert res.status_code == 201, res
        assert res.json['data']['id'], res.json
        assert not len(res.json['data']['subjects']), res.json

    def test_create_invalid(self):
        self.login()
        data = json.dumps({'title': "H"})
        res = self.client.post('/api/collections', data=data,
                               content_type='application/json')
        assert res.status_code == 400, res
        assert 'too short' in res.json['message'], res.json

    def test_create_with_subjects(self):
        self.login()
        data = json.dumps({"title": "Hannah Banana", "subjects": ["foo"]})
        res = self.client.post('/api/collections', data=data,
                               content_type='application/json')
        assert res.status_code == 201, res
        assert res.json['data']['id'], res.json
        assert 1 == len(res.json['data']['subjects']), res.json

    def test_update(self):
        self.login()
        res = self.client.get('/api/collections/%s' % self.coll.id)
        assert res.status_code == 200, res
        assert 'data' in res.json, res.json
        data = res.json['data']
        data['title'] = '%s - new' % data['title']
        jdata = json.dumps(data)
        res = self.client.post('/api/collections/%s' % data['id'], data=jdata,
                               content_type='application/json')
        assert res.status_code == 200, res
        assert res.json['data']['title'] == data['title'], res.json
        assert res.json['data']['id'], res.json

    def test_update_invalid(self):
        self.login()
        res = self.client.get('/api/collections/%s' % self.coll.id)
        data = res.json['data']
        data['title'] = 'H'
        jdata = json.dumps(data)
        res = self.client.post('/api/collections/%s' % data['id'], data=jdata,
                               content_type='application/json')
        assert res.status_code == 400, res

    def test_update_subjects(self):
        self.schema_uri = 'https://schema.occrp.org/generic/organization.json#'
        self.entity = {'id': 'bar', 'name': 'Barfoo'}
        self.config.entities.save(self.schema_uri, self.entity, 'test_source')

        data = json.dumps({"title": "Hannah Banana", "subjects": ["foo"]})
        res = self.client.post('/api/collections', data=data,
                               content_type='application/json')
        assert res.status_code == 403, res
        self.login()
        res = self.client.post('/api/collections', data=data,
                               content_type='application/json')
        assert res.status_code == 201, res
        assert res.json['data']['id'], res.json
        assert 1 == len(res.json['data']['subjects']), res.json
        data = res.json['data']
        data['subjects'] = ['bar']
        res = self.client.post('/api/collections/%s' % res.json['data']['id'],
                               data=json.dumps(data),
                               content_type='application/json')
        assert res.status_code == 200, res
        assert res.json['data']['id'], res.json
        assert 1 == len(res.json['data']['subjects']), res.json
        assert 'bar' in res.json['data']['subjects'], res.json
        assert 'foo' not in res.json['data']['subjects'], res.json

    def test_create_with_invalid_subjects(self):
        self.login()
        data = json.dumps({"title": "Hannah Banana", "subjects": ["no-foo"]})
        res = self.client.post('/api/collections', data=data,
                               content_type='application/json')
        assert res.status_code == 400, res
