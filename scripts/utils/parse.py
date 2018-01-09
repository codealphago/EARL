#!/usr/bin/python

from __future__ import print_function
import sys,json,urllib, urllib2, requests
import requests

f1 = open('output.json','w')

result = []
count = 0
f = open(sys.argv[1])
s = f.read()
d = json.loads(s)
f.close()

for item in d: 
    try:
        req = urllib2.Request('http://localhost:5000/processQuery')
        req.add_header('Content-Type', 'application/json')
        inputjson = {'nlquery': item['question']}
        response = urllib2.urlopen(req, json.dumps(inputjson))
        response = json.loads(response.read())
        result.append(response)
        print(count, len(d))
        count += 1
    except Exception,e:
        print("Error: ",e,item['question'])
        result.append({})
        count += 1

print(json.dumps(result),file=f1)
f1.close()

