'''
Created on 23 нояб. 2014 г.

@author: feelosoff
'''
import random

class Shingle(object):
    
    def __init__(self):
        self.shingles = [dict()]        # таблица шинглов хранятся в дикте тольк ненулевые значения
        self.replaces = [[]]            # таблица перестановок
        self.minHash  = [[{}]]          # таблица хэшей. хранится помимо позиции еще и вес
        self.countShingles = 0          # количество шинглов
        self.shingleMap = dict()        # словарь соответствия шингла номеру
        self.docs = []

    def addToShingle(self, data, docName):
        dataShingles = dict()
        
        for key, value in data.items:
            num = self.countShingles

            if self.shingleMap.get(key,-1) == -1:
                self.shingleMap[key] = num
                self.countShingles += 1
            else:
                num = self.shingleMap[key]
            
            dataShingles[num]=value
        
        if not docName in self.docs:
            self.shingles.append(dataShingles)
        
        else:
            num = self.docs.index(docName)
            for key, value in dataShingles.items():
                self.shingles[num][key] = self.shingles[num].get(key,0) + value
        
    def doMinHashing(self,numReplace):
        cols = len(self.shingles)
        
        self.replaces = [[]]          
        self.minHash  = [[{}]]          
        self.shingleMap = dict()        
        
        for i in xrange(numReplace):
            
            seq = range(self.countShingles)
            random.shuffle(seq)
            self.replaces.append(seq)
            seq = []
                        
            for j in xrange(cols):
                for k in xrange(self.countShingles):
                    pos = self.replaces[i][k]
                    value = self.shingles[j].get(pos, 0)
                    
                    if value == 0:
                        continue
                    
                    seq.append( {'pos':k,'value':value} )
                    break
            
            self.minHash.append(seq)
        
            
    def getMinHash(self,data):
        data = { self.shingleMap[key]:value  
                    for key, value in data.items() 
                        if self.shingleMap.get(key,-1) != -1 }
        res = []
        
        for replace in self.replaces:
            for i in xrange(self.countShingles):
                value = data.get(replace[i], 0)
                
                if value == 0:
                    continue
                
                res.append({'pos':i,'value':value})
                break
        
        return res
