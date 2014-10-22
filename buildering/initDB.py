# -*- coding: utf-8 -*-
'''
Created on 18 окт. 2014 г.

@author: feelosoff
'''
from buildering.db import init_db
from buildering.models import engine, Countries, Regions, Cities
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import and_
import re



if __name__ == '__main__':
    init_db()
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    geo = open('../rsc/locations.csv')
    
    for line in geo:
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
       
        countryInDB = session.query(Countries).filter(and_(Countries.code == country.code, 
                                                         Countries.name == country.name))
        
        if countryInDB.count() > 0 :
                       
            country = countryInDB[0]
        else:
            session.add(country)
            etc = Regions()
            etc.code = country.code
            etc.country = country
            session.add(etc)
    
        regionInDB = session.query(Regions).filter(and_(Regions.code == region.code, 
                                                        Regions.name == region.name, 
                                                        Countries.code == country.code,
                                                        Countries.name == country.name))
        if regionInDB.count() > 0 :           
            region = regionInDB[0]
        else:
            region.country = country
            session.add(region)

        city.region = region

        session.add(city)
        session.commit()  