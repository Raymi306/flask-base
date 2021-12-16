from functools import wraps

from argon2 import PasswordHasher
from flask import Blueprint, request, g
from werkzeug.exceptions import Unauthorized

bp = Blueprint('auth', __name__, url_prefix='/auth')


def add_user_to_request():
    g.current_user = None
    if authorization := request.headers.get('Authorization', None):
        g.current_user = authorization


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not g.current_user:
            raise Unauthorized()
        else:
            return fn(*args, **kwargs)
    return wrapper


before_hooks = [add_user_to_request]


@bp.route('', methods=('GET',))
@login_required
def stub():
    return '', 200

@bp.route('/register', methods=('POST',))
def register():
    username = request.json.get(['foo'])
    password = request.json.get(['bar'])
    hash_ = PasswordHasher(password)
    return '', 200
