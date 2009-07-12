import sys
url = sys.argv[1]

import os
data = "birthyear=1905&press=%20OK%20"
os.system('curl -d "%s" %s' % (data, url))
