# -*- coding: utf-8 -*-

from selenium import webdriver
'''
Created on 29 авг. 2014 г.

@author: feelosoff
'''
from posix import wait
from time import sleep


class Spider(object):
    def __init__(self, placeFrom, placeTo):
        
        self.placeFrom = placeFrom
        self.placeTo = placeTo
        self.num = 0
        
    def load(self,listUrls):
        badCount = 0
        result = []
        lastUrls = set()
        for url in listUrls:
            print url
            for i in xrange(10):
                try:
                    driver = webdriver.PhantomJS()
                    driver.get(self.placeFrom + url)
                except:
                    print 'driver exception' 
                    sleep(1)
                    continue
                
                if driver.current_url in lastUrls:
                    badCount += 1
                    break           
                
                lastUrls.add(driver.current_url)
                
                if self.placeTo != '':
                    fileOut = open(self.placeTo + str(self.num),'w')
                    fileOut.write(driver.page_source.encode('utf-8'))
                    fileOut.close()
                    
                    self.num+=1
                    driver.quit()
                    
                else:
                    result += [driver]
                break
        
        print badCount
        return result
    