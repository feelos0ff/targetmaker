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
import hotshot

g = InitGraph()
rootNode = GetRoot(g)
#toDo необходимо запилить этот индекс 
#vertexIndex = g.client_class.create_vertex_index("")


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
    

def CreateIfNotFindUser(userLogin, searcher):
    inGraph = g.twitterUser.index.lookup(screen_name=userLogin)
    user = None
    
    if not inGraph:
        try:
            info = searcher.getPersonActions(userLogin)
        except Exception as e:
            if e.response.status == 401:
                return
            print e
            
        twitts = [stat.text for stat in info]
        
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
                                     location = unicodedata2.normalize('NFD',unicode(userLocation))[0:5000],
                                     index = 
                                    )
    else:
        user = inGraph.next()
    
    return user


def CreateIfNotFindFollow(user, follower):
    inGraph = user.inE(start=follower.eid,limit=1)
    
    if (not inGraph) or (inGraph[0].outV() != user):
        return g.follow.create(user, follower)

    return inGraph[0]


def AddUserToGraph(userLogin, searcher):
    
    user = CreateIfNotFindUser(userLogin, searcher)  
    
    if not user:
        return
      
    followers = searcher.getPerson( user.screen_name).followers()
    
    for follower in followers:
        follower = CreateIfNotFindUser(follower.screen_name, searcher)
            

def ConvertFromSQLToGraph():
    
    InitDB()
    
    searcher = TwitterSearcher()
    Session = sessionmaker(bind=engine)
    session = Session()
    
    num = session.query(func.count(Goods.url)).all()[0][0]
    shift = 100

    prof = hotshot.Profile("your_project.prof")
    prof.start()
    '''
    for i in xrange(0,100,shift):
        goods = session.query(Goods).filter(and_(Goods.id < i + shift, Goods.id >= i)).all()
        for product in goods:
            AddProductToGraph(product)
    '''
    num = session.query(func.count(Persons.id)).all()[0][0]
    
    for i in xrange(0,100,shift):
        users = session.query(Persons).filter(and_(Persons.id < i + shift, Persons.id >= i)).all()
        for user in users:
            AddUserToGraph(user.twitterAccount,searcher)
            
    prof.stop()
    
    
ConvertFromSQLToGraph()   