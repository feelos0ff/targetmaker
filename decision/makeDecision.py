# -*- coding: utf-8 -*-
'''
Created on 23 нояб. 2014 г.

@author: feelosoff
'''
import sys
from pyes.query import QueryStringQuery, Search
from pyes.highlight import HighLighter
from rake.rake import Rake
from parsers.text import TextProcess
sys.path.insert(0,'/home/priora/workspace/targetmaker/')

from buildering.models import Goods
from buildering.db import InitDB, GetAll, GetNum
from parsers.text import TextProcess
from graph.orient import GraphWrapper
from twitter.request import TwitterSearcher    
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
        self.keyword = Rake("../rake/SmartStoplist.txt")
        self.processor = TextProcess()
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
                   
            keywordsList = [" AND ".self.processor.processing(word[0]) 
                            for word in self.keyword.run(tweet) 
                                if word[1] > 1]
            if not keywordsList:
                continue
            
            query = " OR ".join(self.processor.processing(keywordsList))
            res = es.search( QueryStringQuery(query), "tweezon","goods")[0]     
            
            try:
                if res:
                    targets += res[0]
                else:
                    res = es.search( QueryStringQuery(tweet), "tweezon","goods")
                    if res:
                        targets += res[0]
            except:
                pass
            
            
d = Decision()
d.makeDecision(GraphWrapper().createIfNotFindUser('Kadiki_',TwitterSearcher()))     

