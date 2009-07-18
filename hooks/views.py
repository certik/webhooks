import urllib
import urllib2
import pprint
import logging
import hashlib

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson

from models import User, Repository, RepoUpdate, Author
from google.appengine.ext import db

from google.appengine.api.labs import taskqueue

from utils import log_exception

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
        queue = taskqueue.Queue("github")
        task = taskqueue.Task(url="/hooks/worker/authors/",
                params={'repo': r.key()})
        queue.add(task)
        return HttpResponse("OK\n")

def users(request):
    l = User.objects.all()
    return render_to_response("hooks/users.html", {'users_list': l})

def user(request, user):
    u = User.get(db.Key(user))
    gravatar_id = hashlib.md5(u.email).hexdigest()
    default = "http://github.com/images/gravatars/gravatar-40.png"
    gravatar_url = "http://www.gravatar.com/avatar/%s?d=%s" % \
            (gravatar_id, urllib.quote(default, safe=""))
    return render_to_response("hooks/user.html", {'user': u,
        'gravatar_url': gravatar_url})

def repos(request):
    l = Repository.objects.all()
    return render_to_response("hooks/repos.html", {'repos_list': l})

def repo(request, repo):
    r = Repository.get(db.Key(repo))
    updates = RepoUpdate.gql("WHERE repo = :1", r)
    authors = Author.gql("WHERE repo = :1", r)
    return render_to_response("hooks/repo.html", {'repo': r,
        'updates': updates, 'authors': authors})

@log_exception
def worker_authors(request):
    r = Repository.get(db.Key(request.POST["repo"]))
    logging.info("processing repository: %s" % r.name)
    base_url = "http://github.com/%s/%s" % (r.owner.name, r.name)
    url = base_url + "/network_meta"
    logging.info("  downloading network_meta from: %s" % url)
    try:
        s = urllib2.urlopen(url).read()
    except urllib2.HTTPError:
        logging.info("Probably bad repo, skipping.")
        return HttpResponse("Probably bad repo, skipping.\n")
    logging.info("  network_meta loaded")
    try:
        data = simplejson.loads(s)
    except ValueError:
        logging.info("Probably bad repo, skipping.")
        return HttpResponse("Probably bad repo, skipping.\n")
    logging.info("  network_meta parsed")
    dates = data["dates"]
    nethash = data["nethash"]
    url = "%s/network_data_chunk?nethash=%s&start=0&end=%d" % (base_url,
            nethash, len(dates)-1)
    logging.info("  downloading commits from: %s" % url)
    s = urllib2.urlopen(url).read()
    logging.info("  parsing commits...")
    data = simplejson.loads(s, encoding="latin-1")
    logging.info("  processing authors...")
    commits = data["commits"]
    m = [(x["author"], x["id"]) for x in commits]
    m = dict(m)
    logging.info(m)
    authors = m.keys()
    authors = list(set(authors))
    authors.sort()
    logging.info(authors)
    queue = taskqueue.Queue("github")
    for author in authors:
        q = User.gql("WHERE name = :1", author)
        u = q.get()
        if u is None:
            u = User(name=author, email="None")
            u.save()
            task = taskqueue.Task(url="/hooks/worker/user_email/",
                    params={'user': u.key(), 'commit': m[u.name]})
            queue.add(task)
        q = Author.gql("WHERE user = :1 AND repo = :2", u, r)
        a = q.get()
        if a is None:
            a = Author(repo=r, user=u)
            a.save()
    logging.info("  done.")
    return HttpResponse("OK\n")
