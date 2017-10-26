#!/usr/bin/python

from __future__ import print_function
import math
import json,sys


f = open(sys.argv[1])
s = f.read()
f.close()

d = json.loads(s)
f = open('../data/improveddata.txt','w')

finalresults = []

for item in d:
    newitem = {}
    newitem['ES_content'] = []
    nodestats = json.loads(item['response'])
    for l in item['ES_content']:
        ldict = {}
        for k,v in l.iteritems():
            if k == 'label':
                ldict['label'] = v
                continue
            larr=[]
            for uriset in v:
                del uriset['score']
                if uriset['uri'] in item['correct']:
                    uriset['correctlabel'] = 1
                    uriset['connections'] = nodestats['correctnodestats'][uriset['uri']]['connections']
                    uriset['sumofhops'] = nodestats['correctnodestats'][uriset['uri']]['sumofhops']
                    uriset['elasticsearchscore'] = nodestats['correctnodestats'][uriset['uri']]['elasticsearchscore']
                else:
                    uriset['correctlabel'] = 0
                    uriset['connections'] = nodestats['incorrectnodestats'][uriset['uri']]['connections']
                    uriset['sumofhops'] = nodestats['incorrectnodestats'][uriset['uri']]['sumofhops']
                    uriset['elasticsearchscore'] = nodestats['incorrectnodestats'][uriset['uri']]['elasticsearchscore']
                larr.append(uriset)
            ldict[k] = larr
        newitem['ES_content'].append(ldict)
    finalresults.append(newitem)
print(json.dumps(finalresults), file = f)

f.close()
