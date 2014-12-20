# -*- coding: utf-8 -*-
'''
Created on 23 нояб. 2014 г.

@author: feelosoff
'''
import random
'''
class Shingle(object):
    
    def __init__(self):
        self.shingles = []            # таблица шинглов хранятся в дикте тольк ненулевые значения
        self.replaces = []            # таблица перестановок
        self.minHash  = []            # таблица хэшей. хранится помимо позиции еще и вес
        self.countShingles = 0        # количество шинглов
        self.shingleMap = dict()      # словарь соответствия шингла номеру
        self.docs = []
        self.enShingleMap = dict()

    def addToShingle(self, data, docName):
        dataShingles = dict()
        
        for key, value in data.items():
            num = self.countShingles

            if self.shingleMap.get(key,-1) == -1:
                self.shingleMap[key] = num
                self.countShingles += 1
                self.enShingleMap[num] = key
            else:
                num = self.shingleMap[key]
            
            dataShingles[num]=value
        
        if not docName in self.docs:
            self.shingles.append(dataShingles)
            self.docs.append(docName)
        else:
            num = self.docs.index(docName)
            for key, value in dataShingles.items():
                self.shingles[num][key] = self.shingles[num].get(key,0) + value
        
    def doMinHashing(self,numReplace):
        cols = len(self.shingles)
        
        numReplace = min(numReplace, self.countShingles)
        
        self.replaces = []          
        self.minHash  = []                 

        for i in xrange(numReplace):
            
            seq = range(self.countShingles)
            random.shuffle(seq)
            self.replaces.append(seq)
            
            print len(seq)
            print len(self.replaces)
            
            hashVal = []
            
            for j in xrange(cols):
                for pos in self.replaces[-1]:                    
                    value = self.shingles[j].get(pos, 0)
                    if value == 0:
                        continue
                    
                    hashVal.append( {'pos':pos,'value':value} )
                    break

            self.minHash.append(hashVal)
        self.minHash = zip(*self.minHash)

    def getMinHash(self,model):
        data = { self.shingleMap[key]:value  
                    for key, value in model.items() 
                        if self.shingleMap.get(key,-1) != -1 }
        print len(data)
        res = []
        
        for replace in self.replaces:
            for pos in replace:
                value = data.get(pos, 0)
                
                if value == 0:
                    continue
                
                res.append({'pos':pos,'value':value})
                break
        
        return res
'''