# -*- coding: utf-8 -*-
'''
Created on 11 сент. 2014 г.

@author: feelosoff
'''
from datetime import date
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import create_engine
import json


engine = create_engine('postgresql+psycopg2://postgres:password@localhost/amazon')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

class Persons(object):
    '''
    хранит пользовательскую информацию
    '''
    query = db_session.query_property()

    def __init__(self):
        self.name =''
        self.nickName = ''
        self.location =''
        
    def addAuthor(self, author):
        startNick = author.find('"')
        if(startNick < 0):
            self.name = author.strip()
        else:
            self.name = author[:startNick].strip()
        
        if startNick > 0:
            self.nickName = author[startNick + 1 :-1].strip()
        else:
            self.nickName = ''
            

class Goods(object):    
    '''
    хранит информацию о товарах
    '''
    query = db_session.query_property()

    def __init__(self):
        
        self.category = '{}'
        self.detail = ''
        self.name = ''
        self.price = ''
        self.description = ''
        self.brand = '' 
        self.url = ''    
    
    def addGoods(self, category):        
        categoryTree = json.loads(self.category)
        subTree = categoryTree
        depth = len(category)

        for i in xrange(depth):
            if not subTree.has_key(category[i]):
                subTree[category[i]] = dict()
            subTree = subTree[category[i]]
        
        self.category = json.dumps(categoryTree)


    def getGoods(self, category):
        if len(category) != 0:
            if category[0] in self.category:
                return self.category[category[0]]
        return self.category


class Reviews(object):
    '''
    хранит информацию об отзывах
    '''
    query = db_session.query_property()

    def __init__(self):
        self.review = ''
        self.stars = 0
        self.title = ''
        self.date_review = date(1,2,3)
        self.helpful = 0.0

class Country(object):
    query = db_session.query_property()

    def __init__(self):
        self.code = ''
        self.name = ''

class Region(object):
    query = db_session.query_property()

    def __init__(self):
        self.code = ''
        self.name = ''

class City(object):
    query = db_session.query_property()

    def __init__(self):
        self.name = ''
    
    