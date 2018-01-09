#!/usr/bin/python

import json,sys
import itertools
from operator import itemgetter
from pybloom import BloomFilter
import numpy as np
from pytsp import atsp_tsp, run,  dumps_matrix
import os,glob

reload(sys)
sys.setdefaultencoding('utf8')

class JointLinker:
    def __init__(self):
        print "Joint Linker initializing"
        try:
            f = open('../data/blooms/bloom1hoppredicate.pickle')
            self.bloom1hoppred = BloomFilter.fromfile(f)
            f.close()
            f = open('../data/blooms/bloom1hopentity.pickle')
            self.bloom1hopentity = BloomFilter.fromfile(f)
            f.close()
            f = open('../data/blooms/bloom2hoppredicate.pickle')
            self.bloom2hoppredicate = BloomFilter.fromfile(f)
            f.close()
            f = open('../data/blooms/bloom2hoptypeofentity.pickle')
            self.bloom2hoptypeofentity = BloomFilter.fromfile(f)
            f.close()
        except Exception,e:
            print e
            sys.exit(1)
        print "Joint Linker initialized"

    def jointLinker(self, topklists):
        lists = []
        chunktexts = []
        ertypes = []
        for chunk in topklists:
            lists.append(chunk['topkmatches'])
            chunktexts.append(chunk['chunk']) 
            ertypes.append(chunk['class'])
        if len(lists) == 1:
            return {'resultnodes': [lists[0][0]], 'chunktext': chunktexts, 'ertypes': ertypes}
        totalnodes = sum(len(x) for x in lists)
        graph = np.zeros(shape=(totalnodes,totalnodes))
        graph.fill(99999) #not connected in knowledge graph
        np.fill_diagonal(graph,0)
        nodestore = []
        count = 0
        for listt in lists:
            innercount = 0
            for uri in listt:
                nodestore.append(uri+';#'+str(count)+';#'+str(innercount))
                count += 1
                innercount += 1
        for uri1 in nodestore:
            for uri2 in nodestore:
                uri1filt = uri1.split(';#')[0]
                uri2filt = uri2.split(';#')[0]
                uri1pos = int(uri1.split(';#')[1])
                uri2pos = int(uri2.split(';#')[1])
                uri1rank = int(uri1.split(';#')[2])
                uri2rank = int(uri2.split(';#')[2])
                bloomstring1 = uri1filt+':'+uri2filt
                bloomstring2 = uri2filt+':'+uri1filt
                if bloomstring1 in self.bloom1hoppred or bloomstring2 in self.bloom1hoppred:
                    graph[uri1pos][uri2pos] = 0.5 + uri1rank + uri2rank
                    graph[uri2pos][uri1pos] = 0.5 + uri1rank + uri2rank
                elif bloomstring1 in self.bloom1hopentity or bloomstring2 in self.bloom1hopentity: 
                    graph[uri1pos][uri2pos] = 1 + uri1rank + uri2rank
                    graph[uri2pos][uri1pos] = 1 + uri1rank + uri2rank
                elif bloomstring1 in self.bloom2hoppredicate or bloomstring2 in self.bloom2hoppredicate:
                    graph[uri1pos][uri2pos] = 1.5 + uri1rank + uri2rank
                    graph[uri2pos][uri1pos] = 1.5 + uri1rank + uri2rank
                elif bloomstring1 in self.bloom2hoptypeofentity or bloomstring2 in self.bloom2hoptypeofentity:
                    graph[uri1pos][uri2pos] = 2 + uri1rank + uri2rank
                    graph[uri2pos][uri1pos] = 2 + uri1rank + uri2rank

        gtsp_sets_s = []
        innercount = 1
        outercount = 1
        for listt in lists:
            innerlist = [outercount]
            for uri in listt:
                innerlist.append(innercount)
                innercount += 1 
            innerlist.append(-1) 
            outercount += 1
            gtsp_sets_s.append(innerlist)

        outf = "/tmp/myroute.tsp"
        with open(outf, 'w') as dest:
            dest.write(dumps_matrix(graph, gtsp_sets_s, len(lists), name="myroute"))
        tour = run(outf, start=None, solver="GLKH")
        nodes = [] 
        for node in tour['tour']:
            nodes.append(nodestore[node].split(';')[0])
        
        for fl in glob.glob("/tmp/myroute*"):
            os.remove(fl)
        return {'resultnodes': nodes, 'chunktext': chunktexts, 'ertypes': ertypes}
    

