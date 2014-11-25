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
                    for key in ['category', 'name', 'brand','description']:
                        self.shingles.addToShingle(
                            TextProcess().processing(
                                product.__dict__[key], i), product.id)
            num += 100
            if num > 250:
                break
            print num
             
        self.shingles.doMinHashing(50)
    
    
    def makeDecision(self,user): 
        tweets = ''
        scalarM = lambda v1, v2:  sum(v1[i]['value']*v2[i]['value'] 
                                      for i in xrange(min(len(v1), len(v2))) 
                                          if v1[i]['pos'] == v2[i]['pos'])

        for tweet in user.getTweets():
            tweets += tweet
        
        model = {}
        
        for i in xrange(1,3):
            model = dict( TextProcess().processing(tweets, i, True).items() + model.items() )
        
        userShingles =self.shingles.getMinHash(model)
        

        
        userLen = scalarM(userShingles, userShingles)
        
        scalar= [scalarM(v, userShingles)/math.sqrt(userLen * scalarM(v, v)) for v in self.shingles.minHash]    
        #print scalar
        res = scalar.index( max(scalar) )
        print res, scalar[res], self.shingles.docs[res], len(userShingles)

        for i in xrange(len(userShingles)):
            if userShingles[i]['pos'] == self.shingles.minHash[res][i]['pos']:
                print self.shingles.enShingleMap[userShingles[i]['pos']], userShingles[i], self.shingles.minHash[res][i]
        
d = Decision()
d.makeDecision(CreateIfNotFindUser('Kadiki_',TwitterSearcher()))     
        
        