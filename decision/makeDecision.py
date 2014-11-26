# -*- coding: utf-8 -*-
'''
Created on 23 нояб. 2014 г.

@author: feelosoff
'''
import sys
sys.path.insert(0,'/home/priora/workspace/targetmaker/')

from decision.shingle import Shingle
from buildering.models import Goods
from buildering.db import InitDB, GetAll, GetNum
from parsers.text import TextProcess
from graph.orient import CreateIfNotFindUser
from twitter.request import TwitterSearcher    
import math
from pyes import ES

class Decision(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.shingles = Shingle()
        InitDB()
        '''
        mapping = {u'country_code': {'boost': 1.0,
                                'index': 'analyzed',
                                'store': 'yes',
                                'type': u'string',
                                "term_vector": "with_positions_offsets"},
                u'country_name': {'boost': 1.0,
                                'index': 'analyzed',
                                'store': 'yes',
                                'type': u'string',
                                "term_vector": "with_positions_offsets"},
                u'region_code': {'boost': 5.0,
                                'index': 'analyzed',
                                'store': 'yes',
                                'type': u'string',
                                "term_vector": "with_positions_offsets"},
                u'region_name': {'boost': 5.0,
                                'index': 'analyzed',
                                'store': 'yes',
                                'type': u'string',
                                "term_vector": "with_positions_offsets"},
                u'city_name': {'boost': 1.0,
                                'index': 'analyzed',
                                'store': 'yes',
                                'type': u'string',
                                "term_vector": "with_positions_offsets"},
        }
      
        es = ES('127.0.0.1:9200')
        es.indices.create_index("geo-index")
        es.indices.put_mapping("geo", {'properties': mapping}, "geo-index")
    
        for goods in GetAll(Goods):
            for product in goods:
        '''       
    
    
    def makeDecision(self,user): 
        tweets = ''
        scalarM = lambda v1, v2:  sum(1#v1[i]['value']*v2[i]['value'] 
                                      for i in xrange(min(len(v1), len(v2))) 
                                          if v1[i]['pos'] == v2[i]['pos'])

        for tweet in user.getTweets()[:]:
            tweets += tweet
        
        model = {}
        
        for i in xrange(1,3):
            model = dict( TextProcess().processing(tweets, i, True).items() + model.items() )
        
        for key, value in model.items():
            print key,value
            
        userShingles =self.shingles.getMinHash(model)
        
        print len(tweets)
        print tweets.encode('utf-8')
        userLen = scalarM(userShingles, userShingles)
        
        scalar= [scalarM(v, userShingles)/math.sqrt(userLen * scalarM(v, v)) for v in self.shingles.minHash]    
        #print scalar
        res = scalar.index( max(scalar) )
        print res, scalar[res], self.shingles.docs[res], len(userShingles)

        for i in xrange(len(userShingles)):
            if userShingles[i]['pos'] == self.shingles.minHash[res][i]['pos']:
                print self.shingles.enShingleMap[userShingles[i]['pos']], userShingles[i], self.shingles.minHash[res][i]
        p = GetNum( Goods,self.shingles.docs[res])
        print p.url
        '''
        print p.category
        for key, val in TextProcess().processing(p.category).items():
            print key, val
        print p.name
        for key, val in TextProcess().processing(p.name).items():
            print key, val
        print p.brand
        for key, val in TextProcess().processing(p.brand).items():
            print key, val
        print p.description
        for key, val in TextProcess().processing(p.description).items():
            print key, val
        '''
d = Decision()
d.makeDecision(CreateIfNotFindUser('Kadiki_',TwitterSearcher()))     
        
        