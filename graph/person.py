# -*- coding: UTF-8 -*-
'''
Created on 18 авг. 2014 г.

@author: feelosoff
'''

import tweepy, sys, locale, threading 
from time import localtime, strftime, sleep
from tweepy.models import Status


replyed=['']
search_reply_words={'печалька':' каждый раз, когда вы говорите "печалька", умирают хомячки.','пичалька':' каждый раз, когда вы говорите "пичалька", умирают хомячки.'}
update_time=60 #время обновления

def Tweet(twit,id_reply):
    if len(twit)<=140 and len(twit)>0:
        api.update_status(twit,id_reply) #обновляем статус (постим твит)
        return True
    else:
        return False

def init(): #инициализируемся
    global api
    consumer_key = "mD68Xtt994xZPSQ7a6DuiyHmQ"
    consumer_secret = "FboATUEDCPOJLGNze0AryhEaFKqhRATEq8d9iPlZfVBOujDvqC"
    access_key="2692494289-7GJj6F2CdvmBtiZvcMV7YVxp3sQnDm7F62ymV0c"
    access_secret="ZjTgcHV8LuEIdbMU8KJxCw7kIJjtm5gU7VjwPlZWsEEaj"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api=tweepy.API(auth)
    

class TwiBot(threading.Thread): 
    def __init__ (self, keyword,answer):
        self.keyword = keyword
        self.answer=answer
        threading.Thread.__init__(self)

    def run (self):
        global replyed,api
        request=api.search(self.keyword) #ищем твиты с указанным словом
        for i in request:
            print i
            
            '''
            if i.from_user!='thevar1able' and i.id not in replyed: # если твит не наш и мы на него еще не отвечали...
                try:
                    Tweet('@'+i.from_user+self.answer,i.id) #...отвечаем
                    print strftime('[%d/%m %H:%M:%S]',localtime())+' Reply to @'+i.from_user+'('+str(i.from_user_id)+')'
                except:
                    print strftime('DUP [%d/%m %H:%M:%S]',localtime())+' Reply to @'+i.from_user+'('+str(i.from_user_id)+')'
                replyed.append(i.id)
                '''
        return True



init() # инициализируемся
u = tweepy.models.User()

users = api.search_users('Natalia Corres')[:5]


 #users = api.user_timeline('@delmartian')

for user in users:
    print user.location, user.screen_name, user.description

    
   # for friend in user.friends():
   #     print friend.screen_name
'''
while not False: # вечно
    for word in search_reply_words: 
        TwiBot(word, search_reply_words[word]).start() #запускаем поток с нужным словом для поиска
        print strftime('[%d/%m %H:%M:%S]',localtime())+' Updating for word "'+str(word)+'"...'
        sleep(1) 


class Twit(object):
    def __init__(self):
        self.text
        self.owner
        self.date
        
      
class TwitterUser(object):
    def __init__(self):
        self.followers
        self.twits
        self.retwits
        self.friends

'''