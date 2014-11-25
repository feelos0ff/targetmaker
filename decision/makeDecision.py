# -*- coding: utf-8 -*-
'''
Created on 23 нояб. 2014 г.

@author: feelosoff
'''

from decision.shingle import Shingle
from buildering.models import Goods
from buildering.db import InitDB, GetAll
from parsers.text import TextProcess
from graph.orient import CreateIfNotFindUser
from twitter.request import TwitterSearcher    
import math

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
        num = 0
        for goods in GetAll(Goods):
            for product in goods:
                for i in xrange(1,3):
                    for key in ['category', 'detail', 'name', 'brand', 'description']:
                        self.shingles.addToShingle(
                            TextProcess().processing(
                                product.__dict__[key], i), product.id)
            num += 100
            if num > 1000:
                break
            print num
             
        self.shingles.doMinHashing(8)
    
    def scalarM(self,v1,v2):
        count = min(len(v1), len(v2))
        return sum(v1[i]['value']*v2[i]['value'] for i in xrange(count) if v1[i]['pos'] == v2[i]['pos'])
    
    def makeDecision(self,user): 
        tweets = ''
        for tweet in user.getTweets():
            tweets += tweet
        model = {}
        
        for i in xrange(1,3):
            model = dict( TextProcess().processing(tweets, i).items() + model.items() )
        
        userShingles =self.shingles.getMinHash(model)
        
        userLen = self.scalarM(userShingles, userShingles)
        
        scalar= [self.scalarM(v, userShingles)/math.sqrt(userLen * self.scalarM(v, v)) for v in self.shingles.minHash]    
        #print scalar
        res = scalar.index( max(scalar) )
        print res, scalar[res], self.shingles.docs[res]
        print userShingles

d = Decision()
d.makeDecision(CreateIfNotFindUser('Ncorres',TwitterSearcher()))     
        
        