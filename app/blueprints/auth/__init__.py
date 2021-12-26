from base64 import b64decode
from functools import wraps

from argon2.exceptions import InvalidHash
from flask import Blueprint, request, current_app, g
import jwt
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized

from app import password_hasher, db
from app.models.user import User as UserModel

bp = Blueprint('auth', __name__, url_prefix='/auth')


def add_user_to_request():
    g.current_user = None
    if authorization := request.headers.get('Authorization', None):
        token = b64decode(authorization, validate=True)
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=('HS256',))
        if user := UserModel.query.get(payload['uuid']):
            if user.login_counter == payload['login_counter']:
                g.current_user = user


before_hooks = [add_user_to_request]


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not g.current_user:
            raise Unauthorized
        return fn(*args, **kwargs)
    return wrapper


def make_user_jwt_token(user):
    if user:
        payload = {
                'uuid': user.uuid.hex(),
                'login_counter': user.login_counter,
                }
    else:
        payload = {
                'uuid': '',
                'login_counter': ''
                }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
    return None


@bp.route('/login', methods=('POST',))
def login():
    email = request.json.get('email')
    password_raw = request.json.get('password')
    user = UserModel.query.filter_by(email=email).one_or_none()
    hash_ = user.hash if user else ''
    token = make_user_jwt_token(user)
    try:
        password_hasher.verify(hash_, password_raw)
        return {'token': token}, 200
    except InvalidHash:
        pass
    raise Unauthorized('Login failed')


@bp.route('/register', methods=('POST',))
def register():
    email = request.json.get('email')
    password = request.json.get('password')
    hash_ = password_hasher.hash(password)
    db.session.add(UserModel(email=email, hash=hash_))
    try:
        db.session.commit()
    except IntegrityError:
        db.session.close()
    return '', 200
