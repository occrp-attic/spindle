import json

from loom.db import Collection, session
from spindle.model import Role, Permission
from spindle.tests.util import TestCase


class PermissionsApiTestCase(TestCase):

    def setUp(self):
        super(PermissionsApiTestCase, self).setUp()
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
        session.flush()
        session.commit()

    def test_roles(self):
        res = self.client.get('/api/roles')
        assert res.json['total'] == 3, res.json
        assert len(res.json['results']) == 3, res.json
        res = Role.load_or_create('foo', Role.USER, 'Foo User')
        session.commit()
        res = self.client.get('/api/roles')
        assert res.json['total'] == 4, res.json

    def test_collection_permissions(self):
        url = '/api/collections/%s/permissions' % self.coll.id
        res = self.client.get(url)
        assert res.status_code == 403, res
        self.login()
        res = self.client.get(url)
        assert res.status_code == 200, res
        assert res.json['total'] == 1, res.json

    def test_update_permissions(self):
        coll_url = '/api/collections/%s' % self.coll.id
        url = coll_url + '/permissions'
        # check guest cannot access this collection
        res = self.client.get(coll_url)
        assert res.status_code == 403, res
        data = json.dumps({'role': Role.SYSTEM_GUEST,
                           'read': True, 'write': True})
        res = self.client.post(url, data=data,
                               content_type='application/json')
        assert res.status_code == 403, res
        self.login()
        res = self.client.post(url, data=data,
                               content_type='application/json')
        assert res.status_code == 200, res
        assert res.json['updated'], res.json
        self.client.get('/auth/reset')
        res = self.client.get(coll_url)
        assert res.status_code == 200, res

    def test_update_permissions_invalid_role(self):
        url = '/api/collections/%s/permissions' % self.coll.id
        self.login()
        data = json.dumps({'role': 'gnaaaa',
                           'read': True, 'write': True})
        res = self.client.post(url, data=data,
                               content_type='application/json')
        assert res.status_code == 400, res
        data = json.dumps({'role': Role.SYSTEM_USER,
                           'read': True})
        assert res.status_code == 400, res
