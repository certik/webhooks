from django.utils import simplejson
from django.test import TestCase

d1 = {
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
            "name": "user4",
            "email": "some4@at.com"
        }
     }
}

d2 = {
  "before": "5aef35982fb2d34e9d9d4502f6ede1072793222d",
  "repository": {
    "url": "http://github.com/defunkt/github",
    "name": "github",
    "description": "You're lookin' at it.",
    "watchers": 5,
    "forks": 2,
    "private": 1,
    "owner": {
      "email": "chris@ozmm.org",
      "name": "defunkt"
    }
  },
  "commits": [
    {
      "id": "41a212ee83ca127e3c8cf465891ab7216a705f59",
      "url": "http://github.com/defunkt/github/commit/41a212ee83ca127e3c8cf465891ab7216a705f59",
      "author": {
        "email": "chris@ozmm.org",
        "name": "Chris Wanstrath"
      },
      "message": "okay i give in",
      "timestamp": "2008-02-15T14:57:17-08:00",
      "added": ["filepath.rb"]
    },
    {
      "id": "de8251ff97ee194a289832576287d6f8ad74e3d0",
      "url": "http://github.com/defunkt/github/commit/de8251ff97ee194a289832576287d6f8ad74e3d0",
      "author": {
        "email": "chris@ozmm.org",
        "name": "Chris Wanstrath"
      },
      "message": "update pricing a tad",
      "timestamp": "2008-02-15T14:36:34-08:00"
    }
  ],
  "after": "de8251ff97ee194a289832576287d6f8ad74e3d0",
  "ref": "refs/heads/master"
}

class SimpleTest(TestCase):
    def test_hooks(self):
        response = self.client.get('/hooks/')
        assert response.status_code == 200

    def test_index(self):
        response = self.client.get('/')
        assert response.status_code == 200

class HookTest(TestCase):
    def test_hook(self):
        data = simplejson.dumps(d1)
        response = self.client.post('/', {"payload": data})
        assert response.status_code == 200
        assert response.content == "OK\n"

        response = self.client.get('/hooks/users/')
        assert response.status_code == 200
        users_list = response.context["users_list"]
        assert len(list(users_list)) == 1
        assert users_list[0].name == "user4"
        assert users_list[0].email == "some4@at.com"
        key = users_list[0].key()
        response = self.client.get('/hooks/users/%s/' % key)
        assert response.status_code == 200
        user = response.context["user"]
        assert user.name == "user4"
        assert user.email == "some4@at.com"

        response = self.client.get('/hooks/repos/')
        assert response.status_code == 200
        repos_list = response.context["repos_list"]
        assert len(list(repos_list)) == 1
        assert repos_list[0].name == "testing_repo"
        assert repos_list[0].owner.name == "user4"
        assert repos_list[0].owner.email == "some4@at.com"

    def test_hook2(self):
        data = simplejson.dumps(d2)
        response = self.client.post('/', {"payload": data})
        assert response.status_code == 200
        assert response.content == "OK\n"

        response = self.client.get('/hooks/users/')
        assert response.status_code == 200
        users_list = response.context["users_list"]
        assert len(list(users_list)) == 1
        assert users_list[0].name == "defunkt"
        assert users_list[0].email == "chris@ozmm.org"

    def test_users1(self):
        data = simplejson.dumps(d1)
        response = self.client.post('/', {"payload": data})
        assert response.status_code == 200
        assert response.content == "OK\n"

        data = simplejson.dumps(d2)
        response = self.client.post('/', {"payload": data})
        assert response.status_code == 200
        assert response.content == "OK\n"

        response = self.client.get('/hooks/users/')
        assert response.status_code == 200
        users_list = response.context["users_list"]
        assert len(list(users_list)) == 2
        assert users_list[0].name == "user4"
        assert users_list[0].email == "some4@at.com"
        assert users_list[1].name == "defunkt"
        assert users_list[1].email == "chris@ozmm.org"

    def test_users2(self):
        data = simplejson.dumps(d1)
        response = self.client.post('/', {"payload": data})
        assert response.status_code == 200
        assert response.content == "OK\n"

        data = simplejson.dumps(d1)
        response = self.client.post('/', {"payload": data})
        assert response.status_code == 200
        assert response.content == "OK\n"

        response = self.client.get('/hooks/users/')
        assert response.status_code == 200
        users_list = response.context["users_list"]
        assert len(list(users_list)) == 1
        assert users_list[0].name == "user4"
        assert users_list[0].email == "some4@at.com"

    def test_users3(self):
        data = simplejson.dumps(d2)
        response = self.client.post('/', {"payload": data})
        assert response.status_code == 200
        assert response.content == "OK\n"

        data = simplejson.dumps(d2)
        response = self.client.post('/', {"payload": data})
        assert response.status_code == 200
        assert response.content == "OK\n"

        response = self.client.get('/hooks/users/')
        assert response.status_code == 200
        users_list = response.context["users_list"]
        assert len(list(users_list)) == 1
        assert users_list[0].name == "defunkt"
        assert users_list[0].email == "chris@ozmm.org"

    def test_repos1(self):
        data = simplejson.dumps(d1)
        response = self.client.post('/', {"payload": data})
        assert response.status_code == 200
        assert response.content == "OK\n"

        data = simplejson.dumps(d2)
        response = self.client.post('/', {"payload": data})
        assert response.status_code == 200
        assert response.content == "OK\n"

        response = self.client.get('/hooks/repos/')
        assert response.status_code == 200
        repos_list = response.context["repos_list"]
        assert len(list(repos_list)) == 2
        assert repos_list[0].name == "testing_repo"
        assert repos_list[0].owner.name == "user4"
        assert repos_list[0].owner.email == "some4@at.com"
        assert repos_list[1].name == "github"
        assert repos_list[1].owner.name == "defunkt"
        assert repos_list[1].owner.email == "chris@ozmm.org"
