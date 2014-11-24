'''
Created on 23 нояб. 2014 г.

@author: feelosoff
'''

from graph import TweeUser
from graph import GraphGoods
from decision.shingle import Shingle
from buildering.models import Goods
from buildering.db import InitDB, GetAll
from parsers.text import TextProcess

class Decision(object):
    '''
    classdocs
    '''
    def __init__(self, params):
        '''
        Constructor
        '''
        self.shingles = Shingle()
        InitDB()
        
        for goods in GetAll(Goods):
            for product in goods:
                for i in xrange(1,4):
                    for value in product.__dict__.itervalues():
                        if type(value) == str:
                            self.shingles.addToShingle(
                                TextProcess().processing(
                                    value, i), product.id)

    def makeDecision(self,user): 
        tweets = user.getTweets()
        
        