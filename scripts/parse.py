#1/usr/bin/python


import sys,json,urllib, urllib2, requests
import requests


result = []
count = 0
f = open(sys.argv[1])
s = f.read()
d = json.loads(s)
f.close()
for item in d: 
    req = urllib2.Request('http://localhost:5005/findBloomPaths')
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(item))
    item['response'] = response.read()
    result.append(item)
print json.dumps(result)
