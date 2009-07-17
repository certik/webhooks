import urllib
import pprint
from django.http import HttpResponse
from django.utils import simplejson

def index(request):
    if request.method == 'GET':
        return HttpResponse("Hooks.")
    elif request.method == 'POST':
        payload = request.POST["payload"]
        payload = urllib.unquote(payload)
        payload = simplejson.loads(payload)
        #logging.info("-"*40 + "\n" + pprint.pformat(payload) + "\n" + "-"*40)
        print("-"*40 + "\n" + pprint.pformat(payload) + "\n" + "-"*40)
        return HttpResponse("OK\n")
