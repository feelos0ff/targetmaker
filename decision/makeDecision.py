# -*- coding: utf-8 -*-
'''
Created on 23 нояб. 2014 г.

@author: feelosoff
'''
import sys
from pyes.query import QueryStringQuery
import unicodedata2
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
        InitDB()
        '''
        es = ES('127.0.0.1:9200')
    
        for goods in GetAll(Goods):
            for product in goods:
                productFields = dict()
                
                for key, value in product.__dict__.items():
                    if key != '_sa_instance_state':
                        productFields[key]= value
                        
                es.index(productFields,'tweezon','tweets')
    
        '''
    def makeDecision(self,user): 
        targets = []
        es = ES('127.0.0.1:9200')
        for tweet in user.getTweets()[:]:
            tweet = TextProcess().processing(tweet)
            if not tweet:
                continue
            query = QueryStringQuery(tweet)
            print tweet.encode('utf-8')
            targets += es.search(query, "tweezon","tweets")
        for taget in targets:
            print taget
d = Decision()
d.makeDecision(CreateIfNotFindUser('Kadiki_',TwitterSearcher()))     
        
        