import urllib
import pprint
import logging

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson

from models import User

def index(request):
    if request.method == 'GET':
        return render_to_response("hooks/index.html")
    elif request.method == 'POST':
        payload = request.POST["payload"]
        payload = urllib.unquote(payload)
        payload = simplejson.loads(payload)
        logging.info("-"*40 + "\n" + pprint.pformat(payload) + "\n" + "-"*40)
        repository = payload["repository"]
        owner = repository["owner"]
        u = User(name=owner["name"], email=owner["email"])
        u.save()
        return HttpResponse("OK\n")

def users(request):
    l = User.objects.all()
    #l = [{"name": "ok", "email": "em"}, {"name": "ok2"}]
    return render_to_response("hooks/users.html", {'users_list': l})
