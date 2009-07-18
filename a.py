from django.utils import simplejson
import urllib2

s = urllib2.urlopen("http://github.com/certik/sympy/network_meta").read()
data = simplejson.loads(s)
dates = data["dates"]
nethash = data["nethash"]
print len(dates)
print nethash
base = "http://github.com/certik/sympy"
url = "%s/network_data_chunk?nethash=%s&start=0&end=%d" % (base, nethash,
        len(dates)-1)
print "downloading..."
s = urllib2.urlopen(url).read()
print "   done."
data = simplejson.loads(s, encoding="latin-1")
commits = data["commits"]
authors = [x["author"] for x in commits]
authors = list(set(authors))
authors.sort()
print authors
print len(authors)
