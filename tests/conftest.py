import os
import tempfile

from unittest import TestCase
from app import create_app, password_hasher, db
from app.models.user import User


class FlaskTestSuite(TestCase):

    def setUp(self):
        app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': f'sqlite://',
            })
        self.app = app
        with self.app.app_context():
            db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()

    def create_user(self, details=None, password='abcd1234'):
        hash_ = password_hasher.hash(password)
        if not details:
            details = {}
        details.setdefault('email', 'test@test.tld')
        user = User(**details, hash=hash_)
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
            result = user.uuid
        return result

    def get_user(self, uuid):
        with self.app.app_context():
            return User.query.get(uuid)
