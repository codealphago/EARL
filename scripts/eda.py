#!/usr/bin/python

import json,sys
import numpy as np
from sklearn import svm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

f = open(sys.argv[1])
s = f.read()
d = json.loads(s)
f.close()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

correctconn = []
incorrectconn = []
correctweights = []
incorrectweights = []
correctes = []
incorrectes = []

X1 = []
Y1 = []
Z1 = []
X2 = []
Y2 = []
Z2 = []
for item in d:
    for inc in item['incorrectnodestats']:
        feat = []
        incorrectconn.append(inc['connections'])
        feat.append(inc['connections'])
        incorrectweights.append(inc['sumofweights'])
        feat.append(inc['sumofweights'])
        incorrectes.append(inc['elasticsearchscore'])
        #feat.append(inc['elasticsearchscore'])
        X1.append(inc['connections'])
        Y1.append(inc['sumofweights'])
        Z1.append(inc['elasticsearchscore'])
    #plt.plot(X,Y, 'ro')
    for nc in item['correctnodestats']:
        feat = []
        correctconn.append(nc['connections'])
        feat.append(nc['connections'])
        correctweights.append(nc['sumofweights'])
        feat.append(nc['sumofweights'])
        correctes.append(nc['elasticsearchscore'])
        #feat.append(nc['elasticsearchscore'])
        X2.append(nc['connections'])
        Y2.append(nc['sumofweights'])
        Z2.append(nc['elasticsearchscore'])

ax.scatter(X1, Y1, Z1, color='r', marker='1')
ax.scatter(X2, Y2, Z2, color='b', marker='1')
ax.set_xlabel('Connections')
ax.set_ylabel('Sum of Weights')
ax.set_zlabel('Elasticsearch Score')
plt.show()


#clf = svm.SVC(kernel='linear', C = 1.0)
#print "Trainin SVM"
#clf.fit(X,Y)

#correct = 0
#incorrect = 0
#for feat,y in zip(X,Y):
#    if clf.predict(feat) == y:
#        correct += 1
#    else:
#        incorrect += 1
#
#
#print correct,incorrect

#print "correctconn mean %f"%(np.mean(correctconn))
#print "correctconn std %f"%(np.std(correctconn))
#print "incorrectconn mean %f"%(np.mean(incorrectconn))
#print "incorrectconn std %f"%(np.std(incorrectconn))
#
#print "correctweights mean %f"%(np.mean(correctweights))
#print "correctweights std %f"%(np.std(correctweights))
#print "incorrectweights mean %f"%(np.mean(incorrectweights))
#print "incorrectweights std %f"%(np.std(incorrectweights))
#
#print "correctes mean %f"%(np.mean(correctes))
#print "correctes std %f"%(np.std(correctes))
#print "incorrectes mean %f"%(np.mean(incorrectes))
#print "incorrectes std %f"%(np.std(incorrectes))
