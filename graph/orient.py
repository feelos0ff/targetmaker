# -*- coding: utf-8 -*-
'''
Created on 12 авг. 2014 г.

@author: feelosoff
'''

import json
from sqlalchemy.orm.session import sessionmaker
from buildering.models import engine, Goods, Persons
import unicodedata2
from graph import InitGraph,  GetRoot
from buildering.db import InitDB
from sqlalchemy.sql.expression import and_
from sqlalchemy import func
from twitter.request import TwitterSearcher    
from pyes import ES

g = InitGraph()
rootNode = GetRoot(g)
es = ES('127.0.0.1:9200')

def Depth(parent, tree, product):
    if tree == {}:
        k = unicodedata2.normalize('NFD',unicode(product.name )).strip()
        g.categoriesLink.create(parent, product, {'label': k})
        
    for key, val in tree.items():
        if key == '': 
            continue
        if key.find('\n') > 0:
            continue    
        
        k = unicodedata2.normalize('NFD',unicode(key )).strip()
        category = ''
        
        if not parent.outE() or not parent.outE(k):
            category = g.category.create()  
            g.categoriesLink.create(parent,category, {'label':k})

        else:
            category = parent.outE(k).outV()             

        Depth(category, val, product)
    
    
def AddProductToGraph(product):

    rec = g.goods.create(
                          num = product.id,        
                          detail= unicodedata2.normalize('NFD',product.detail)[0:5000], 
                          name = unicodedata2.normalize('NFD',product.name)[0:5000], 
                          price = product.price, 
                          description = unicodedata2.normalize('NFD',product.description)[0:5000],
                          brand = unicodedata2.normalize('NFD',product.brand)[0:5000],
                          url = product.url[0:5000]
                        )
    Depth( rootNode, 
           json.loads(product.category), 
           rec)
    
    
def CreateIfNotFindFollow(user, follower):
    inGraph = user.inE(start=follower.eid)
    
    if (not inGraph) or (inGraph[0].outV() != user):
        return g.follow.create(user, follower)

    return inGraph[0]


def CreateIfNotFindUser(userLogin, searcher):
    inGraph = g.twitterUser.index.lookup(screen_name=userLogin)
    user = None
    
    if not inGraph:
        try:
            info = searcher.getPersonActions(userLogin)
        except Exception as e:
            if e.response.status == 401:
                return None
            print e
            
        twitts = [stat.text for stat in info]
        #toDo add inserting twitts into ES
        if len(twitts)< 5:
            return None
        
        try:
            userName = info[0].author.name
            userLocation = info[0].author.location

        except Exception as e:
            print 'add user exc', e
            userName = ''
            userLocation = ''
        
        user = g.twitterUser.create( name = userName, 
                                     screen_name= unicodedata2.normalize('NFD',unicode(userLogin))[0:5000], 
                                     data = twitts, 
                                     location = unicodedata2.normalize('NFD',unicode(userLocation))[0:5000]
                                    )
    else:
        user = inGraph.next()
    
    return user


def AddUserToGraph(userLogin, searcher):
    
    user = CreateIfNotFindUser(userLogin, searcher)  
    
    if not user:
        return False
      
    followers = searcher.getFollowers(screen_name=user.screen_name)
    
    for follower in followers:
        follower = CreateIfNotFindUser(follower.screen_name, searcher)
        
        if follower:
            CreateIfNotFindFollow(user, follower)

    return True

def ConvertFromSQLToGraph():
    
    InitDB()
    
    searcher = TwitterSearcher()
    Session = sessionmaker(bind=engine)
    session = Session()
    
    num = session.query(func.count(Goods.url)).all()[0][0]
    shift = 100

#    prof = hotshot.Profile("your_project.prof")
 #   prof.start()
    '''
    for i in xrange(0,100,shift):
        goods = session.query(Goods).filter(and_(Goods.id < i + shift, Goods.id >= i)).all()
        for product in goods:
            AddProductToGraph(product)
    '''
    num = session.query(func.count(Persons.id)).all()[0][0]

    for i in xrange(0,num,shift):
        users = session.query(Persons).filter(and_(Persons.id < i + shift, Persons.id >= i)).all()
        for user in users:
            AddUserToGraph(user.twitterAccount,searcher)

            
  #  prof.stop()
    
    
ConvertFromSQLToGraph()   