# -*- coding: utf-8 -*-
'''
Created on 12 авг. 2014 г.

@author: feelosoff
'''

import pyorient

client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect( "root", "E8132024602821D045CBD3024FF7747A81FF36B19D111D9C24FA9076EFF86E94" )

client.db_open( 'tweezon', "root", "E8132024602821D045CBD3024FF7747A81FF36B19D111D9C24FA9076EFF86E94" )



