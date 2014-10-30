# -*- coding: utf-8 -*-
'''
Created on 11 сент. 2014 г.

@author: feelosoff
'''
from datetime import date
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import create_engine
import json
from sqlalchemy.sql.expression import and_


engine = create_engine('postgresql+psycopg2://postgres:password@localhost/tweezon')
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
        self.twitterAccount = ''
        
    def addAuthor(self, author):
        startNick = author.find('"')
        if(startNick < 0):
            self.name = author.strip()
        else:
            self.name = author[:startNick].strip()
        
        if startNick > 0:
            
            self.nickName = author[startNick + 1 :].strip()
            stopNick = self.nickName.find('"')
            self.nickName = author[:stopNick].strip()
        else:
            self.nickName = ''
    def __unicode__(self):
        return  self.name + ' '  + self.nickName + ' ' +  self.location  + ' ' +  self.twitterAccount 
   
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


class Countries(object):
    query = db_session.query_property()
    
    def __init__(self):
        self.code = ''
        self.name = ''
        
    def checkLoc(self, session, line, location):
        try:
            self = session.query(Countries).get_by(name=line)
            return True
        except:
            pass
        try:
            self = session.query(Countries).get_by(code=line)
            return True
        except:
            pass
        
        return False

class Regions(object):
    query = db_session.query_property()

    def __init__(self):
        self.code = ''
        self.name = ''

    def checkLoc(self, session, line, location):
        try:
            if location[0].code != '': 
                self = session.query(Regions).get_by(and_(Regions.name==line, Countries.code==location[0].code))
                print session.query(Regions).get_by(and_(Regions.name==line, Countries.code==location[0].code))
            else :
                self = session.query(Regions).filter_by(name=line).first()
            
            return True
        
        except:
            pass
        try:
            if location[0].code != '':
                self = session.query(Regions).get_by(and_(Regions.code==line, Countries.code==location[0].code))
                print session.query(Regions).get_by(and_(Regions.code==line, Countries.code==location[0].code))
            else :
                self = session.query(Regions).filter_by(code=line).first()
            
            return True
        except:
            pass
        
        return False

class Cities(object):
    query = db_session.query_property()

    def __init__(self):
        self.name = ''
    
    def checkLoc(self, session, line, location):
        try:
            if location[1].name != '': 
                self = session.query(Regions).get_by(and_(Regions.name==line, Countries.code==location[0].code))
                print session.query(Regions).get_by(and_(Regions.name==line, Countries.code==location[0].code))
            else :
                self = session.query(Regions).filter_by(name=line).first()
            
            return True
        
        except:
            pass
        try:
            if location[0].code != '':
                self = session.query(Regions).get_by(and_(Regions.code==line, Countries.code==location[0].code))
                print session.query(Regions).get_by(and_(Regions.code==line, Countries.code==location[0].code))
            else :
                self = session.query(Regions).filter_by(code=line).first()
            
            return True
        except:
            pass
        
        return False