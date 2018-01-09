#!/usr/bin/python

from __future__ import print_function
import sys,json,urllib, urllib2, requests
import requests

result = []
count = 0
f = open(sys.argv[1])
s = f.read()
d = json.loads(s)
f.close()
lcqgold = []
earltest = []

for item in d: 
    itarr = []
    for ent in item['entity mapping']:
        itarr.append(ent['uri'])
    for pred in item['predicate mapping']:
        itarr.append(pred['uri'])
    lcqgold.append(itarr)

f = open(sys.argv[2])
s = f.read()
d = json.loads(s)
for item in d:
    itarr = []
    if 'entities' in item:
        if len(item['entities']) > 0:
            for ent in item['entities']:
                itarr.append(ent['uris'][0]['uri'][0])
    if 'relations' in item:
        if len(item['relations']) > 0:
            for rel in item['relations']:
                itarr.append(rel['uris'][0]['uri'][0])
    earltest.append(itarr)
f.close()


correct = 0
wrong = 0
total = 0
for idx,arr in enumerate(lcqgold):
    print (lcqgold[idx],earltest[idx])
    for uri in arr:
        if '/resource/' in uri:
            if uri in earltest[idx]:
                correct += 1
            else:
                wrong += 1
            total += 1

print(correct/float(total))

