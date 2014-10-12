# -*- coding: utf-8 -*-
'''
Created on 30 авг. 2014 г.

@author: feelosoff
'''
import sys
import math
sys.path.insert(0,'/home/feelosoff/workspace/targetmaker/buildering/')
sys.path.insert(0,'/home/feelosoff/workspace/targetmaker/')
    
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
        goods.append(goodsParser.getGoods(page))
        manager.Erase(page)#page.quit()
        
    return goods


def ProcessPersonReview(personReviewMainPages):
    rootSpider   = Spider('', '')
    Session = sessionmaker(bind=engine)

    session = Session()
    reviewPersonParser  = ReviewPersonParser ()
    
    for page in personReviewMainPages:
        person = reviewPersonParser.getPersonInfo(page)
        urls = reviewPersonParser.getPages(page)
            
        PersonReviewPages =[] 
        reviews = []
        if len(urls) > 0: 
            manager.Erase(page)#page.quit()
            print 'loads person reviews'               
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
            
        print 'loads goods'  
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
    idxStart = idReviews.index('B001D07IPG')

    for review in idReviews[ idxStart: ]:
        urls = reviewProductParser.getPages(reviewSpider.load( [ review] )[0])  # урлы отзывов продуктов
        
        productReviewPages = rootSpider.load(urls)    # все страницы отзывов о продуктах
        
        for page in productReviewPages:
            try:
                urls = reviewProductParser.getUrlPersonalReviews(page, review) # урлы всех отзывов покупателей    
                manager.Erase(page)#page.quit() 
                print 'loads main pages' 
                ProcessPersonReview(rootSpider.load(urls))
            except:
                print 'goods review error parser ' + page.current_url
                manager.Erase(page)
                continue
     
   
if __name__ == '__main__':
    
    init_db()
   
    goods = FoodParser()
    
    idReviews = list(goods.getGoods('/home/feelosoff/foods.txt'))    # список отзывов продуктов 
    
    ProcessProductReview(idReviews)    