# -*- coding: utf-8 -*-
'''
Created on 12 авг. 2014 г.

@author: feelosoff
'''

import json
from sqlalchemy.orm.session import sessionmaker
from buildering.models import engine, Goods
import unicodedata2
from graph import InitGraph,  GetRoot
from buildering.db import InitDB
from sqlalchemy.sql.expression import and_
from sqlalchemy import func

g = InitGraph()
rootNode = GetRoot(g)

def Depth(parent, tree, product):
    if tree == {}:
        k = unicodedata2.normalize('NFD',unicode(product.name )).strip()
        g.categoriesLink.create(parent, product, {'name': k})
        
    for key, val in tree.items():
        if key == '': 
            continue
        if key.find('\n') > 0:
            continue    
        
        k = unicodedata2.normalize('NFD',unicode(key )).strip()
        category = ''
        
        if not parent.outE() or not (k in [i.name for i in parent.outE()]):
            category = g.category.create()  
            g.categoriesLink.create(parent,category, {'name':k})

        else:
            category = [i for i in parent.outE() if i.name == k][0].outV()             

        Depth(category, val, product)
    
def ConvertFromSQLToGraph():
    InitDB()
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    num = session.query(func.count(Goods.url)).all()[0][0]
    shift = 100
    import hotshot
    prof = hotshot.Profile("your_project.prof")
    prof.start()
    for i in xrange(0,500,shift):
        goods = session.query(Goods).filter(and_(Goods.id < i + shift, Goods.id >= i)).all()
        count = 1
        for product in goods:
            AddProductToGraph(product)
            print i + count
            count +=1
        
        
        
    prof.stop()
    
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


ConvertFromSQLToGraph()   