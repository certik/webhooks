import urllib
import pprint
import logging

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson

from models import User, Repository, RepoUpdate
from google.appengine.ext import db

def index(request):
    if request.method == 'GET':
        return render_to_response("hooks/index.html")
    elif request.method == 'POST':
        payload = request.POST["payload"]
        payload = urllib.unquote(payload)
        payload = simplejson.loads(payload)
        #logging.info("-"*40 + "\n" + pprint.pformat(payload) + "\n" + "-"*40)
        repository = payload["repository"]
        owner = repository["owner"]
        q = User.gql("WHERE email = :1", owner["email"])
        u = q.get()
        if u is None:
            u = User(name=owner["name"], email=owner["email"])
            u.save()
        q = Repository.gql("WHERE name = :1 AND owner = :2",
                repository["name"], u)
        r = q.get()
        if r is None:
            r = Repository(name=repository["name"], owner=u)
            r.save()
        u = RepoUpdate(repo=r, update=pprint.pformat(payload))
        u.save()
        return HttpResponse("OK\n")

def users(request):
    l = User.objects.all()
    return render_to_response("hooks/users.html", {'users_list': l})

def user(request, user):
    u = User.get(db.Key(user))
    return render_to_response("hooks/user.html", {'user': u})

def repos(request):
    l = Repository.objects.all()
    return render_to_response("hooks/repos.html", {'repos_list': l})

def repo(request, repo):
    r = Repository.get(db.Key(repo))
    updates = RepoUpdate.gql("WHERE repo = :1", r)
    return render_to_response("hooks/repo.html", {'repo': r,
        'updates': updates})
