# -*- coding: utf-8 -*-
'''
Created on 12 авг. 2014 г.

@author: feelosoff
'''
from bulbs.rexster import Graph,REXSTER_URI,Vertex,Edge
from bulbs.config import Config
import pyorient
from buildering.db import init_db
from buildering.models import Goods, engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm.query import Query
import json
from sqlalchemy.sql.expression import and_
from sqlalchemy import func
import sqlalchemy
import re
import unicodedata2
from bulbs.model import Node, Relationship
from bulbs.property import Integer, String, Float
#from graph.orient import OrientWrapper

init_db()

c = Config('http://localhost:8182/graphs/orientdbsample')
g = Graph(config = c)


class GraphGoods(Node):
    element_type = 'goods'
    num = Integer()
    detail = String()
    name = String()
    price = Float()
    description = String()
    brand = String()
    url = String()
    
class GraphCategory(Node):
    element_type = 'category'
    

class GraphCategoriesLink(Relationship):
    label= 'categoriesLink'
    name = String()


g.add_proxy("goods", GraphGoods)
g.add_proxy("category", GraphCategory)
g.add_proxy("categoriesLink", GraphCategoriesLink)

Session = sessionmaker(bind=engine)
session = Session()

client = g.client_class 

def Depth(parent, tree, product):
    if tree == {}:
        k = unicodedata2.normalize('NFD',unicode(product.name )).strip()
        e = g.categoriesLink.create(parent, product, {'name': k})
        
    for key, val in tree.items():
        if key == '': 
            continue
        if key.find('\n') > 0:
            continue    
        
        k = unicodedata2.normalize('NFD',unicode(key )).strip()

        category = ''
        
        if not parent.outE() or not (k in [i.name for i in parent.outE()]):
            category = g.category.create()  
            e = g.categoriesLink.create(parent,category, {'name':k})

        else:
            print k
            category = [i for i in parent.outE() if i.name == k][0].outV()           
        Depth(category, val, product)
    
            
num = session.query(func.count(Goods.url)).all()[0][0]
shift = 100

rootNode = g.category.create()
  
for i in xrange(0,num,shift):
    goods = session.query(Goods).filter(and_(Goods.id < i + shift, Goods.id >= i)).all()
    
    for product in goods:
        '''
        print len(unicodedata2.normalize('NFD',product.description))
        print ( product.id,unicodedata2.normalize('NFD',product.detail),
                unicodedata2.normalize('NFD',product.detail),
                product.price,
                unicodedata2.normalize('NFD',product.description),
                unicodedata2.normalize('NFD',product.brand),
                product.url)
        '''
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


'''
 id | category | detail | name | price | description | brand | url 
----------+--------------------------------------------------------------------------------
  1 | {" Home & Kitchen ": {}} |  Levolor 14062 Window Hardware Brass| Levolor Curtain Rod Center Support Bracket 3-1/2" Projection Chrome |     0 |  14062 Features: -Product Type:Chain And Hooks. Dimensions: -Overall Height - Top to Botto
m:0.25 -Overall Width - Side to Side:3.25 -Overall Depth - Front to Back:7 -Overall Product Weight:0.06                                                                                                                                                                                                                                                    | Levolor              
           | http://www.amazon.com/Levolor-Curtain-Support-Bracket-Projection/dp/B000M3THTU
'''