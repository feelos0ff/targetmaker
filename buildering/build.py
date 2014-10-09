# -*- coding: utf-8 -*-
'''
Created on 30 авг. 2014 г.

@author: feelosoff
'''

from parsers.food import FoodParser 

from spiderStand.spider import Spider
from parsers.page import ReviewProductParser, ReviewPersonParser

from buildering.models import Persons, Goods, Reviews, engine
from sqlalchemy.orm import sessionmaker
from db import init_db


def ProcessGoodsPages(goodsPages):
    pass

def ProcessPersonReview(personReviewMainPages):
    amazonSpider = Spider('http://www.amazon.com/','')
    rootSpider   = Spider('', '')
    
    reviewPersonParser  = ReviewPersonParser ()
    
    for page in personReviewMainPages:
        person = reviewPersonParser.getPersonInfo(page)
        urls = reviewPersonParser.getPages(page)
            
        PersonReviewPages =[] 
        PersonReviews = []
        if len(urls) > 0:                
            PersonReviewPages = amazonSpider.load(urls)
        else:
            PersonReviewPages = [page]
           
        urls = []    
            
        for reviewPage in PersonReviewPages:
            PersonReviews += reviewPersonParser.getReviews(reviewPage)
            urls += reviewPersonParser.getUrlsGoods(reviewPage)
        
        goodsPages = rootSpider.load(urls)
        goods = ProcessGoodsPages(goodsPages)
    


def ProcessProductReview(idReviews):
    
    reviewSpider = Spider('http://www.amazon.com/review/', '')
    amazonSpider = Spider('http://www.amazon.com/','')
    rootSpider   = Spider('', '')
    
    reviewProductParser = ReviewProductParser()

    for review in idReviews:
        urls = reviewProductParser.getPages(reviewSpider.load( [ review] )[0])  # урлы отзывов продуктов
        
        productReviewPages = rootSpider.load(urls)    # все страницы отзывов о продуктах
        personReviewMainPages = []
        
        for page in productReviewPages:
            urls = reviewProductParser.getUrlPersonalReviews(page, review) # урлы всех отзывов покупателей    
            personReviewMainPages += rootSpider.load(urls)
        
     
   
if __name__ == '__main__':
    init_db()
    Session = sessionmaker(bind=engine)
    
    pers = Persons()

    session = Session()
    session.add(pers)
    session.commit()
   
    goods = FoodParser()
    
    idReviews = ['B0024V8PSC']#list(goods.getGoods('/home/feelosoff/foods.txt'))    # список отзывов продуктов 
    
    ProcessProductReview(idReviews)    