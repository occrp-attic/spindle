import json

from loom.db import Source, session
from spindle.model import Permission, Role
from spindle.tests.util import TestCase


class SourcesApiTestCase(TestCase):

    def setUp(self):
        super(SourcesApiTestCase, self).setUp()
        self.source = Source()
        self.source.slug = "test"
        self.source.title = "Test Collection"
        self.source.url = "http://test.com/"
        session.add(self.source)
        session.flush()
        permission = Permission()
        permission.role_id = Role.SYSTEM_USER
        permission.read = True
        permission.write = True
        permission.resource_id = self.source.id
        permission.resource_type = Permission.SOURCE
        session.add(permission)
        session.commit()

    def test_index(self):
        res = self.client.get('/api/sources')
        assert res.status_code == 200, res
        assert res.json['total'] == 0, res.json
        self.login()
        res = self.client.get('/api/sources')
        assert res.status_code == 200, res
        assert res.json['total'] >= 1, res.json

    def test_view(self):
        res = self.client.get('/api/sources/%s' % self.source.id)
        assert res.status_code == 403, res
        self.login()
        res = self.client.get('/api/sources/%s' % self.source.id)
        assert res.status_code == 200, res.json
        data = res.json['data']
        assert data['title'] == self.source.title

    def test_view_not_found(self):
        res = self.client.get('/api/sources/8388')
        assert res.status_code == 404, res

    def test_update(self):
        self.login()
        res = self.client.get('/api/sources/%s' % self.source.id)
        data = res.json['data']
        data['title'] = '%s - new' % data['title']
        jdata = json.dumps(data)
        res = self.client.post('/api/sources/%s' % data['id'], data=jdata,
                               content_type='application/json')
        assert res.status_code == 200, res
        assert res.json['data']['title'] == data['title'], res.json
        assert res.json['data']['id'], res.json

    def test_update_invalid(self):
        self.login()
        res = self.client.get('/api/sources/%s' % self.source.id)
        data = res.json['data']
        data['title'] = 'H'
        jdata = json.dumps(data)
        res = self.client.post('/api/sources/%s' % data['id'], data=jdata,
                               content_type='application/json')
        assert res.status_code == 400, res
