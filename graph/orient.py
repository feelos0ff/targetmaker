# -*- coding: utf-8 -*-
'''
Created on 12 авг. 2014 г.

@author: feelosoff
'''


from encodings.base64_codec import base64_decode,base64_encode
from requests.auth import HTTPBasicAuth
import requests
import json
#from requests import cookies


class OrientWrapper(object):
    def __init__(self):
        self.session = {}
        self.db = ''
        
    def connect(self, login, password, dbName):
        self.db = dbName
        response = requests.get('http://localhost:2480/connect/' +dbName,auth=HTTPBasicAuth(login, password))
        self.session = dict(OSESSIONID = response.cookies['OSESSIONID'])
        
        return response
    
    def display(self,entityType,subject):
        if entityType:
            url = ('http://localhost:2480/%s/%s/%s' %(entityType, self.db, subject))
        else:
            url = 'http://localhost:2480/listDatabases'
        
        return requests.get(url,cookies=self.session)
    
    def create(self, entityType,body,subject):
        url = ('http://localhost:2480/%s/%s/%s' %(entityType, self.db, subject))
        response = requests.post(url,data=json.dumps(body),cookies=self.session)
        
        return response
        
    def update(self,):
        pass