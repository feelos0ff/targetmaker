# -*- coding: utf-8 -*-

import requests
from requests.models import Response

'''
Created on 29 авг. 2014 г.

@author: feelosoff
'''

class Spider(object):
    def __init__(self, placeFrom, placeTo):
        self.placeFrom = placeFrom
        self.placeTo = placeTo
        self.num = 0
        
    def load(self,listUrls):
        badCount = 0
        result = []
        
        for url in listUrls:
            response = Response()
            print url
            while True:
                response = requests.get(self.placeFrom + url)
                if response.status_code == 200:
                    break
                if response.status_code == 404:
                    badCount += 1
                    break
            if len(response.text) == 0:
                badCount += 1
                continue
            
            if self.placeTo != '':
                fileOut = open(self.placeTo + str(self.num),'w')
                fileOut.write(response.text.encode('utf-8'))
                fileOut.close()
                self.num+=1
                
            else:
                result += [response.text.encode('utf-8')]
        
        print badCount
        return result
    