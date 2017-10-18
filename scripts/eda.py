#!/usr/bin/python

import json,sys
import numpy as np
from sklearn import svm
import matplotlib
matplotlib.use('agg')
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
for question in d:
    for listt in question['ES_content']:
        for k,v in listt.iteritems():
            if k == 'label':
                continue
            for item in v:
                if item['correctlabel'] == 1:
                    correctconn.append(item['sumhopspath'])
                    correctweights.append(item['pathlength'])
                    correctes.append(item['elasticsearchscore'])
                    X2.append(item['sumhopspath'])
                    Y2.append(item['pathlength'])
                    Z2.append(item['elasticsearchscore']) 
                else:
                    incorrectconn.append(item['sumhopspath'])
                    incorrectweights.append(item['pathlength'])
                    incorrectes.append(item['elasticsearchscore'])
                    X1.append(item['sumhopspath'])
                    Y1.append(item['pathlength'])
                    Z1.append(item['elasticsearchscore'])
ax.scatter(X1, Y1, Z1, color='r', marker='1')
ax.scatter(X2, Y2, Z2, color='b', marker='1')
ax.set_xlabel('sum hops path')
ax.set_ylabel('path length')
ax.set_zlabel('Elasticsearch Score')
#plt.show()
plt.savefig('foo.png')


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
