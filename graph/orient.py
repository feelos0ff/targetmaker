# -*- coding: utf-8 -*-
'''
Created on 12 авг. 2014 г.

@author: feelosoff
'''


from encodings.base64_codec import base64_decode,base64_encode
from requests.auth import HTTPBasicAuth
import requests


class OrientWrapper(object):
    def __init__(self):
        self.session = 0
        self.db = ''
        
    def connect(self, login, password, dbName):
      #  password =base64_encode(password)
        self.db = dbName
        response = requests.get('http://localhost:2480/connect/' +dbName,auth=HTTPBasicAuth(login, password))
        self.session = response.headers['OSESSIONID']
        
        return response