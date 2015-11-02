from spindle.tests.util import TestCase


class EntitiesApiTestCase(TestCase):

    def setUp(self):
        super(EntitiesApiTestCase, self).setUp()
        self.schema_uri = 'https://schema.occrp.org/generic/organization.json#'
        self.entity = {'id': 'foo', 'name': 'Foobar'}
        self.config.entities.save(self.schema_uri, self.entity, 'test_source')

    def test_view(self):
        res = self.client.get('/api/entities/foo')
        assert res.status_code == 200
        data = res.json['data']
        assert 'name' in data, data
        assert data['name'] == 'Foobar', data

    def test_view_not_found(self):
        res = self.client.get('/api/entities/foobar')
        assert res.status_code == 404
