import sys
import os
import urllib
import json
url = sys.argv[1]

d = {
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
data = json.dumps(d)
data = "payload=%s" % urllib.quote(data)
os.system('curl -d "%s" %s' % (data, url))
