# -*- coding: utf-8 -*-

from selenium import webdriver
'''
Created on 29 авг. 2014 г.

@author: feelosoff
'''

from time import sleep


class ConnectManager(object):
    def __init__(self):
        self.count = 0
        self.freeDrivers = []
        self.drivers = []
    
    def Erase(self, driver):
        self.freeDrivers.append(self.drivers.index(driver))
    
    def GetDriver(self):
        if self.freeDrivers == []:
            self.drivers.append(webdriver.PhantomJS())
            self.freeDrivers.append(self.count)
            self.count += 1
            
        idx = self.freeDrivers.pop()
        return self.drivers[idx]
         
manager = ConnectManager()

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
            for i in xrange(10):
                try:
                    driver = manager.GetDriver()#webdriver.PhantomJS()
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
    
        return result
    