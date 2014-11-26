# -*- coding: utf-8 -*-
'''
Created on 19 сент. 2014 г.

@author: feelosoff
'''
import sys
from sqlalchemy import ForeignKey
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.elements import and_

sys.path.insert(0,'/home/feelosoff/workspace/TargetMaker/buildering/')
sys.path.insert(0,'/home/feelosoff/workspace/TargetMaker/')

from buildering.models import Goods, Persons, Reviews, engine, Countries, Regions,\
    Cities
from sqlalchemy.schema import Column, Table, Sequence, MetaData
from sqlalchemy.orm import mapper, relation
from sqlalchemy.types import String, Float, Integer, DateTime

def InitDB():
    metadata = MetaData()
    
    persons = Table('person', metadata,
        Column('id', Integer, Sequence('person_id_seq'), primary_key=True),
        Column('name', String()),
        Column('nickName', String()),
        Column('location', String()),
        Column('twitterAccount', String())
    )
    
    
    goods = Table ('goods', metadata,
        Column('id', Integer, Sequence('good_id_seq'), primary_key=True),
        Column('category', String()),
        Column('detail', String()),
        Column('name', String()),
        Column('price',Float()),
        Column('description', String()),
        Column('brand', String()),
        Column('url', String())   
    )
    
    
    reviews = Table('reviews', metadata,
        Column('id',Integer, Sequence('review_id_seq'), primary_key=True),
        Column('review', String()),
        Column('stars', Float()),
        Column('title', String()),
        Column('date_review', DateTime()),
        Column('helpful', Float()),
        Column('person_id',  ForeignKey('person.id')),
        Column('product_id', ForeignKey('goods.id'))
    )
    
    city = Table('city', metadata,
        Column('id' ,Integer, Sequence('city_id_seq'), primary_key=True),
        Column('name', String()),
        Column('region_id',  ForeignKey('region.id'))
    )
    
    region = Table('region', metadata,
        Column('id' ,Integer, Sequence('region_id_seq'), primary_key=True),
        Column('code', String()),
        Column('name', String()),
        Column('country_id',  ForeignKey('country.id'))
    ) 
    
    country = Table('country', metadata,
        Column('id' ,Integer, Sequence('country_id_seq'), primary_key=True),
        Column('code', String()),
        Column('name', String())
    )
    
    mapper(Countries, country, properties={
    'region': relation(Regions, backref='country'),})
    mapper(Regions, region, properties={
    'city': relation(Cities, backref='region'),})
    mapper(Cities, city)
    
    mapper(Persons, persons, properties={
    'reviews': relation(Reviews, backref='person'),})
    mapper(Goods, goods, properties={
    'reviews': relation(Reviews, backref='product'),})
    mapper(Reviews, reviews)
    
    metadata.create_all(bind=engine)


def GetAll(objType, shift = 100):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    num = session.query(func.count(objType.id)).all()[0][0]
    
    for i in xrange(0,num,shift):
        yield session.query(objType).filter(and_(objType.id < i + shift, objType.id >= i)).all()

def GetNum(objType,num):
    Session = sessionmaker(bind=engine)
    session = Session()    
    print num, objType
    return session.query(objType).filter(objType.id  == num).all()[0]
