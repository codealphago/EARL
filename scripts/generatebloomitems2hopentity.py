#!/usr/bin/python


import sys
from sets import Set
from pybloom import BloomFilter
import redis

reload(sys)
sys.setdefaultencoding('utf8')

d1 = {}
red = redis.StrictRedis(host='localhost', port=6379, db=0)
bloom  = BloomFilter(capacity=200000000, error_rate=0.000001)
f = open(sys.argv[1])
count = 0
red.set('linesread3',0)
for line in f.readlines():
    if count == 0:
        count += 1
        continue
    line = line.strip()
    red.incr('linesread3')
    try:
        s,p,o = line.split(' ')
        if s not in d1:
            d1[s] = Set()
            d1[s].add(o)
        else:
            d1[s].add(o)
        if o not in d1:
            d1[o] = Set()
            d1[o].add(s)
        else:
            d1[o].add(s)
    except Exception,e:
        pass
    count += 1
f.close()
f = open(sys.argv[1])

red.set('linesread3',0)
for line in f.readlines():
    if count == 0:
        count += 1
        continue
    line = line.strip()
    try:
        red.incr('linesread3')
        s,p,o = line.split(' ')
        if o in d1:
            for sub in d1[o]:
                bloom.add(s+':'+sub)
        if s in d1:
            for sub in d1[s]:
                bloom.add(o+':'+sub)
    except Exception,e:
        pass

f.close()

f = open('/data/debayan/blooms/bloom2hopentity.pickle','w')
bloom.tofile(f)
f.close()
