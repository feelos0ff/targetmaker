# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from random import randint
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
        self.headers = [
                        #'Opera/9.80 (X11; Linux x86_64; U; ru) Presto/2.2.15 Version/10.10', 
                       # "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 (KHTML, like Gecko) Chrome/15.0.87",
                        #"Mozilla/5.0 (X11; Linux x86_64; U; ru; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 10.10",
                        #"Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux x86_64; ru) Opera 10.10",
                       # "Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0",
                       # "Mozilla/5.0 (X11; Linux x86_64; U; ru; rv:1.8.1) Gecko/20061208 Firefox/2.0.0",
                        
                        #"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; ru)",
                       # "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36",
                        #"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
                        ]
        fileAgents = open("../rsc/userAgents.txt")

        for agent in fileAgents:
            self.headers.append(agent)
    
    def Erase(self, driver):
        try:
            self.freeDrivers.append(self.drivers.index(driver))
        except:
            print  'wow wow wow driver truble'
    def EraseAll(self):
        self.freeDrivers = range(self.count)
    
    def CreateDriver(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = self.headers[ randint(0,len(self.headers)-1) ]
       # print dcap["phantomjs.page.settings.userAgent"]
        driver = webdriver.PhantomJS()#desired_capabilities=dcap)
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)

        return driver
            
    def GetDriver(self):
        if self.freeDrivers == []:
            
            self.drivers.append(self.CreateDriver())
            
            self.count += 1
            
            return self.drivers[-1]
            
        idx = self.freeDrivers.pop()
        return self.drivers[idx]
    
    def RestartDriver(self, driver):
        num = self.drivers.index(driver)            

        self.drivers[num].close()
        self.drivers[num] = self.CreateDriver()
        
        return self.drivers[num]
        
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
                    driver = manager.GetDriver()
                except Exception as e:
                    print "can't open driver ", e
                    continue
                
                try:
                    driver.get(self.placeFrom + url)
                except Exception as e:
                    print 'driver exception ', e 
                    
                    driver = manager.RestartDriver(driver)
                    sleep(1)
                    continue
                
               # print driver.current_url
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
                    '''
                    fileOut = open(self.placeTo + str(self.num),'w')
                    fileOut.write(driver.page_source.encode('utf-8'))
                    fileOut.close()
                    self.num+=1
                    '''
                    result += [driver]
                break
    
        return result
    