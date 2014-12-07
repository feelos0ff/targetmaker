# -*- coding: utf-8 -*-
'''
Created on 12 авг. 2014 г.

@author: feelosoff
'''

import json
from buildering.models import  Persons, Goods
import unicodedata2
from graph import InitGraph,  GetRoot
from buildering.db import InitDB, GetAll
from twitter.request import TwitterSearcher 
from twitter.filter import TweeFilter   
from pyes import ES
from parsers.text import TextProcess


class GraphWrapper:
    
    def __init__(self):
        self.g = InitGraph()
        self.rootNode = GetRoot(self.g)
        self.es = ES('127.0.0.1:9200')
        self.tweeFilter = TweeFilter()
        self.norm = TextProcess().normalizeForGraph
    
    def depth(self,parent, tree, product):
        if tree == {}:
            k = unicodedata2.normalize('NFD',unicode(product.name )).strip()
            self.g.categoriesLink.create(parent, product, {'label': k})
            
        for key, val in tree.items():
            if key == '': 
                continue
            if key.find('\n') > 0:
                continue    
            
            k = unicodedata2.normalize('NFD',unicode(key )).strip()
            category = ''
            
            if not parent.outE() or not parent.outE(k):
                category = self.g.category.create()  
                self.g.categoriesLink.create(parent,category, {'label':k})
    
            else:
                category = parent.outE(k).outV()             
    
            self.depth(category, val, product)
        
    def addProductToGraph(self,product):
    
        rec = self.g.goods.create(
                              num = product.id,        
                              detail= self.norm(product.detail), 
                              name = self.norm(product.name), 
                              price = product.price, 
                              description = self.norm(product.description),
                              brand = self.norm(product.brand),
                              url = product.url
                            )
        self.depth( self.rootNode, 
               json.loads(product.category), 
               rec)
            
    def createIfNotFindFollow(self, user, follower):
        inGraph = user.inE(start=follower.eid)
        
        if (not inGraph) or (inGraph[0].outV() != user):
            return self.g.follow.create(user, follower)
    
        return inGraph[0]
        
    def createIfNotFindUser(self, userLogin, searcher):
        inGraph = self.g.twitterUser.index.lookup(screen_name=userLogin)
        user = None
        
        if not inGraph:
            try:
                info = searcher.getPersonActions(userLogin)
            except Exception as e:
                if e.response.status == 401:
                    return None
                print e
                
            twitts = [self.es.index({'twitt' :stat.text , 'key' : userLogin},"twitter", "twitts")['_id']
                        for stat in info if self.tweeFilter(stat)]
            
            if len(twitts)< 5:
                return None
            
            try:
                userName = info[0].author.name
                userLocation = info[0].author.location
    
            except Exception as e:
                print 'add user exc', e
                userName = ''
                userLocation = ''
            
            user = self.g.twitterUser.create( name = userName, 
                                         screen_name= self.norm(userLogin), 
                                         data = twitts, 
                                         location = self.norm(userLocation)
                                        )
        else:
            user = inGraph.next()
        
        return user
        
    def addUserToGraph(self, userLogin, searcher):
        try:
            user = self.createIfNotFindUser(userLogin, searcher)  
        except:
            return False
        
        if not user:
            return False
          
        followers = searcher.getFollowers(screen_name=user.screen_name)
        
        for follower in followers:
            try:
                follower = self.createIfNotFindUser(follower.screen_name, searcher)
                
                if follower:
                    self.createIfNotFindFollow(user, follower)
            except:
                pass
            
        return True
    
    def convertFromSQLToGraph(self):
        
        InitDB()
        
        searcher = TwitterSearcher()
        '''
        for goods in GetAll(Goods):
            for product in goods:
                self.addProductToGraph(product)
        '''
        for users in GetAll(Persons):
            for user in users:
                self.addUserToGraph(user.twitterAccount,searcher)
    
    
       
#ConvertFromSQLToGraph()   