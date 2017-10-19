#!/usr/bin/python

from __future__ import print_function
import sys,json,urllib, urllib2, requests
import requests


f1 = open('bloomoutput.json','w')
f2 = open('bloomoutputhuman.txt','w')

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
    j = json.dumps(item, indent=4, sort_keys=True)
    print(j, file=f2)
    result.append(item)
print(json.dumps(result),file=f1)

f1.close()
f2.close()
