# -*- coding: utf-8 -*-
'''
Created on 18 окт. 2014 г.

@author: feelosoff
'''
import tweepy
from Levenshtein import jaro, jaro_winkler
from buildering.models import Persons
from parsers.location import LocationParser
from pyes.es import ES
from nltk.corpus import stopwords
import nltk
from math import log

class TwitterSearcher(object):
    '''
    classdocs
    '''
    def __init__(self):
        self.locParse = LocationParser()
        self.es = ES('127.0.0.1:9200')
       
        consumer_key = "mD68Xtt994xZPSQ7a6DuiyHmQ"
        consumer_secret = "FboATUEDCPOJLGNze0AryhEaFKqhRATEq8d9iPlZfVBOujDvqC"
        
        access_key="2692494289-7GJj6F2CdvmBtiZvcMV7YVxp3sQnDm7F62ymV0c"
        access_secret="ZjTgcHV8LuEIdbMU8KJxCw7kIJjtm5gU7VjwPlZWsEEaj"
       
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
       
        self.api=tweepy.API(auth)
        
    def createModel(self,description):
        stops = stopwords.words('english')
        stemmer= nltk.PorterStemmer()
        
        text =nltk.tokenize.wordpunct_tokenize("cat is a cast of cats which cat's dog dog's cast") 
        text = [stemmer.stem(word) for word in text if not stemmer.stem(word) in stops]
        
        return nltk.Text(text)
    
    def getChance(self,count, size):
        return (float(count) +1) / (size + 1)
    
    def KulbakLeibler(self,model1, model2):
        distance = 0
        
        lenMod1 = len(model1)
        lenMod2 = len(model2)
        
        for word, count in model1.vocab().items():
            p = self.getChance(count, lenMod1)
            q = self.getChance(model2.vocab()[word],lenMod2) 
            distance += p * log(p)/log(q)

        return distance
    
    def countDistance(self, amazon,twitter):
        distance = 0        
        amazonModel = self.createModel(amazon.nickName)
        twitterModel =  self.createModel(twitter.description)
        
        distance += self.KulbakLeibler(amazonModel,twitterModel) 
        distance += self.KulbakLeibler(twitterModel,amazonModel) 
        
        return distance
    
    def getSameUser(self, person):
        users = self.api.search_users(person.name)[:20]
        count = len(users)
        rankedUsers = []
        
        for i in xrange(count):
            distanceName =  max( jaro(person.name.lower(), users[i].screen_name.lower()), 
                                 jaro(person.name.lower(), users[i].name.lower()) ) * (count - i) / count
            distanceDescription = self.countDistance(person, users[i])
            
            tweeAddr = self.locParse.parse(users[i].location)
            amazonAddr = self.locParse.parse(person.location)
            distanceLocation =  (3 -self.locParse.distance(amazonAddr,tweeAddr) ) / 3.0

            rankedUsers.append([users[i], distanceName, distanceLocation, distanceDescription])
    
        rankedUsers.sort(key= lambda el: 3* el[1] + 2 * el[2] + el[3])
        for usr in rankedUsers:
            if len(usr[0].followers()) < 5:
                continue
            if usr[2] < 0.3 and usr[0][3] < 0.2 and usr[1] < 0.5:
                return None
          
            return usr[0].screen_name

        return None
