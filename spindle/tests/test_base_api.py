from spindle.tests.util import TestCase


class BaseApiTestCase(TestCase):

    def setUp(self):
        super(BaseApiTestCase, self).setUp()

    def test_index(self):
        res = self.client.get('/')
        assert res.status_code == 200, res
        assert '<title>' in res.data, res.data
        assert 'ng-view' in res.data, res.data
