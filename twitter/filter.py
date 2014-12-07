# -*- coding: utf-8 -*-
'''
Created on 06 дек. 2014 г.

@author: feelosoff
'''

import requests
from parsers.text import TextProcess

class TweeFilter(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        self.processor = TextProcess()
    
    def filter(self, tweet):
        tweet = " OR ".join(self.processor.processing(tweet))
        query = {
                    "query_string" : {
                        "min_score": 0.5,
                        "default_field" : ["brand","category"],
                        "query" : tweet
                    }
                }
        response = requests.get("http://localhost:9200/twitter/goods/_search", params=query)
        
        if response["hits"]["total"] > 1:
            return True
        
        return False
    