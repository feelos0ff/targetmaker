# -*- coding: utf-8 -*-
'''
Created on 23 нояб. 2014 г.

@author: feelosoff
'''
import sys
sys.path.insert(0,'/home/priora/workspace/targetmaker/')
sys.path.insert(0,'/home/feelosoff/workspace/targetmaker/')
#from pyes.query import QueryStringQuery
from rake.rake import Rake
import json
from twitter.filter import TweeFilter
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

        InitDB()
        self.processor = TextProcess()
        self.keyword = Rake("../rake/SmartStoplist.txt")
        self.es = ES('127.0.0.1:9200')
        self.goods = {}
        self.tweeFilter=TweeFilter().find

    def depth(self, parent, category, product, k):
        if not category:
            if not product["name"] in parent.keys():
                parent[product["name"]] = [product["id"], k]
            else:
                parent[product["name"]][1] += k
        
        for key, val in category.items():
            key = key.strip()
            if key in parent.keys():
                self.depth(parent[key][0], val, product, k)
            else:
                parent[key] = self.depth({}, val, product, k)
            parent[key][1] += k
            
        return [parent, 0]
    
    def addToGraph(self, product, k = 1):
        self.goods = self.depth( self.goods,json.loads(product["category"]),product, k)[0]
 
    def getBestChoice(self):
        it = self.goods
        while isinstance(it, dict) or isinstance(it, defaultdict):
            optKey = max(it.items(), key = lambda x : x[1][1])[0]
            it = it[optKey][0]
        # вернули товар о котором чаще всего говорили(можно через граф откатиться на уровеь назад и взять рандом)
        print it, str(it), unicode(it)
        
        return it
                
    def contextDecision(self,user):
        for tweet in user.getTweets()[:]:  
            keywordsList = [(" ".join(self.processor.processing(word[0]))) 
                            for word in self.keyword.run(tweet) 
                                if word[1] > 1]
            if not keywordsList:
                continue
            
            keywordsList += [" ".join(self.processor.processing(tweet))] 
            for query in keywordsList:
                res = self.tweeFilter(query)     
                
                try:
                    if res:
                        print query, res["name"], res["brand"],res["category"]
                        self.addToGraph( res)
                except Exception as e:
                    print e
                    pass
            
        return self

    def makeDecision(self,user): 
        '''
        for v in user.inV():
            if not v.idEl:
                v.idEl = str( self.contextDecision(v).getBestChoice() )
                v.save()
                self.goods.clear()
        
        for v in user.inV():
            self.addToGraph(v, 0.33)
        '''   
        self.contextDecision(user).getBestChoice()
       # user.idEl = str(self.contextDecision(user).getBestChoice())
       # user.save()
        
        return user.idEl
            
d = Decision()
d.makeDecision(GraphWrapper().createIfNotFindUser('VynnieMcDaniels',TwitterSearcher())) 