# -*- coding: utf-8 -*-

import requests
from requests.models import Response
from selenium import webdriver
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
            print url
            
            driver = webdriver.PhantomJS()
            
            
            driver.get(self.placeFrom + url)
                
            if driver.current_url() != self.placeFrom + url:
                badCount += 1
                continue              
            
            if self.placeTo != '':
                fileOut = open(self.placeTo + str(self.num),'w')
                fileOut.write(driver.text.encode('utf-8'))
                fileOut.close()
                
                self.num+=1
                driver.quit()
                
            else:
                result += [driver]
        
        print badCount
        return result
    