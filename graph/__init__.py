# -*- coding: utf-8 -*-
'''
Created on 12 авг. 2014 г.

@author: feelosoff
'''
from bulbs.rexster import Graph
from bulbs.config import Config
from bulbs.model import Node, Relationship
from bulbs.property import Integer, String, Float
from tweepy.models import User

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
    
class GraphCategoryRoot(Node):
    element_type = 'categoryRoot'
    
class GraphCategoriesLink(Relationship):
    label= 'categoriesLink'
    name = String()



def InitGraph():
    global g
    global rootNode
    
    c = Config('http://localhost:8182/graphs/orientdbsample')
    g = Graph(config = c)

    g.add_proxy("categoryRoot", GraphCategoryRoot)
    g.add_proxy("goods", GraphGoods)
    g.add_proxy("category", GraphCategory)
    g.add_proxy("categoriesLink", GraphCategoriesLink)
    
    return g


def GetRoot(g):
    
    if not g.categoryRoot.get_all().next():
        rootNode = g.categoryRoot.create()
    else:
        rootNode = g.categoryRoot.get_all().next()

    return rootNode
    
