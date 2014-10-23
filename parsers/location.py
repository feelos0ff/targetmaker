# -*- coding: utf-8 -*-
'''
Created on 22 окт. 2014 г.

@author: priora
'''
from buildering.models import Countries, Regions, Cities, engine
from sqlalchemy.orm import sessionmaker
from elasticsearch.client import Elasticsearch
from pyes.es import ES
from pyes.query import TermsQuery, TermQuery, Search, WildcardQuery



class LocationParser(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        pass
    
    def parse(self, address):
        
        Session = sessionmaker(bind=engine)
        session = Session() 
        
        parts = [ line.split(' ') for line in address.split(',')].reverse()
        location = [Countries(), Regions(), Cities()]
        
        for levelLoc in location:
            for part in parts:
                partLen = len(part)
                
                for windowLen in xrange(partLen, 0, -1):
                    
                    for windowPos in xrange(partLen -windowLen, -1, -1):
                        forCheck = ''
                        for wordNum in xrange(windowLen):
                            forCheck = forCheck + part[wordNum + windowPos]
                            
                        if(levelLoc.checkLoc(session, forCheck, location)):
                            break
                    else:
                        continue
                    break
            else:
                if isinstance(levelLoc,Regions):
                    levelLoc.checkLoc(session, '', location)
                continue
            break
        

def toElastic():
    es = Elasticsearch()
    rsc = open('../rsc/locations.csv')
    i = 0
    for line in rsc:
        res = es.index(index="test-index", doc_type='tweet', id=i,body={'geo':line})
        i += 1
        print(res['created'])
        
es = ES('127.0.0.1:9200')

res = TermQuery('country_code', 'us')
res = es.search(query =res,indices ="geo-index")
#res  = es.get("geo-index", "geo", 2)
print res.total
for x in res:
    print x
        