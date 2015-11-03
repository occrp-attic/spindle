from flask import request, Blueprint, session, redirect
from apikit import jsonify

from loom.db import session as db_session
from spindle.model import Role
from spindle.core import oauth_provider
from spindle.util import url_for

# TODO: support OAuth against ID
auth_api = Blueprint('auth', __name__)


@oauth_provider.tokengetter
def get_oauth_token():
    if 'oauth' in session:
        sig = session.get('oauth')
        return (sig.get('access_token'), '')


@auth_api.before_app_request
def load_user():
    request.auth_roles = session.get('roles', [Role.SYSTEM_GUEST])
    request.auth_user = session.get('user', {})
    request.logged_in = request.auth_user is not None


@auth_api.route('/api/session')
def get_session():
    return jsonify({
        'logged_in': request.logged_in,
        'user': Role.load(request.auth_user),
        'roles': list(request.auth_roles),
        'login_uri': url_for('auth.authorize')
    })


@auth_api.route('/auth/authorize')
def authorize():
    return oauth_provider.authorize(callback=url_for('auth.callback'))


@auth_api.route('/auth/reset')
def reset():
    session.clear()
    return redirect(url_for('base.index'))


@auth_api.route('/auth/callback')
def callback():
    next_url = url_for('base.index')
    resp = oauth_provider.authorized_response()
    if resp is None:
        # FIXME: notify the user, somehow.
        return redirect(next_url)
    session['oauth'] = resp
    me = oauth_provider.get('userinfo')
    user_id = 'google:%s' % me.data.get('id')
    Role.load_or_create(user_id, Role.USER, me.data.get('name'),
                        email=me.data.get('email'))
    session['roles'] = [Role.SYSTEM_GUEST, Role.SYSTEM_USER, user_id]
    session['user'] = user_id
    db_session.commit()
    return redirect(next_url)
