#!/usr/bin/python

import sys, os, json,  urllib3, requests, codecs, re
from elasticsearch import Elasticsearch,helpers
from sets import Set
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import redis

reload(sys)
sys.setdefaultencoding('utf8')

red = redis.StrictRedis()
pool = ThreadPool(10)

es = Elasticsearch()
q={"query" : {"match_all" : {}}, "size" : 15000000}
records = helpers.scan(es, query=q , index="dbpredicateindex14", doc_type="records")
d1 = {}
choices = []
for hit in records:
    label = hit['_source']['mergedLabel'].lower()
    if label not in d1:
        d1[label] = [hit['_source']['uri']]
    else:
        if hit['_source']['uri'] not in d1[label]:
            d1[label].append(hit['_source']['uri'])

for k,v in d1.iteritems():
    choices.append(k)

f = open(sys.argv[1])
s = f.read()
d = json.loads(s)

red.set('totalcount',0)
red.set('correctcount',0)
red.set('missingcount',0)
items = []
for ques in d:
    for item in ques['predicate mapping']:
        items.append(item)

def getresponse(item):
    url = "http://131.220.155.68:81/getresponse/%s/100"%item['label']
    try:
        r = requests.get(url)
        response =json.loads(r.text)
    except Exception,e:
        print e
        return
    found = False
    s = Set()
    hitarray = []
    red.incr('totalcount')
    for hit in response:
        for uri in d1[hit[0]]:
            if uri not in s:
                s.add(uri)
                hitarray.append(uri)
        if len(s) >= 50:
            break
    for uri in hitarray:
        if uri == item['uri']:
            found = True
            red.incr('correctcount')
            break
    if not found:
        print "Not found: %s %s"%(item['label'], item['uri'])
        red.incr('missingcount')


results = pool.map(getresponse, items)
pool.close()
pool.join()

print red.get('totalcount'),red.get('correctcount'),red.get('missingcount')
