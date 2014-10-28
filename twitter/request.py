# -*- coding: utf-8 -*-
'''
Created on 18 окт. 2014 г.

@author: feelosoff
'''
import tweepy
from buildering.models import Persons
from parsers.location import LocationParser
from pyes.es import ES
from pyes.query import QueryStringQuery
import math

class TwitterSearcher(object):
    '''
    classdocs
    '''
    def __init__(self, params):
        self.locParse = LocationParser()
        self.es = ES('127.0.0.1:9200')
        self.api
        consumer_key = "mD68Xtt994xZPSQ7a6DuiyHmQ"
        consumer_secret = "FboATUEDCPOJLGNze0AryhEaFKqhRATEq8d9iPlZfVBOujDvqC"
        access_key="2692494289-7GJj6F2CdvmBtiZvcMV7YVxp3sQnDm7F62ymV0c"
        access_secret="ZjTgcHV8LuEIdbMU8KJxCw7kIJjtm5gU7VjwPlZWsEEaj"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.api=tweepy.API(auth)
        
    def createModel(self,description):
        pass
    
    def KulbakLeibler(self,model1, model2):
        pass
    
    def countdistance(self, amazon,twitter):
        distance = 2 * self.locParse(amazon.location, twitter.location)
        distance += self.KulbakLeibler(self.createModel(amazon.nickName), self.createModel(twitter.description)) 
        return distance
    
    def getSameUser(self, person):
        users = self.api.search_users(person.name)[:20]
        count = len(users)
        rankedUsers = []
        
        for i in xrange(count):
            distance = 3 * (count - i) / count * math.log(i) + self.countdistance(person, users[i])
            rankedUsers.append([users.screen_name, distance])
    
        rankedUsers.sort(key= lambda el: el[1])
        return rankedUsers[0][0]