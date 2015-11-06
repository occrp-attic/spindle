from flask import request, Blueprint, session, redirect
from flask_oauthlib.client import OAuthException
from apikit import jsonify

from loom.db import session as db_session
from spindle import authz
from spindle.model import Role
from spindle.core import oauth_provider
from spindle.util import url_for

auth_api = Blueprint('auth', __name__)


@oauth_provider.tokengetter
def get_oauth_token():
    if 'oauth' in session:
        sig = session.get('oauth')
        return (sig.get('access_token'), '')


@auth_api.before_app_request
def load_user():
    request.auth_roles = session.get('roles', [Role.SYSTEM_GUEST])
    request.auth_user = session.get('user')
    request.auth_admin = session.get('is_admin', False)
    request.logged_in = request.auth_user is not None
    authz.request_resources()


@auth_api.route('/api/session')
def get_session():
    return jsonify({
        'logged_in': request.logged_in,
        'user': Role.load(request.auth_user),
        'roles': list(request.auth_roles),
        'login_uri': url_for('auth.authorize'),
        'sources': request.authz_sources,
        'collections': request.authz_collections
    })


@auth_api.route('/auth/authorize')
def authorize():
    return oauth_provider.authorize(callback=url_for('auth.callback'))


@auth_api.route('/auth/reset')
def reset():
    authz.require(authz.logged_in())
    session.clear()
    return redirect(url_for('base.index'))


@auth_api.route('/auth/callback')
def callback():
    next_url = url_for('base.index')
    resp = oauth_provider.authorized_response()
    if resp is None or isinstance(resp, OAuthException):
        # FIXME: notify the user, somehow.
        return redirect(next_url)
    session['oauth'] = resp
    # This is ugly, but useful for debugging and non-OCCRP users.
    session['roles'] = [Role.SYSTEM_GUEST, Role.SYSTEM_USER]
    if 'googleapis.com' in oauth_provider.base_url:
        me = oauth_provider.get('userinfo')
        user_id = 'google:%s' % me.data.get('id')
        role = Role.load_or_create(user_id, Role.USER, me.data.get('name'),
                                   email=me.data.get('email'))
    elif 'occrp.org' in oauth_provider.base_url or \
            'investigativedashboard.org' in oauth_provider.base_url:
        me = oauth_provider.get('api/2/accounts/profile/')
        user_id = 'idashboard:user:%s' % me.data.get('id')
        role = Role.load_or_create(user_id, Role.USER,
                                   me.data.get('display_name'),
                                   email=me.data.get('email'),
                                   is_admin=me.data.get('is_admin'))
        for group in me.data.get('groups', []):
            group_id = 'idashboard:%s' % group.get('id')
            Role.load_or_create(group_id, Role.GROUP, group.get('name'))
            session['roles'].append(group_id)
    else:
        raise RuntimeError("Unknown OAuth URL: %r" % oauth_provider.base_url)
    session['roles'].append(user_id)
    session['user'] = role.id
    session['is_admin'] = role.is_admin
    db_session.commit()
    return redirect(next_url)
