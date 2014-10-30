# -*- coding: utf-8 -*-
'''
Created on 22 окт. 2014 г.

@author: priora
'''

from pyes.es import ES
from pyes.query import QueryStringQuery
import re

class LocationParser(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.exceptionTable = {'usa': 'United States', 'us':'United States'}
        self.es = ES('127.0.0.1:9200')

    def parse(self, address):
        try:
            address = address.lower()
            
            for key, val in self.exceptionTable.items():
                address = re.sub(r'\W'+key+'\W',val,address)
            
            res = QueryStringQuery(address)
            res = self.es.search(query =res,indices ="geo-index")
            
            return res[0]
        except:
            print "error location " +address
        
        return {'country_code' : '', 'region_code' :'', 'city_name' :''}
        
    def distance(self,addr1, addr2):
        
        if addr1['country_code'] != addr2['country_code']:
            return 3
        
        if len(addr1) == 1 or len(addr2) == 1 or addr1['region_code'] != addr2['region_code']:
            return 2
        
        if len(addr1) > 2 and len(addr2) > 2 and addr1['city_name'] != addr2['city_name']:
            return 1
        return 0
    
        