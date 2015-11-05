from spindle.core import get_loom_config
from spindle.tests.util import TestCase


class SearchApiTestCase(TestCase):

    def setUp(self):
        super(SearchApiTestCase, self).setUp()

    def test_basic_search(self):
        self.setUpFixtures()
        config = get_loom_config()
        assert len(config.types), len(config.types)

        res = self.client.get('/api/search')
        assert res.json['total'] == 0, res.json

        self.login()
        res = self.client.get('/api/search')
        assert res.json['total'] == 50, res.json

        res = self.client.get('/api/search?limit=4')
        assert len(res.json['results']) == 4, res.json

        res = self.client.get('/api/search?offset=46')
        assert len(res.json['results']) == 4, res.json

        res = self.client.get('/api/search?q=Hazim')
        assert res.json['total'] == 1, res.json['total']
        assert not res.json['facets'], res.json['total']

        res = self.client.get('/api/search?facet=jurisdiction_code')
        facets = res.json['facets']
        assert 'jurisdiction_code' in facets, facets
        jur = facets['jurisdiction_code']
        assert jur['values'][0]['key'] == 'BA', facets

        ORG = "https://schema.occrp.org/generic/organization.json#"
        res = self.client.get('/api/search?filter:$schema=' + ORG)
        assert res.json['total'] == 8, res.json['total']

        qs = '?filter:jurisdiction_code=BA&filter:$schema=' + ORG
        res = self.client.get('/api/search' + qs)
        assert res.json['total'] == 8, res.json['total']

        qs = '?filter:jurisdiction_code=GB&filter:$schema=' + ORG
        res = self.client.get('/api/search' + qs)
        assert res.json['total'] == 0, res.json['total']

    def test_search(self):
        res = self.client.get('/api/search')
        assert res.status_code == 200, res
        assert 'status' in res.json, res.json
        assert 'results' in res.json, res.json
