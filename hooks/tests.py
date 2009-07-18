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
        d = {
                "commits": [{
                    "id": "984375209487abe",
                    "author": {
                        "name": "user1",
                        "email": "some@at.com"
                    }
                }, {
                    "id": "984375aaf209487abe",
                    "author": {
                        "name": "user3",
                        "email": "some3@at.com"
                    }
                }],
                "repository": {
                    "name": "testing_repo",
                    "owner": {
                        "name": "user3",
                        "email": "some3@at.com"
                    }
                 }
            }
        data = simplejson.dumps(d)
        response = self.client.post('/', {"payload": data})
        assert response.status_code == 200
        assert response.content == "OK\n"
