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
        self.exceptionTable = {'usa': ' United States ', 'us':' United States ', 'nyc':' New York ', 'uk':' United Kingdom '}
        self.es = ES('127.0.0.1:9200')

    def parse(self, address):
        address = address.encode('utf-8').strip()
        if address != '':
            try:
                address = address.lower()
                
                for key, val in self.exceptionTable.items():
                    address = re.sub(r'(^|\W)'+key+'(\W|$)',val,address)
                    address = re.sub(r'\W',' ',address)
                #print address
                res = QueryStringQuery(address)
                res = self.es.search(query =res,indices ="geo-index")
                
                return res[0]
            except:
                print 'location err ' + address
            
        return {'country_code' : '', 'region_code' :'', 'city_name' :''}
        
    def distance(self,addr1, addr2):
        
        if  addr1 == {'country_code' : '', 'region_code' :'', 'city_name' :''} or addr2 == {'country_code' : '', 'region_code' :'', 'city_name' :''}:
            return 3
        
        if addr1['country_code'] != addr2['country_code']:
            return 3
        
        if len(addr1) == 1 or len(addr2) == 1 or addr1['region_code'] != addr2['region_code']:
            return 2
        
        if len(addr1) > 2 and len(addr2) > 2 and addr1['city_name'] != addr2['city_name']:
            return 1
        return 0

'''
es = LocationParser()
print es.parse('nyc nyc')
print es.parse('ny')
print es.parse('n')
print es.parse(' ')
print es.parse('')
print es.parse('bg')
print es.parse('uk')
print es.parse('uka')
print es.parse('usa')
print es.parse('us')
print es.parse('god-save.\/()*&^%!@@#$%^&*({}":><us')

print es.parse('US->BG->GB')
'''