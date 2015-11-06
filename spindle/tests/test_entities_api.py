from loom.db import Collection, session
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
        session.commit()
        self.schema_uri = 'https://schema.occrp.org/generic/organization.json#'
        self.entity = {'id': 'foo', 'name': 'Foobar'}
        self.config.entities.save(self.schema_uri, self.entity,
                                  collection_id=self.coll.id)

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
        assert res.status_code == 404
