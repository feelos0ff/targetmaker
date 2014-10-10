# -*- coding: utf-8 -*-
'''
Created on 19 сент. 2014 г.

@author: feelosoff
'''
import sys
from sqlalchemy import ForeignKey

sys.path.insert(0,'/home/feelosoff/workspace/TargetMaker/buildering/')
sys.path.insert(0,'/home/feelosoff/workspace/TargetMaker/')

from buildering.models import Goods, Persons, Reviews, engine
from sqlalchemy.schema import Column, Table, Sequence, MetaData
from sqlalchemy.orm import mapper, relation
from sqlalchemy.types import String, Float, Integer, DateTime
from sqlalchemy.dialects.postgresql import ARRAY

def init_db():
    metadata = MetaData()
    
    persons = Table('person', metadata,
        Column('id', Integer, Sequence('person_id_seq'), primary_key=True),
        Column('name', String()),
        Column('nickName', String()),
        Column('location', String())
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
    
    
    mapper(Persons, persons, properties={
    'reviews': relation(Reviews, backref='person'),})
    mapper(Goods, goods, properties={
    'reviews': relation(Reviews, backref='product'),})
    mapper(Reviews, reviews)
    
    metadata.create_all(bind=engine)
