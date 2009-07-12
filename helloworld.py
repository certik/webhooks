import base64
import urllib
import pprint
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import logging
from django.utils import simplejson

class MainPage(webapp.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')
        logging.info("get has been called")

    def post(self):
        payload = self.request.get("payload")
        payload = urllib.unquote(payload)
        payload = simplejson.loads(payload)
        logging.info("-"*40 + "\n" + pprint.pformat(payload) + "\n" + "-"*40)

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
