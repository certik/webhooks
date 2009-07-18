from django.test import TestCase

class SimpleTest(TestCase):
    def test_hooks(self):
        response = self.client.get('/hooks/')
        assert response.status_code == 200

    def test_index(self):
        response = self.client.get('/')
        assert response.status_code == 200
