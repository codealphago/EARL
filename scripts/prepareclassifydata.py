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
    numoflists = len(item['correct'])
    for l in item['ES_content']:
        ldict = {}
        for k,v in l.iteritems():
            if k == 'label':
                ldict['label'] = v
                continue
            larr=[]
            for uriset in v:
                if uriset['uri'] in item['correct']:
                    uriset['correctlabel'] = 1
                    uriset['connections'] = (nodestats['correctnodestats'][uriset['uri']]['connections'])/float(numoflists)
                    uriset['sumofhops'] = (nodestats['correctnodestats'][uriset['uri']]['sumofhops'])/float(numoflists)
                    uriset['pathlength'] = (nodestats['correctnodestats'][uriset['uri']]['pathlength'])/float(math.pow(15,numoflists))
                    uriset['sumhopspath'] = (nodestats['correctnodestats'][uriset['uri']]['sumhopspath'])/float(math.pow(15,numoflists))
                    uriset['elasticsearchscore'] = nodestats['correctnodestats'][uriset['uri']]['elasticsearchscore']
                else:
                    uriset['correctlabel'] = 0
                    uriset['connections'] = (nodestats['incorrectnodestats'][uriset['uri']]['connections'])/float(numoflists)
                    uriset['sumofhops'] = (nodestats['incorrectnodestats'][uriset['uri']]['sumofhops'])/float(numoflists)
                    uriset['pathlength'] = (nodestats['incorrectnodestats'][uriset['uri']]['pathlength'])/float(math.pow(15,numoflists))
                    uriset['sumhopspath'] = (nodestats['incorrectnodestats'][uriset['uri']]['sumhopspath'])/float(math.pow(15,numoflists))
                    uriset['elasticsearchscore'] = nodestats['incorrectnodestats'][uriset['uri']]['elasticsearchscore']
                larr.append(uriset)
            ldict[k] = larr
        newitem['ES_content'].append(ldict)
    finalresults.append(newitem)
print(json.dumps(finalresults), file = f)

f.close()
