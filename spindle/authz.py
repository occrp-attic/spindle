from flask import request
from werkzeug.exceptions import Forbidden

GROUP_GUEST = 'guest'
GROUP_USER = 'user'


def is_user():
    return GROUP_USER in request.authz_groups


def require(pred):
    if not pred:
        raise Forbidden("Sorry, you're not permitted to do this!")
