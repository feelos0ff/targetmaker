# -*- coding: utf-8 -*-
'''
Created on 12 авг. 2014 г.

@author: feelosoff
'''

from bulbs.config import Config
from bulbs.rexster import Graph, Edge, Vertex
from bulbs.rexster.client import REXSTER_URI


#Edge()
#Vertex()
c = Config('http://localhost:8182/graphs/orientdbsample')
g = Graph(c)

james = g.vertices.create(name="James")
julie = g.vertices.create(name="Julie")
g.edges.create(james, "knows", julie)

if __name__ == '__main__':
    pass