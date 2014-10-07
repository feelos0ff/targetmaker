# -*- coding: utf-8 -*-
'''
Created on 11 сент. 2014 г.

@author: feelosoff
'''
from datetime import date
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import create_engine


engine = create_engine('postgresql+psycopg2://feelosoff:password@localhost/amazon')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

class Persons(object):
    '''
    хранит пользовательскую информацию
    '''
    query = db_session.query_property()

    def __init__(self):
        self.nickName = ''
        self.name =''
        self.location =''
        
    def addAuthor(self, author):
        startNick = author.find('"')
        self.name = author[:startNick]
        
        if startNick > 0:
            self.nickName = author[startNick + 1 :-1]
        else:
            self.nickName = ''
            

class Goods(object):    
    '''
    хранит информацию о товарах
    '''
    query = db_session.query_property()

    def __init__(self, category=[]):
        
        self.category = {}
        self.detail = ''
        self.name = ''
        self.price = ''
        self.description = ''
        self.brand = ''
        
        if len(category) != 0:
            self.category[category[0]] = self.addGood(category[1:])
    
    def addGoods(self, category):
        if len(category) != 0:
            self.category[category[0]] = Goods(category[1:])
    
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
        self.date_review = date()
        self.helpful = 0.0
        self.person_id = Persons()
        self.good_id = Goods()
    
