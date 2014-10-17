# -*- coding: utf-8 -*-
'''
Created on 18 окт. 2014 г.

@author: feelosoff
'''
from buildering.db import init_db
from buildering.models import engine, Country, Region, City
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import and_
from buildering import db

if __name__ == '__main__':
    init_db()
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    geo = open('../rsc/location.csv')
    for line in geo:
        line = eval(line)
        country = Country()
        region = Region()
        city = City()
        
        country.code = line[3]
        country.name = line[4]
        
        if line[5] == '' and line[6] == '':
            region.code = line[3]
            
        region.code  = line[5]
        region.name  = line[6]
        
        city.name    = line[7]
        
        countryInDB = session.query(Country).filter(and_(Country.code == country.code, 
                                                         Country.name == country.name))
        
        if countryInDB.scalar > 0 :           
            country = countryInDB[0]
        else:
            session.add(country)
            etc = Region()
            etc.code = country.code
            etc.country = country
            session.add(etc)
    
        regionInDB = session.query(Region).filter(and_(Region.code == region.code, 
                                                       Region.name == region.name,
                                                       Region().country == country))
        
        if regionInDB.scalar > 0 :           
            region = regionInDB[0]
        else:
            region.country = country
            session.add(region)
        
        city.region = region

        session.add(city)
        session.commit()
