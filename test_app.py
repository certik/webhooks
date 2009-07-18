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
data = json.dumps(d1)
data = "payload=%s" % urllib.quote(data)
os.system('curl -d "%s" %s' % (data, url))
data = json.dumps(d2)
data = "payload=%s" % urllib.quote(data)
os.system('curl -d "%s" %s' % (data, url))
