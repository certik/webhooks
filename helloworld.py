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
        payload = simplejson.loads(self.request.body)
        logging.info("-"*40)
        logging.info(str(payload))
        for revision in payload["revisions"]:
            logging.info("Project %s, revision %s contains %s paths",
                payload["project_name"],
                revision["revision"],
                revision["path_count"])
        logging.info("-"*40)

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
