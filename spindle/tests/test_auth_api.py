from spindle.tests.util import TestCase


class AuthApiTestCase(TestCase):

    def setUp(self):
        super(AuthApiTestCase, self).setUp()

    def test_session_logged_out(self):
        res = self.client.get('/api/session')
        assert not res.json.get('logged_in'), res.json
        assert not res.json.get('user'), res.json

    def test_session_logged_in(self):
        self.login()
        res = self.client.get('/api/session')
        assert res.json.get('logged_in'), res.json
        assert res.json.get('user'), res.json
