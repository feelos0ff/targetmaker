# -*- coding: utf-8 -*-
'''
Created on 23 нояб. 2014 г.

@author: feelosoff
'''
import sys
from pyes.query import QueryStringQuery
from rake.rake import Rake
import json
from __builtin__ import max
sys.path.insert(0,'/home/priora/workspace/targetmaker/')
from collections import defaultdict
from buildering.db import InitDB
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
        self.processor = TextProcess()
        self.keyword = Rake("../rake/SmartStoplist.txt")
     
        self.es = ES('127.0.0.1:9200')
    
        self.graph = defaultdict(list)

    def depth(self, parent, category, product):
        if not category:
            if parent[product.name]:
                return parent[product.name]
            else:
                return [product, 0]
        
        for key, val in category.items():
            if parent[key]:
                self.depth(parent[key],val, product)
            else:
                parent[key] = self.depth(parent[key],val, product)
                parent[key][1] += 1
            
            return [parent, 0]
    
    def addToGraph(self, product):
        self.graph = self.depth( self.graph,json.loads(product.category),product)
       
    def getBestChoice(self):
        it = self.graph
        while isinstance(it, dict) or isinstance(it, defaultdict):
            optKey = max(it.items(), key = lambda x : x[1][1])
            it = it[optKey]
        # вернули товар о котором чаще всего говорили(можно через граф откатиться на уровеь назад и взять рандом)
        return it
                
    def makeDecision(self,user): 

        # переработать
        for tweet in user.getTweets()[:]:  
    
            keywordsList = [(" ".join(self.processor.processing(word[0]))) 
                            for word in self.keyword.run(tweet) 
                                if word[1] > 1]
            if not keywordsList:
                continue
            
            query = " ".join(keywordsList)
            res = self.es.search( QueryStringQuery(query), "tweezon","goods")     
            
            try:
                if res:
                    self.addToGraph( res[0])
                else:
                    res = self.es.search( QueryStringQuery(tweet), "tweezon","goods")
                    if res:
                        self.addToGraph( res[0])
            except:
                pass

        print self.getBestChoice()

d = Decision()
d.makeDecision(GraphWrapper().createIfNotFindUser('Kadiki_',TwitterSearcher()))     