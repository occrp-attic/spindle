from loom.db import Collection, session
from spindle.tests.util import TestCase


class CollectionsApiTestCase(TestCase):

    def setUp(self):
        super(CollectionsApiTestCase, self).setUp()
        self.coll = Collection()
        self.coll.title = "Test Collection"
        session.add(self.coll)
        session.commit()

    def test_index(self):
        res = self.client.get('/api/collections')
        assert res.status_code == 200
        assert res.json['total'] == 1, res.json

    def test_view(self):
        res = self.client.get('/api/collections/%s' % self.coll.id)
        assert res.status_code == 200
        data = res.json['data']
        assert data['title'] == self.coll.title

    def test_view_not_found(self):
        res = self.client.get('/api/collections/8388')
        assert res.status_code == 404
