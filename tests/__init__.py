from unittest import TestCase
from app import create_app, db


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
