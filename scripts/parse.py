#1/usr/bin/python


import sys,json,urllib, urllib2, requests
import requests



count = 0
f = open(sys.argv[1])
s = f.read()
d = json.loads(s)
f.close()
for item in d: 
    req = urllib2.Request('http://localhost:5005/findBloomPaths')
    req.add_header('Content-Type', 'application/json')
    print json.dumps(item['ES_content']).decode('string_escape')[1:-1]
    response = urllib2.urlopen(req, json.dumps(item['ES_content']).decode('string_escape')[1:-1])
    item['response'] = response.read()
    print json.dumps(item, indent=4, sort_keys=True)
