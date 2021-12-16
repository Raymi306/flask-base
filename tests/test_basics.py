from .conftest import FlaskTestSuite


class TestOne(FlaskTestSuite):
    def test_heartbeat(self):
        with self.client as client:
            response = client.get('/heartbeat')
            self.assertEqual(b'up', response.data)

    def test_auth_stub(self):
        with self.client as client:
            response = client.get('/auth', headers={'Authorization': 'TEST'})
            self.assertEqual(200, response.status_code)
