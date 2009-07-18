from django.test import TestCase

class SimpleTest(TestCase):
    def test_hooks(self):
        response = self.client.get('/hooks/')
        self.failUnlessEqual(response.status_code, 200)

    def test_index(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)
