# -*- coding: utf-8 -*-
'''
Created on 30 авг. 2014 г.

@author: feelosoff
'''
import sys
from datetime import datetime

sys.path.insert(0,'/home/feelosoff/workspace/targetmaker/buildering/')
sys.path.insert(0,'/home/feelosoff/workspace/targetmaker/')
    

from twitter.request import TwitterSearcher

from parsers.food import FoodParser 

from spiderStand.spider import Spider, manager
from parsers.page import ReviewProductParser, ReviewPersonParser, GoodsParser

from buildering.models import  engine, Persons, Goods
from sqlalchemy.orm import sessionmaker
from db import init_db
from sqlalchemy import and_


def ProcessGoodsPages(goodsPages):
    goods = []
    goodsParser = GoodsParser()

    for page in goodsPages:
        try:
            goods.append(goodsParser.getGoods(page))
        except Exception as e:
            print 'goods parser ', e
        manager.Erase(page)
            
    return goods


def ProcessPersonReview(personReviewMainPages):
    rootSpider   = Spider('', '')
    Session = sessionmaker(bind=engine)
    searcher = TwitterSearcher()
    session = Session()
    reviewPersonParser  = ReviewPersonParser ()
    
    for page in personReviewMainPages:
        try:
            person = reviewPersonParser.getPersonInfo(page)
            urls = reviewPersonParser.getPages(page)
        except Exception as e:
            print 'person info err ', e
            manager.Erase(page)
            continue
        try:
            twittAcc = searcher.getSameUser(person)
            if not twittAcc:
                manager.Erase(page)
                continue
            person.twitterAccount = twittAcc
        except Exception as e:
            print ' error of twitter ', e
            manager.Erase(page)
            continue
        
            
        PersonReviewPages =[] 
        reviews = []
        
        if len(urls) > 0: 
            manager.Erase(page)#page.quit()
            print ('loads person reviews',   manager.count)               
            PersonReviewPages = rootSpider.load(urls)
        else:
            PersonReviewPages = [page]
           
        urls = []    
            
        for reviewPage in PersonReviewPages:
            try:
                reviews += reviewPersonParser.getReviews(reviewPage)
                urls += reviewPersonParser.getUrlsGoods(reviewPage)
                manager.Erase(reviewPage)
            except:
                manager.Erase(reviewPage)#reviewPage.quit()
                continue
            
        print ('loads goods',  manager.count)
        goods = []
        shift = 10
        
        for i in xrange(0,len(urls), shift):
            goodsPages = rootSpider.load(urls[i: min(i + shift, len(urls))])
            goods += ProcessGoodsPages(goodsPages)
        
        personInDB = session.query(Persons).filter(and_(Persons.name == person.name, Persons.nickName == person.nickName))
        
        if personInDB.scalar() > 0:
            continue
        
        session.add(person)
        session.commit()
        
        for i in xrange(len(goods)):
            reviews[i].product_id = goods[i].id
            reviews[i].person_id  = person.id
            goodsInDB = session.query(Goods).filter(Goods.url == goods[i].url)

            if goodsInDB.scalar() > 0:
                goods[i] = goodsInDB[0]
            else:
                session.add(goods[i])
                
            reviews[i].product = goods[i]
            reviews[i].person = person
            session.add(reviews[i])
        print 'saving'
        session.commit()
        

def ProcessProductReview(idReviews):
    
    reviewSpider = Spider('http://www.amazon.com/review/', '')
    rootSpider   = Spider('', '')
    
    reviewProductParser = ReviewProductParser()
#    точка предыдущей остановки
    idxStart =705# idReviews.index('B006K2ZZ7K')
    
    print (idxStart, len(idReviews))
    for review in idReviews[ idxStart: ]:
        print 'num in file',idReviews.index(review), datetime.now()
        manager.EraseAll()
        try:
            urls = reviewProductParser.getPages(reviewSpider.load( [ review] )[0])  # урлы отзывов продуктов
        
            productReviewPages = rootSpider.load(urls)    # все страницы отзывов о продуктах
        except Exception as e:
            print 'product error ', e
        for page in productReviewPages:
            
            try:
                urls = reviewProductParser.getUrlPersonalReviews(page, review) # урлы всех отзывов покупателей    
                manager.Erase(page)#page.quit() 
                print 'loads main pages' 
                ProcessPersonReview(rootSpider.load(urls))
            except Exception as e:
                try:
                    print ' goods review error parser ' + page.current_url , e
                except:
                    pass
                manager.Erase(page)
                continue
     
   
if __name__ == '__main__':
    
    init_db()
   
    goods = FoodParser()
    
    idReviews = list(goods.getGoods('../rsc/foods.txt'))    # список отзывов продуктов 
    
    ProcessProductReview(idReviews)    
