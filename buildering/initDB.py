# -*- coding: utf-8 -*-
'''
Created on 18 окт. 2014 г.

@author: feelosoff
'''
from buildering.db import InitDB
from buildering.models import engine, Countries, Regions, Cities
from sqlalchemy.orm.session import sessionmaker
import re
from pyes import ES


if __name__ == '__main__':
    InitDB()
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    es = ES('127.0.0.1:9200')
    es.indices.create_index("tweezon")
    
    mapping = {u'country_code': {'boost': 1.0,
                                'index': 'analyzed',
                                'store': 'yes',
                                'type': u'string',
                                "term_vector": "with_positions_offsets"},
                u'country_name': {'boost': 1.0,
                                'index': 'analyzed',
                                'store': 'yes',
                                'type': u'string',
                                "term_vector": "with_positions_offsets"},
                u'region_code': {'boost': 5.0,
                                'index': 'analyzed',
                                'store': 'yes',
                                'type': u'string',
                                "term_vector": "with_positions_offsets"},
                u'region_name': {'boost': 5.0,
                                'index': 'analyzed',
                                'store': 'yes',
                                'type': u'string',
                                "term_vector": "with_positions_offsets"},
                u'city_name': {'boost': 1.0,
                                'index': 'analyzed',
                                'store': 'yes',
                                'type': u'string',
                                "term_vector": "with_positions_offsets"},
    }
    es.indices.put_mapping("geo", {'properties': mapping}, "tweezon")
    
    mapping = {u'name': {'boost': 5.0,
                                'index': 'analyzed',
                                'store': 'yes',
                                'type': u'string',
                                "term_vector": "with_positions_offsets"},
                u'detail': {'boost': 1.0,
                                'index': 'analyzed',
                                'store': 'yes',
                                'type': u'string',
                                "term_vector": "with_positions_offsets"},
               
                u'description': {'boost': 5.0,
                                'index': 'analyzed',
                                'store': 'yes',
                                'type': u'string',
                                "term_vector": "with_positions_offsets"},
                u'brand': {'boost': 5.0,
                                'index': 'analyzed',
                                'store': 'yes',
                                'type': u'string',
                                "term_vector": "with_positions_offsets"},
                u'url': {'boost': 2.0,
                                'index': 'analyzed',
                                'store': 'yes',
                                'type': u'string',
                                "term_vector": "with_positions_offsets"},
                u'category': {'boost': 4.0,
                                'index': 'analyzed',
                                'store': 'yes',
                                'type': u'string',
                                "term_vector": "with_positions_offsets"},
                u'idInGraph': {'boost': 0.1,
                                'index': 'analyzed',
                                'store': 'yes',
                                'type': u'string',
                                "term_vector": "with_positions_offsets"},               
        }
    
    es.indices.put_mapping("goods", {'properties': mapping}, "tweezon")
    
    geo = open('../rsc/locations.csv')
    num = 0
    for line in geo:
        num +=1
        line = line.replace('"', '')
        line = [i[1:].strip() for i in re.findall(r',[^,]*', line)]

        region = Regions()
        city = Cities()
        
        country = Countries()
        country.code = line[2]
        country.name = line[3]
        
        if line[4] == '' and line[5] == '':
            region.code = line[2]
        else:   
            region.code  = line[4]
            region.name  = line[5]
        
        city.name    = line[6]
        
        res = es.index({'country_code' : country.code, 'country_name' : country.name,
                        'region_code' : region.code, 'region_name' : region.name, 'city_name':line[6]},"tweezon", "geo", num)
        
        print res
  
    es.indices.refresh()
    geo.close()