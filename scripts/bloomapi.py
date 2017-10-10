#!/usr/bin/python

from flask import request
from flask import Flask
import json,sys
import itertools
from operator import itemgetter
from pybloom import BloomFilter

f = open('../data/blooms/bloom1hoppredicate.pickle')
bloom1hoppred = BloomFilter.fromfile(f)
f.close()

f = open('../data/blooms/bloom1hopentity.pickle')
bloom1hopentity = BloomFilter.fromfile(f)
f.close()

f = open('../data/blooms/bloom2hoppredicate.pickle')
bloom2hoppredicate = BloomFilter.fromfile(f)
f.close()

f = open('../data/blooms/bloom2hoptypeofentityentity.pickle')
bloom2hoptypeofentity = BloomFilter.fromfile(f)
f.close()

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

@app.route('/findBloomPaths', methods=['POST'])
def findBloomPaths():
    d = request.get_json(silent=True)
    print d
    lists = []
    for k,v in d.iteritems():
        lists.append(v)
    sequence = range(len(lists))
    result = []
    nodestats = {}
    for perm in itertools.permutations(sequence, 2):
        for uri1 in lists[perm[0]]:
            for uri2 in lists[perm[1]]:
                s = uri1+':'+uri2
                print s
                if s in bloom1hoppred:
                    result.append('%s has 0.5 hop predicate connection in knowledgebase'%s)
                    if uri1 not in nodestats:
                        nodestats[uri1] = {'connections':0, 'sumofweights':0}
                        nodestats[uri1]['connections'] += 1
                        nodestats[uri1]['sumofweights'] += 0.5
                    if uri2 not in nodestats:
                        nodestats[uri2] = {'connections':0, 'sumofweights':0}
                        nodestats[uri2]['connections'] += 1
                        nodestats[uri2]['sumofweights'] += 0.5
                if s in bloom1hopentity:
                    result.append('%s has 1 hop entity connection in knowledgebase'%s)
                    if uri1 not in nodestats:
                        nodestats[uri1] = {'connections':0, 'sumofweights':0}
                        nodestats[uri1]['connections'] += 1
                        nodestats[uri1]['sumofweights'] += 1
                    if uri2 not in nodestats:
                        nodestats[uri2] = {'connections':0, 'sumofweights':0}
                        nodestats[uri2]['connections'] += 1
                        nodestats[uri2]['sumofweights'] += 1
                if s in bloom2hoppredicate:
                    result.append('%s has 2 hop predicate connection in knowledgebase'%s)
                    if uri1 not in nodestats:
                        nodestats[uri1] = {'connections':0, 'sumofweights':0}
                        nodestats[uri1]['connections'] += 1
                        nodestats[uri1]['sumofweights'] += 1.5
                    if uri2 not in nodestats:
                        nodestats[uri2] = {'connections':0, 'sumofweights':0}
                        nodestats[uri2]['connections'] += 1
                        nodestats[uri2]['sumofweights'] += 1.5
                if s in bloom2hoptypeofentity:
                    result.append('%s has 2 hop typeOf connection in knowledgebase'%s)
                    if uri1 not in nodestats:
                        nodestats[uri1] = {'connections':0, 'sumofweights':0}
                        nodestats[uri1]['connections'] += 1
                        nodestats[uri1]['sumofweights'] += 2
                    if uri2 not in nodestats:
                        nodestats[uri2] = {'connections':0, 'sumofweights':0}
                        nodestats[uri2]['connections'] += 1
                        nodestats[uri2]['sumofweights'] += 2
    finalresult = {'lists':d, 'humanresults': result, 'nodestats': nodestats }
    return json.dumps(finalresult)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005,debug=True)
