import os
import urllib
import urllib2
import pprint
import logging
import hashlib

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.core.urlresolvers import reverse

from models import User, Repository, RepoUpdate, Author
from google.appengine.ext import db

from google.appengine.api.labs import taskqueue

from utils import log_exception

def get_github_queue():
    # For some reason, the "github" queue doesn't work when testing, so we need
    # to use the "default" queue for tests:
    if "WEBHOOKS_TESTS" in os.environ and \
            os.environ['WEBHOOKS_TESTS'] == "yes":
        queue = taskqueue.Queue("default")
    else:
        queue = taskqueue.Queue("github")
    return queue

def create_repository_and_owner(repository, name, email):
    if email == "None":
        q = User.gql("WHERE name = :1", name)
    else:
        q = User.gql("WHERE email = :1", email)
    u = q.get()
    if u is None:
        u = User(name=name, email=email)
        u.save()
    q = Repository.gql("WHERE name = :1 AND owner = :2", repository, u)
    r = q.get()
    if r is None:
        r = Repository(name=repository, owner=u)
        r.save()
    queue = get_github_queue()
    task = taskqueue.Task(url="/hooks/worker/authors/",
            params={'repo': r.key()})
    queue.add(task)
    return r, u

def get_gravatar_url(email):
    gravatar_id = hashlib.md5(email).hexdigest()
    default = "http://github.com/images/gravatars/gravatar-40.png"
    gravatar_url = "http://www.gravatar.com/avatar/%s?d=%s" % \
            (gravatar_id, urllib.quote(default, safe=""))
    return gravatar_url

def index(request):
    if request.method == 'GET':
        return render_to_response("hooks/index.html",
                {"main_active": "active"})
    elif request.method == 'POST':
        payload = request.POST["payload"]
        payload = urllib.unquote(payload)
        payload = simplejson.loads(payload)
        #logging.info("-"*40 + "\n" + pprint.pformat(payload) + "\n" + "-"*40)
        repository = payload["repository"]
        owner = repository["owner"]
        r, u = create_repository_and_owner(repository["name"],
                owner["name"], owner["email"])
        u = RepoUpdate(repo=r, update=pprint.pformat(payload))
        u.save()
        return HttpResponse("OK\n")

def users(request):
    l = User.objects.all()
    a = []
    for u in l:
        a.append({"name": u.name, "email": u.email, "key": u.key(),
            "gravatar_url": get_gravatar_url(u.email)})
    return render_to_response("hooks/users.html", {'users_list': a,
        "users_active": "active"})

def user(request, user):
    u = User.get(db.Key(user))
    return render_to_response("hooks/user.html", {'user': u,
        'gravatar_url': get_gravatar_url(u.email)})

def repos(request):
    l = Repository.objects.all()
    return render_to_response("hooks/repos.html", {'repos_list': l,
        "repos_active": "active"})

def repo_add(request):
    repo = request.POST["repo"]
    owner_name = request.POST["owner"]
    r, u = create_repository_and_owner(repo, owner_name, "None")
    return HttpResponseRedirect(reverse('hooks.views.repo', args=(r.key(),)))

def repo_delete(request, repo):
    r = Repository.get(db.Key(repo))
    r.delete()
    return HttpResponseRedirect(reverse('hooks.views.repos'))

def repo(request, repo):
    r = Repository.get(db.Key(repo))
    repo_url = "http://github.com/%s/%s" % (r.owner.name, r.name)
    updates = RepoUpdate.gql("WHERE repo = :1", r)
    authors = Author.gql("WHERE repo = :1", r)
    a = []
    for author in authors:
        u = author.user
        a.append({"name": u.name, "email": u.email, "key": u.key(),
            "gravatar_url": get_gravatar_url(u.email)})
    return render_to_response("hooks/repo.html", {'repo': r,
        'repo_url': repo_url, 'updates': updates, 'authors': a})

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
    queue = get_github_queue()
    for author in authors:
        q = User.gql("WHERE name = :1", author)
        u = q.get()
        if u is None:
            u = User(name=author, email="None")
            u.save()
            task = taskqueue.Task(url="/hooks/worker/user_email/",
                    params={'user': u.key(),
                        'r_user_id': r.owner.name,
                        'r_repository': r.name,
                        'r_sha': m[u.name]
                        })
            queue.add(task)
        q = Author.gql("WHERE user = :1 AND repo = :2", u, r)
        a = q.get()
        if a is None:
            a = Author(repo=r, user=u)
            a.save()
    logging.info("  done.")
    return HttpResponse("OK\n")

@log_exception
def worker_email(request):
    u = User.get(db.Key(request.POST["user"]))
    r_user_id = request.POST["r_user_id"]
    r_repository = request.POST["r_repository"]
    r_sha = request.POST["r_sha"]
    logging.info("processing email for: %s" % u.name)
    base_url = "http://github.com/api/v2/json/commits/show/%s/%s" % (r_user_id, r_repository)
    url = base_url + "/%s" % r_sha
    logging.info("  downloading commit from: %s" % url)
    s = urllib2.urlopen(url).read()
    data = simplejson.loads(s, encoding="latin-1")
    author = data["commit"]["author"]
    logging.info(author)
    #assert author["name"] == u.name
    u.email = author["email"]
    u.put()
    logging.info("done")
    return HttpResponse("OK\n")
