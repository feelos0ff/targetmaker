# -*- coding: utf-8 -*-
'''
Created on 12 авг. 2014 г.

@author: feelosoff
'''
from bulbs.rexster import Graph
from bulbs.config import Config
from bulbs.model import Node, Relationship
from bulbs.property import Integer, String, Float,List
from tweepy.models import User
from pyes import ES
import bulbs


class GraphGoods(Node):
    element_type = 'goods'
    num = Integer()
    brand = String(indexed=True) 
    name  = String(indexed=True)
    
class GraphCategory(Node):
    element_type = 'category'

    
class GraphCategoryRoot(Node):
    element_type = 'categoryRoot'

    
class GraphCategoriesLink(Relationship):
    label= 'categoriesLink'
    name = String(indexed=True)


class TweeUser(Node):
    element_type = 'twitterUser'
    name = String(indexed=True)
    screen_name = String(indexed=True)
    data = List(indexed=True)
    location = String(indexed=True)
    idEl = String(indexed=True)

    def getTweets(self):
        es = ES('127.0.0.1:9200')
        res = []
        
        for tweetID in self.data:
            res += [es.get('twitter','twitts' , tweetID)['twitt']]

        return res

class Follow(Relationship):
    label= 'follow'
    name = String(indexed=True)
    


def InitGraph():   
    c = Config('http://localhost:8182/graphs/orientdbsample')
    g = Graph(config = c)

    mapping = {u'twitt': {'index': 'analyzed',
                          'store': 'yes',
                          'type': u'string',
                          "term_vector": "with_positions_offsets"},
               u'key':{'store': 'yes',
                       'type': u'string',
                       "term_vector": "with_positions_offsets"} 
    }
  
    es = ES('127.0.0.1:9200')
    
    try:
        es.indices.create_index("twitter")
        es.indices.put_mapping("twitts", {'properties': mapping}, "twitter")
    except:
        pass
    
    g.add_proxy("categoriesLink", GraphCategoriesLink)
    g.add_proxy("categoryRoot",   GraphCategoryRoot)
    
    g.add_proxy("twitterUser", TweeUser)
    g.add_proxy("category",    GraphCategory) 
 
    g.add_proxy("follow", Follow)
    g.add_proxy("goods",  GraphGoods)

    return g


def GetRoot(g):

    try:
        rootNode = g.categoryRoot.get_all().next()
    except:
        rootNode = g.categoryRoot.create()

    return rootNode
    
