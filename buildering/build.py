# -*- coding: utf-8 -*-
'''
Created on 30 авг. 2014 г.

@author: feelosoff
'''
import sys
sys.path.insert(0,'/home/feelosoff/workspace/targetmaker/buildering/')
sys.path.insert(0,'/home/feelosoff/workspace/targetmaker/')
    
from parsers.food import FoodParser 

from spiderStand.spider import Spider
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
        page.quit()
        
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
            print 'loads person reviews'               
            PersonReviewPages = rootSpider.load(urls)
            page.quit()
        else:
            PersonReviewPages = [page]
           
        urls = []    
            
        for reviewPage in PersonReviewPages:
            reviews += reviewPersonParser.getReviews(reviewPage)
            urls += reviewPersonParser.getUrlsGoods(reviewPage)
            reviewPage.quit()
            
        print 'loads goods'  
        goodsPages = rootSpider.load(urls)
        goods = ProcessGoodsPages(goodsPages)
        print 'set person'
        personInDB = session.query(Persons).filter(and_(Persons.name == person.name, Persons.nickName == person.nickName))
        
        if personInDB.scalar() > 0:
            continue
        
        session.add(person)
        session.commit()
        
        for i in xrange(len(goods)):
            reviews[i].product_id = goods[i].id
            reviews[i].person_id  = person.id
            print 'set product'
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

    for review in idReviews:
        urls = reviewProductParser.getPages(reviewSpider.load( [ review] )[0])  # урлы отзывов продуктов
        
        productReviewPages = rootSpider.load(urls)    # все страницы отзывов о продуктах
        
        for page in productReviewPages:
            urls = reviewProductParser.getUrlPersonalReviews(page, review) # урлы всех отзывов покупателей    
            page.quit() 
            print 'loads main pages' 
            ProcessPersonReview(rootSpider.load(urls))
     
   
if __name__ == '__main__':
    
    init_db()
   
    goods = FoodParser()
    
    idReviews = list(goods.getGoods('/home/feelosoff/foods.txt'))    # список отзывов продуктов 
    
    ProcessProductReview(idReviews)    