#!/usr/bin/python

import sys, os, json,  urllib3, requests, codecs, re
from elasticsearch import Elasticsearch,helpers
from gevent.wsgi import WSGIServer
from flask import request
from flask import Flask
from sets import Set
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

reload(sys)
sys.setdefaultencoding('utf8')
app = Flask(__name__)

es = Elasticsearch(['http://131.220.155.102:9201'])
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

@app.route('/getresponse/<label>/<topk>', methods=['GET'])
def getresponse(label, topk):
    response = process.extract(label.lower(), choices, limit = int(topk), scorer=fuzz.token_sort_ratio)
    return json.dumps(response)

if __name__ == '__main__':
    http_server = WSGIServer(('', int(sys.argv[1])), app)
    http_server.serve_forever()
