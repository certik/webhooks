from django.utils import simplejson
from django.test import TestCase

class SimpleTest(TestCase):
    def test_hooks(self):
        response = self.client.get('/hooks/')
        assert response.status_code == 200

    def test_index(self):
        response = self.client.get('/')
        assert response.status_code == 200

class HookTest(TestCase):
    def test_hook(self):
        d = {23: 23, "ok": 2}
        data = simplejson.dumps(d)
        response = self.client.post('/', {"payload": data})
        assert response.status_code == 200
        assert response.content == "OK\n"
