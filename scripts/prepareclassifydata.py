#!/usr/bin/python

from __future__ import print_function

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
    #newitem['ES_content'] = item['ES_content']
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
                else:
                    uriset['correctlabel'] = 0
                larr.append(uriset)
            ldict[k] = larr
        newitem['ES_content'].append(ldict)
    correctlength = len(item['correct'])
    count = 0
    nodestats = json.loads(item['response'])
    newitem['correctnodestats'] = []
    for uri,tupl in nodestats['correctnodestats'].iteritems():
        correctdict = {}
        correctdict['uri'] = uri
        correctdict['connections'] = tupl['connections']/float(correctlength)
        correctdict['sumofhops'] = tupl['sumofhops']/float(correctlength)
        correctdict['elasticsearchscore'] = tupl['elasticsearchscore']
        newitem['correctnodestats'].append(correctdict)
    newitem['incorrectnodestats'] = []
    for uri,tupl in nodestats['incorrectnodestats'].iteritems():
        incorrectdict = {}
        incorrectdict['uri'] = uri
        incorrectdict['connections'] = tupl['connections']/float(correctlength)
        incorrectdict['sumofhops'] = tupl['sumofhops']/float(correctlength)
        incorrectdict['elasticsearchscore'] = tupl['elasticsearchscore']
        newitem['incorrectnodestats'].append(incorrectdict)
    finalresults.append(newitem)
print(json.dumps(finalresults), file = f)

f.close()
