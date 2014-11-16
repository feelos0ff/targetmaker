# -*- coding: utf-8 -*-
'''
Created on 12 авг. 2014 г.

@author: feelosoff
'''

import json
from sqlalchemy.orm.session import sessionmaker
from buildering.models import engine, Goods, Persons
import unicodedata2
from graph import InitGraph,  GetRoot, TweeUser
from buildering.db import InitDB
from sqlalchemy.sql.expression import and_
from sqlalchemy import func
from twitter.request import TwitterSearcher    
import hotshot

g = InitGraph()
rootNode = GetRoot(g)

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

def AddUserToGraph(userLogin, searcher):
    inGraph = g.twitterUser.index.lookup(screen_name=userLogin)
    
    if not inGraph:
        info = searcher.getPersonActions(userLogin)
        twitts = [stat.text for stat in info]
        try:
            userName = info[0].author.name
            userLocation = info[0].author.location
        except Exception as e:
            print 'add user exc', e
            userName = ''
            userLocation = ''
        user = g.twitterUser.create( name = userName, 
                                     screen_name= unicodedata2.normalize('NFD',userName)[0:5000], 
                                     data = twitts, 
                                     location = unicodedata2.normalize('NFD',userLocation)[0:5000]
                                    )
    else:
        user = inGraph.next()
        
    followers = searcher.getPerson( inGraph.next().screen_name).followers()
    
    for follower in followers:
        inGraph = g.twitterUser.index.lookup(screen_name=follower.screen_name)
        # toDo бороться с дублированием кода
        info = searcher.getPersonActions(follower.screen_name)
        twitts = [stat.text for stat in info]
        try:
            userName = info[0].author.name
            userLocation = info[0].author.location
        except Exception as e:
            print 'add user exc', e
            userName = ''
            userLocation = ''
            
        if not inGraph:
            print userName, userLogin, userLocation
            try:
                follower = g.twitterUser.create( name = userName, 
                                     screen_name= unicodedata2.normalize('NFD',userName)[0:5000], 
                                     data = twitts, 
                                     location = unicodedata2.normalize('NFD',userLocation)[0:5000]
                                    )
            except Exception as e:
                print 'asdadsasd', e
                exit(0)
            g.follow.create(follower,user , {'name' : user.screen_name})
            
        else:
            if not inGraph.next().outE(label=user.screen_name):
                g.follow.create(follower,user , {'name' : user.screen_name})
            

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