# -*- coding: utf-8 -*-
'''
Created on 12 авг. 2014 г.

@author: feelosoff
'''

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
from graph.orient import OrientWrapper

init_db()

client = pyorient.OrientDB("localhost", 2424)
session_id = OrientWrapper().connect( "root", "E8132024602821D045CBD3024FF7747A81FF36B19D111D9C24FA9076EFF86E94",'tweezon' )


if not client.db_exists( 'tweezon', pyorient.STORAGE_TYPE_PLOCAL ):
    client.db_create('tweezon', pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_PLOCAL )        
    client.command( "create class Goods extends V" )
    client.command( "create class Categories extends V" )
    client.command( "create class CategoriesLink extends E" )

else:
    client.db_open( 'tweezon', "root", "E8132024602821D045CBD3024FF7747A81FF36B19D111D9C24FA9076EFF86E94" )
tx = client.tx_commit()
#tx.begin()
#tx.commit()
clusters = client.db_reload()
clusters = {obj['name'] :obj for obj in clusters}

tx = client.tx_commit()

Session = sessionmaker(bind=engine)
session = Session()

def Depth(parent, tree, product):
    # toDo: добавить запись товара 
    print product
    if tree == {}:
        print product
        if parent:
            client.command( "create edge CategoriesLink from "+ parent.rid + " to "+product.rid )
    print tree.items()
    for key, value in tree.items():
        if key == '': 
            continue
        if key.find('\n') > 0:
            continue
        print "create vertex Categories set value = "+ key.encode('utf-8')
        
        id = client.command( 'create vertex Categories set value = "'+ re.sub(r'\W',' ',key.encode('utf-8')) +'"' )[0]
        print type(id)
        if parent:
            client.command( "create edge CategoriesLink from "+ parent.rid + " to "+id.rid )
        
        Depth(id, value, product)
    
            
            
#a = client.command( "create vertex Categories set value = 'azaza'")

#tx.begin()
num = session.query(func.count(Goods.url)).all()[0][0]
shift = 100
for i in xrange(0,num,shift):
    goods = session.query(Goods).filter(and_(Goods.id < i + shift, Goods.id >= i)).all()
    print goods
    for product in goods:
        rec = {'@goods':{'id' : product.id, 
                         'detail': product.detail, 
                         'name': product.name, 
                         'price':product.price, 
                         'description':product.description,
                         'brand':product.brand,
                         'url':product.url } }
        print json.dumps(rec)
        print ( "create vertex Goods set id = %d, detail ='%s',name='%s',description='%s', brand ='%s',url ='%s'"
                                 %(product.id,
                                   unicodedata2.normalize('NFD',product.detail),
                                   unicodedata2.normalize('NFD',product.name),
                                unicodedata2.normalize('NFD',product.description),
                                unicodedata2.normalize('NFD',product.brand),
                                unicodedata2.normalize('NFD', product.url)))
        #client.command("insert into Goods content {all:' hgh  ghj'}")
        while True:
            res = client.command( "create vertex Goods set id = %d, detail ='%s',name='%s',description='%s', brand ='%s',url ='%s'"
                                 %(product.id,
                                   unicodedata2.normalize('NFD',product.detail),
                                   unicodedata2.normalize('NFD',product.name),
                                unicodedata2.normalize('NFD',product.description),
                                unicodedata2.normalize('NFD',product.brand),
                                unicodedata2.normalize('NFD', product.url)))
            if res :
                break
        print res.rid 
        Depth( None, 
               {'rootGoods':json.loads(product.category)}, 
                res)
        
        print unicodedata2.normalize('NFD', product.category)
#res = tx.commit()

'''
 id | category | detail | name | price | description | brand | url 
----------+--------------------------------------------------------------------------------
  1 | {" Home & Kitchen ": {}} |  Levolor 14062 Window Hardware Brass| Levolor Curtain Rod Center Support Bracket 3-1/2" Projection Chrome |     0 |  14062 Features: -Product Type:Chain And Hooks. Dimensions: -Overall Height - Top to Botto
m:0.25 -Overall Width - Side to Side:3.25 -Overall Depth - Front to Back:7 -Overall Product Weight:0.06                                                                                                                                                                                                                                                    | Levolor              
           | http://www.amazon.com/Levolor-Curtain-Support-Bracket-Projection/dp/B000M3THTU
'''