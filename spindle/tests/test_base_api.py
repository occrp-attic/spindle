from spindle.tests.util import TestCase


class BaseApiTestCase(TestCase):

    def setUp(self):
        super(BaseApiTestCase, self).setUp()

    def test_index(self):
        res = self.client.get('/')
        assert res.status_code == 200, res
        assert '<title>' in res.data, res.data
        assert 'ng-view' in res.data, res.data

    def test_metadata(self):
        res = self.client.get('/api/metadata')
        assert res.status_code == 200, res
        assert 'schemas' in res.json, res.json
        assert 'sources' in res.json, res.json
        assert 'countries' in res.json, res.json
        countries = res.json['countries']
        assert 'AR' in countries, countries
        assert countries['AR']['title'] == 'Argentina', countries

    def test_search(self):
        res = self.client.get('/api/search')
        assert res.status_code == 200, res
        assert 'status' in res.json, res.json
        assert 'results' in res.json, res.json
