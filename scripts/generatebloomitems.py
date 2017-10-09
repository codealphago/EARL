#!/usr/bin/python


import sys
from sets import Set
import redis

reload(sys)
sys.setdefaultencoding('utf8')

red = redis.StrictRedis(host='localhost', port=6379, db=4)

f = open(sys.argv[1])
sett = Set()
d = {}
d1 = {}
count = 0
rels = ['http://dbpedia.org/ontology/wikiPageWikiLink','http://www.w3.org/2002/07/owl#sameAs','http://purl.org/dc/terms/subject','http://www.w3.org/2000/01/rdf-schema#label','http://dbpedia.org/ontology/wikiPageRevisionID','http://www.w3.org/ns/prov#wasDerivedFrom','http://dbpedia.org/ontology/wikiPageID','http://dbpedia.org/ontology/wikiPageOutDegree','http://dbpedia.org/ontology/wikiPageLength','http://xmlns.com/foaf/0.1/primaryTopic','http://xmlns.com/foaf/0.1/isPrimaryTopicOf','http://purl.org/dc/elements/1.1/language','http://dbpedia.org/ontology/wikiPageExternalLink','http://dbpedia.org/ontology/wikiPageRedirects','http://dbpedia.org/ontology/abstract','http://www.w3.org/2000/01/rdf-schema#comment','http://dbpedia.org/property/wikiPageUsesTemplate','http://dbpedia.org/ontology/wikiPageDisambiguates']
for line in f.readlines():
    if count == 0:
        count += 1
        continue
    line = line.strip()
    try:
        s,p,o = line.split(',')
        if p in rels:
            continue
        if s not in d1:
            d1[s] = [p]
        else:
            d1[s].append(p)
        if o not in d1:
            d1[o] = [p]
        else:
            d1[o].append(p)
        #print s,p,o
    except Exception,e:
        pass
    count += 1
f.close()
f = open(sys.argv[1])

red.set('linesread',0)
for line in f.readlines():
    if count == 0:
        count += 1
        continue
    line = line.strip()
    try:
        red.incr('linesread')
        s,p,o = line.split(',')
        if p in rels:
            continue
        if o in d1:
            for pred in d1[o]:
                if pred == p:
                    continue
                red.set(s+':'+pred,0)
                #print s+':'+pred
        if s in d1:
            for pred in d1[s]:
                if pred == p:
                    continue
                red.set(o+':'+pred,0)
                #print o+':'+pred
    except Exception,e:
        pass

print len(sett)
f.close()
