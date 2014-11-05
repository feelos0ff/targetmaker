# -*- coding: utf-8 -*-
'''
Created on 12 авг. 2014 г.

@author: feelosoff
'''

import pyorient
from buildering.db import init_db
from buildering.models import Goods, engine
from sqlalchemy.orm.session import sessionmaker
import json


init_db()

client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect( "root", "E8132024602821D045CBD3024FF7747A81FF36B19D111D9C24FA9076EFF86E94" )


if not client.db_exists( 'tweezon', pyorient.STORAGE_TYPE_PLOCAL ):
    client.db_create('tweezon', pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_PLOCAL )
    tx = client.tx_commit()
    tx.begin()
    client.command( "create class Goods extends V" )
    client.command( "create class Categories extends V" )
    client.command( "create class CategoriesLink extends E" )
    tx.commit()
else:
    client.db_open( 'tweezon', "root", "E8132024602821D045CBD3024FF7747A81FF36B19D111D9C24FA9076EFF86E94" )

clusters = client.db_reload()
clusters = {obj['name'] :obj for obj in clusters}

tx = client.tx_commit()

Session = sessionmaker(bind=engine)
session = Session()

def Depth(parent, tree, product):
    # toDo: добавить запись товара 
    if tree.empty():
        client.command( "create vertex Goods set value =")
        if parent:
            client.command( "create edge CategoriesLink from "+ parent.rid + " to "+id.rid )
    
    for key, value in tree:
        id = client.command( "create vertex Categories set value = "+ key )[0]
        if parent:
            client.command( "create edge CategoriesLink from "+ parent.rid + " to "+id.rid )
        
        Depth(id[0], value)
            
            
            
a = client.command( "create vertex Categories set value = 'azaza'")

tx.begin()
goods = session.query(Goods).all()
for product in goods:
    categories = json.loads(product.category)
    Depth(None, categories, product)
    
tx.commit()
'''
 id | category | detail | name | price | description | brand | url 
----------+--------------------------------------------------------------------------------
  1 | {" Home & Kitchen ": {}} |  Levolor 14062 Window Hardware Brass| Levolor Curtain Rod Center Support Bracket 3-1/2" Projection Chrome |     0 |  14062 Features: -Product Type:Chain And Hooks. Dimensions: -Overall Height - Top to Botto
m:0.25 -Overall Width - Side to Side:3.25 -Overall Depth - Front to Back:7 -Overall Product Weight:0.06                                                                                                                                                                                                                                                    | Levolor              
           | http://www.amazon.com/Levolor-Curtain-Support-Bracket-Projection/dp/B000M3THTU
'''