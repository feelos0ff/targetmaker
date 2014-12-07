# -*- coding: utf-8 -*-
'''
Created on 06 дек. 2014 г.

@author: feelosoff
'''

import requests

class TweeFilter(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
    
    def filter(self, tweet):
        query = {
                    "query_string" : {
                        "default_field" : [""],
                        "query" : "this AND that OR thus"
                    }
                }
        return True