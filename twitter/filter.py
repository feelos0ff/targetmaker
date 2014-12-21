# -*- coding: utf-8 -*-
'''
Created on 06 дек. 2014 г.

@author: feelosoff
'''

import requests
from parsers.text import TextProcess
import json

class TweeFilter(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.processor = TextProcess()
    
    def filter(self, tweet): 
        query = {"min_score": 1,
                 "query" : 
                    {
                        "query_string" : {
                            "fields" : ["brand","category"],
                            "query" : " ".join(self.processor.processing(tweet))
                        }
                    }
                 }
        response = requests.get("http://localhost:9200/tweezon/goods/_search", data=json.dumps(query))
        
        if json.loads(response.text)["hits"]["total"] > 1:
            return True

        return False
    
    def find(self, tweet):
        query = {"min_score": 1,
                 "query" : 
                    {
                        "query_string" : {
                            "fields" : ["brand","category", "name"],
                            "query" : " ".join(self.processor.processing(tweet))
                        }
                    }
                 }
        response = requests.get("http://localhost:9200/tweezon/goods/_search", data=json.dumps(query))
        
        if json.loads(response.text)["hits"]["total"] > 1:
            return json.loads(response.text)["hits"]["hits"][0]["_source"]

        return None
    