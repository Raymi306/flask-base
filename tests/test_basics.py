from flask import g

from app.models.user import User as UserModel
from . import FlaskTestSuite


DEFAULT_EMAIL = 'test@test.tld'
DEFAULT_PWD = 'abcd1234'


def register(client, email=DEFAULT_EMAIL, password=DEFAULT_PWD):
    return client.post('/auth/register', json={'email': email, 'password': password})

def login(client, email=DEFAULT_EMAIL, password=DEFAULT_PWD):
    return client.post('/auth/login', json={'email': email, 'password': password})


class TestCore(FlaskTestSuite):
    def test_heartbeat(self):
        with self.client as client:
            response = client.get('/heartbeat')
            self.assertEqual(b'up', response.data)


class TestAuth(FlaskTestSuite):
    def test_register_normal(self):
        with self.client as client:
            with self.app.app_context():
                self.assertEqual(0, len(UserModel.query.all()))
                response = register(client)
                self.assertEqual(1, len(UserModel.query.all()))
                self.assertEqual(200, response.status_code)

    def test_register_duplicate(self):
        with self.client as client:
            with self.app.app_context():
                self.assertEqual(0, len(UserModel.query.all()))
                response = register(client)
                self.assertEqual(200, response.status_code)
                response = register(client)
                self.assertEqual(200, response.status_code)
                self.assertEqual(1, len(UserModel.query.all()))

    def test_login_normal(self):
        with self.client as client:
            register(client)
            response = login(client)
            self.assertEqual(200, response.status_code)

    def test_login_failure(self):
        with self.client as client:
            register(client)
            response = login(client, email='foo@bar.baz')
            self.assertEqual(401, response.status_code)
