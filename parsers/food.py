# -*- coding: utf-8 -*-
'''
Created on 05 авг. 2014 г.

@author: feelosoff
'''

class FoodParser(object):
    
    def __init__(self):
        pass
    def getGoods(self, fileName):
        good = set()
        fileFood = open( fileName, 'r')
        for line in fileFood:
            
            search = 'product/productId:'
            pos = line.find(search) 

            if pos != -1:
                good.add(line[pos + len(search):].strip())
        return good
