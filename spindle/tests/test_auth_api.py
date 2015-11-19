from spindle.tests.util import TestCase
from loom.db import Collection, session


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

    def test_header_login(self):
        role = self.create_user()
        session.refresh(role)
        headers = {'Authorization': 'apikey foo'}
        res = self.client.get('/api/session', headers=headers)
        assert not res.json.get('logged_in'), res.json
        assert not res.json.get('user'), res.json

        headers = {'Authorization': 'apikey %s' % role.apikey}
        res = self.client.get('/api/session', headers=headers)
        assert res.json.get('logged_in'), res.json
        assert res.json['user']['id'] == role.id, res.json

    def test_admin_all_access(self):
        self.setUpFixtures()
        self.coll = Collection()
        self.coll.title = "Test Collection"
        session.add(self.coll)
        session.commit()
        res = self.client.get('/api/session')
        assert not len(res.json['sources']['write']), res.json
        assert not len(res.json['collections']['write']), res.json
        self.login(id='admin', is_admin=True)
        res = self.client.get('/api/session')
        assert len(res.json['sources']['write']), res.json
        assert len(res.json['collections']['write']), res.json
