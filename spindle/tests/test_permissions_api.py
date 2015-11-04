import json

from loom.db import Collection, session
from spindle.model import Role
from spindle.tests.util import TestCase


class PermissionsApiTestCase(TestCase):

    def setUp(self):
        super(PermissionsApiTestCase, self).setUp()
        self.coll = Collection()
        self.coll.title = "Test Collection"
        session.add(self.coll)
        session.commit()

    def test_roles(self):
        res = self.client.get('/api/roles')
        assert res.json['total'] == 2, res.json
        assert len(res.json['results']) == 2, res.json
        res = Role.load_or_create('foo', Role.USER, 'Foo User')
        session.commit()
        res = self.client.get('/api/roles')
        assert res.json['total'] == 3, res.json
