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
                for i in xrange(2,3):
                    for key in ['category', 'detail', 'name', 'brand']:
                        self.shingles.addToShingle(
                            TextProcess().processing(
                                product.__dict__[key], i), product.id)
            num += 100
            if num > 1000:
                break
            print num
             
        print 'azaza'
        self.shingles.doMinHashing(8)
        print 'wow'
        
    def makeDecision(self,user): 
        tweets = ''
        for tweet in user.getTweets():
            tweets += tweet
        model = {}
        
        for i in xrange(1,4):
            model = dict( TextProcess().processing(tweets, i).items() + model.items() )
        
        userShingles =self.shingles.getMinHash(model)
        
        print userShingles

d = Decision()
d.makeDecision(CreateIfNotFindUser('Ncorres',TwitterSearcher()))     
        
        