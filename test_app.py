import sys
import os
import urllib
import json
url = sys.argv[1]

d = {23: 23, "ok": 2}
data = json.dumps(d)
data = "payload=%s" % urllib.quote(data)
os.system('curl -d "%s" %s' % (data, url))
