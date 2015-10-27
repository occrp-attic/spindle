from flask import jsonify, request, Blueprint
from flask import session, redirect

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
    request.user_id = session.get('user_id')
    request.logged_in = request.user_id is not None
    request.user = session.get('user', {})


@auth_api.route('/api/session')
def get_session():
    return jsonify({
        'logged_in': request.logged_in,
        'user_id': request.user_id,
        'user': request.user,
        'login_uri': url_for('auth.authorize')
    })


@auth_api.route('/auth/authorize')
def authorize():
    return oauth_provider.authorize(callback=url_for('auth.callback'))


@auth_api.route('/auth/callback')
def callback():
    next_url = url_for('base.index')
    resp = oauth_provider.authorized_response()
    if resp is None:
        # FIXME: notify the user, somehow.
        return redirect(next_url)
    session['oauth'] = resp
    me = oauth_provider.get('userinfo')
    session['user'] = me.data
    session['user_id'] = 'google:%s' % me.data.get('id')
    return redirect(next_url)
