import os
import tempfile

from unittest import TestCase
from app import create_app, db


class FlaskTestSuite(TestCase):

    def setUp(self):
        db_fd, db_path = tempfile.mkstemp()
        app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': f'sqlite:////{db_path}',
            })
        self.app = app
        with app.app_context():
            db.create_all()
        self.client = app.test_client()

    def teardown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

def create_user(details, password):
    from app.models.app_user import User
    from argon2 import PasswordHasher
    hasher = PasswordHasher()
    hash_ = hasher.hash(password)
    details.setdefault('email', 'test@test.tld')
    user = User(**details, hash=_hash)
