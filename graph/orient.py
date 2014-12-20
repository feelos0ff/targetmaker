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
            self.g.categoriesLink.create(parent, product, {'name': k})
            
        for key, val in tree.items():
            if key == '': 
                continue
            if key.find('\n') > 0:
                continue    
            
            k = unicodedata2.normalize('NFD',unicode(key )).strip()
            category = ''
            
            try:      
                for tmpE in self.g.categoriesLink.index.lookup(name = k):  
                    if tmpE._outV == parent.eid:
                        category = tmpE.outV() 
                        break
            except:
                pass     
            
            if category == '':
                category = self.g.category.create()  
                self.g.categoriesLink.create(parent,category, {'name':k})                
                        
            self.depth(category, val, product)
        
    def addProductToGraph(self,product):
        productFields = dict()
        
        for key, value in product.__dict__.items():
            if key != '_sa_instance_state':
                productFields[key]= value
        try:
            rec = self.g.goods.index.lookup(num = product.id)
            if rec:
                return
        except:
            pass
        
        rec = self.g.goods.create(
                              num = product.id,
                              brand  = product.brand,        
                              name = product.name
                            )
        productFields['idInGraph'] = rec.eid
        self.es.index(productFields,'tweezon','goods',product.id, bulk=True)
        self.depth( self.rootNode, 
               json.loads(product.category), 
               rec)
            
    def createIfNotFindFollow(self, user, follower):

        if user.inE():
            for inGraph in user.inE():
                if inGraph._inV == follower.eid:
                    return inGraph
        
        return self.g.follow.create(follower, user)
        
    def createIfNotFindUser(self, userLogin, searcher):
        try:
            inGraph = self.g.twitterUser.index.lookup(screen_name=userLogin)
        except:
            inGraph = None
        user = None
        
        if not inGraph:
            try:
                info = searcher.getPersonActions(userLogin)
            except Exception as e:
                if e.response.status == 401:
                    return None
                print e
                
            twitts = [self.es.index({'twitt' :stat.text , 'key' : userLogin},"twitter", "twitts")['_id']
                        for stat in info if self.tweeFilter.filter(stat.text)]
            
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
        except Exception as e:
            print e
            return False
        
        if not user:
            return False
          
        followers = searcher.getFollowers(screen_name=user.screen_name)
        
        for follower in followers:
            try:
                follower = self.createIfNotFindUser(follower.screen_name, searcher)
                
                if follower:
                    self.createIfNotFindFollow(user, follower)
            except Exception as e:
                print e
                pass
            
        return True
    
    def convertFromSQLToGraph(self):
        
        InitDB()
        
        searcher = TwitterSearcher()
        i = 0
   
        for goods in GetAll(Goods):
            for product in goods:
                try:
                    self.addProductToGraph(product)
                except Exception as e:
                    print e
                    pass
            print i 
            i += 100
        i = 0
        self.es.force_bulk()
        self.es.indices.refresh()
    
        for users in GetAll(Persons):
            for user in users:
                try:
                    self.addUserToGraph(user.twitterAccount,searcher)
                except:
                    pass
            print i 
            i += 100
        self.es.indices.refresh()   
        
if __name__ == '__main__':
    g = GraphWrapper() 
    g.convertFromSQLToGraph()               
