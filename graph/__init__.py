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
    value = String()

class GraphCategoriesLink(Relationship):
    label= 'categoriesLink'

#v = Vertex()

g.add_proxy("goods", GraphGoods)
g.add_proxy("category", GraphCategory)
g.add_proxy("categoriesLink", GraphCategoriesLink)

Session = sessionmaker(bind=engine)
session = Session()

def Depth(parent, tree, product):
    # toDo: добавить запись товара 
    print product
    if tree == {}:
        if parent:
            g.categoriesLink.create(parent, product)
            
    for key, val in tree.items():
        if key == '': 
            continue
        if key.find('\n') > 0:
            continue    
        print key
        category = g.category.create(value= unicodedata2.normalize('NFD',unicode(key )))  
      
        if parent:
            g.categoriesLink.create(parent,category)
        
        Depth(category, val, product)
    
            
num = session.query(func.count(Goods.url)).all()[0][0]
shift = 100

class Person(Node):
    element_type = "person"
    
    name = String(nullable=False)
    age = Integer()

g.add_proxy("people", Person)
james = g.people.create(name="James")
print james.eid
for i in xrange(0,num,shift):
    goods = session.query(Goods).filter(and_(Goods.id < i + shift, Goods.id >= i)).all()
    print goods

    for product in goods:
        rec = g.goods.create(
                             num = product.id,        
                             detail= unicodedata2.normalize('NFD',product.detail), 
                             name = unicodedata2.normalize('NFD',product.name), 
                             price = product.price, 
                             description = unicodedata2.normalize('NFD',product.description),
                             brand = unicodedata2.normalize('NFD',product.brand),
                             url = product.url
                             )
        
      
        Depth( None, 
               {'rootGoods':json.loads(product.category)}, 
                rec)


'''
 id | category | detail | name | price | description | brand | url 
----------+--------------------------------------------------------------------------------
  1 | {" Home & Kitchen ": {}} |  Levolor 14062 Window Hardware Brass| Levolor Curtain Rod Center Support Bracket 3-1/2" Projection Chrome |     0 |  14062 Features: -Product Type:Chain And Hooks. Dimensions: -Overall Height - Top to Botto
m:0.25 -Overall Width - Side to Side:3.25 -Overall Depth - Front to Back:7 -Overall Product Weight:0.06                                                                                                                                                                                                                                                    | Levolor              
           | http://www.amazon.com/Levolor-Curtain-Support-Bracket-Projection/dp/B000M3THTU
'''