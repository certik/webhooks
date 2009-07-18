import sys
import os
import urllib
import json
url = sys.argv[1]

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
                "name": "user3",
                "email": "some3@at.com"
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
d3 = {u'after': u'6f4f8e4ec110c23eb2f2fb48363eb19af8f73ac1',
 u'before': u'bb8a111ad149cf775b9ac400391bb4e3759f25db',
 u'commits': [{u'added': [],
               u'author': {u'email': u'ondrej@certik.cz',
                           u'name': u'Ondrej Certik'},
               u'id': u'be1b010afc5a35d624dd2e53733f86ef6268bd9c',
               u'message': u'Fixes several typos in the docstrings\n\nLike indentation problems and similar.\n\nSigned-off-by: Ondrej Certik <ondrej@certik.cz>\nSigned-off-by: Aaron Meurer <asmeurer@gmail.com>',
               u'modified': [u'sympy/simplify/simplify.py'],
               u'removed': [],
               u'timestamp': u'2009-07-11T19:02:21-07:00',
               u'url': u'http://github.com/certik/sympy/commit/be1b010afc5a35d624dd2e53733f86ef6268bd9c'},
              {u'added': [],
               u'author': {u'email': u'ondrej@certik.cz',
                           u'name': u'Ondrej Certik'},
               u'id': u'6f4f8e4ec110c23eb2f2fb48363eb19af8f73ac1',
               u'message': u'SymPy logo: use a transparent background',
               u'modified': [u'doc/src/_static/sympylogo.png'],
               u'removed': [],
               u'timestamp': u'2009-07-12T09:39:06-07:00',
               u'url': u'http://github.com/certik/sympy/commit/6f4f8e4ec110c23eb2f2fb48363eb19af8f73ac1'}],
 u'ref': u'refs/heads/master',
 u'repository': {u'description': u"Ondrej's sympy development repo",
                 u'fork': False,
                 u'forks': 3,
                 u'homepage': u'',
                 u'name': u'sympy',
                 u'open_issues': 0,
                 u'owner': {u'email': u'ondrej@certik.cz',
                            u'name': u'certik'},
                 u'private': False,
                 u'url': u'http://github.com/certik/sympy',
                 u'watchers': 8}}

data = json.dumps(d1)
data = "payload=%s" % urllib.quote(data)
os.system('curl -d "%s" %s' % (data, url))
data = json.dumps(d2)
data = "payload=%s" % urllib.quote(data)
os.system('curl -d "%s" %s' % (data, url))
data = json.dumps(d3)
data = "payload=%s" % urllib.quote(data)
os.system('curl -d "%s" %s' % (data, url))
