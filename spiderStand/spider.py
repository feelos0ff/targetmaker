# -*- coding: utf-8 -*-

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
        lastUrls = set()
        for url in listUrls:
            print url
            while True:
                try:
                    driver = webdriver.PhantomJS()
                    driver.get(self.placeFrom + url)
                except Exception as err:
                    print 'driver exception' + str(err)
                    continue
                
                if driver.current_url in lastUrls:
                    badCount += 1
                    break           
                
                lastUrls.add(driver.current_url)
                
                if self.placeTo != '':
                    fileOut = open(self.placeTo + str(self.num),'w')
                    fileOut.write(driver.text.encode('utf-8'))
                    fileOut.close()
                    
                    self.num+=1
                    driver.quit()
                    
                else:
                    result += [driver]
                break
        
        print badCount
        return result
    