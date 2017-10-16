#!/usr/bin/python

import json,sys
import numpy as np

f = open(sys.argv[1])
s = f.read()
d = json.loads(s)
f.close()


correctconn = []
incorrectconn = []
correctweights = []
incorrectweights = []
correctes = []
incorrectes = []
for item in d:
    for inc in item['incorrectnodestats']:
        incorrectconn.append(inc['connections'])
        incorrectweights.append(inc['sumofweights'])
        incorrectes.append(inc['elasticsearchscore'])
    for nc in item['correctnodestats']:
        correctconn.append(nc['connections'])
        correctweights.append(nc['sumofweights'])
        correctes.append(nc['elasticsearchscore'])

print "correctconn mean %f"%(np.mean(correctconn))
print "correctconn std %f"%(np.std(correctconn))
print "incorrectconn mean %f"%(np.mean(incorrectconn))
print "incorrectconn std %f"%(np.std(incorrectconn))

print "correctweights mean %f"%(np.mean(correctweights))
print "correctweights std %f"%(np.std(correctweights))
print "incorrectweights mean %f"%(np.mean(incorrectweights))
print "incorrectweights std %f"%(np.std(incorrectweights))

print "correctes mean %f"%(np.mean(correctes))
print "correctes std %f"%(np.std(correctes))
print "incorrectes mean %f"%(np.mean(incorrectes))
print "incorrectes std %f"%(np.std(incorrectes))
