# -*- coding: utf-8 -*-
'''
Created on 12 авг. 2014 г.

@author: feelosoff
'''
import pyorient


client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect( "root", "9017CA15222093A14E41CB8A32527E61099711B5E902F07D72F4E3B479163971" )
client.db_open( "testsox",  "root", "9017CA15222093A14E41CB8A32527E61099711B5E902F07D72F4E3B479163971"  )

if __name__ == '__main__':
    pass