if __name__ == '__main__':
    j = JointLinker()
    print j.jointLinker([{'chunk': 'obama', 'class': 'entity', 'topkmatches': [u'http://dbpedia.org/resource/Mr._Obama', u'http://dbpedia.org/resource/Al-Haramain_v._Obama', u'http://dbpedia.org/resource/Obama_(disambiguation)', u'http://dbpedia.org/resource/Obama_(surname)', u'http://dbpedia.org/resource/Klayman_v._Obama', u'http://dbpedia.org/resource/Shut_up_your_mouse,_Obama', u'http://dbpedia.org/resource/Hedges_v._Obama', u'http://dbpedia.org/resource/Obama_(genus)', u'http://dbpedia.org/resource/Obama,_Nagasaki', u'http://dbpedia.org/resource/Obama\u2013Medvedev_Commission', u'http://dbpedia.org/resource/Obama-mania', u'http://dbpedia.org/resource/Obama,_Fukui', u'http://dbpedia.org/resource/Obama:_From_Promise_to_Power', u'http://dbpedia.org/resource/Obama,_Sarah', u'http://dbpedia.org/resource/President_Obama_on_Death_of_Osama_bin_Laden_(SPOOF)', u'http://dbpedia.org/resource/Oyama', u'http://dbpedia.org/resource/Ohama', u'http://dbpedia.org/resource/Obara', u'http://dbpedia.org/resource/Odama', u'http://dbpedia.org/resource/Otama', u'http://dbpedia.org/resource/Obava', u'http://dbpedia.org/resource/Okama', u'http://dbpedia.org/resource/Obata', u'http://dbpedia.org/resource/Felicidad_(Margherita)', u'http://dbpedia.org/resource/Mbama', u'http://dbpedia.org/resource/Obala', u'http://dbpedia.org/resource/Obaba', u'http://dbpedia.org/resource/Oboama', u'http://dbpedia.org/resource/Bama', u'http://dbpedia.org/resource/Pan-orama', u'http://dbpedia.org/resource/Oyama,_Shizuoka', u'http://dbpedia.org/resource/Tropical_Cyclone_Nisha-Orama', u'http://dbpedia.org/resource/Obara,_Aichi', u'http://dbpedia.org/resource/Oyama,_British_Columbia', u'http://dbpedia.org/resource/Omama,_Gunma', u'http://dbpedia.org/resource/Obata,_Mie', u'http://dbpedia.org/resource/Oyama,_Tochigi', u'http://dbpedia.org/resource/Flora-Bama', u'http://dbpedia.org/resource/Bama,_Burkina_Faso', u"http://dbpedia.org/resource/Osama\u2014Yo'_Mama:_The_Album", u'http://dbpedia.org/resource/Bama,_Nigeria', u'http://dbpedia.org/resource/Obama_Domain', u'http://dbpedia.org/resource/Obama_logo', u'http://dbpedia.org/resource/Obama_Mama', u'http://dbpedia.org/resource/Obama_Academy', u'http://dbpedia.org/resource/Obama_Doctrine', u'http://dbpedia.org/resource/Barack_Obama', u'http://dbpedia.org/resource/Obama_chmo', u'http://dbpedia.org/resource/Back_Obama', u'http://dbpedia.org/resource/Mount_Obama', u'http://dbpedia.org/resource/Obama_BasedGod']}, {'chunk': 'mother', 'class': 'relation', 'topkmatches': [u'http://dbpedia.org/property/mother/father', u'http://dbpedia.org/property/father,Mother', u'http://dbpedia.org/property/father', u'http://dbpedia.org/property/mother', u'http://dbpedia.org/property/%5Dother', u'http://dbpedia.org/property/mmaOther', u'http://dbpedia.org/property/mother%60sName', u'http://dbpedia.org/property/mothert', u'http://dbpedia.org/property/mather', u'http://dbpedia.org/property/other', u'http://dbpedia.org/ontology/other']}])
     
        
