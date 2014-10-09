# -*- coding: utf-8 -*-
'''
Created on 30 авг. 2014 г.

@author: feelosoff
'''

from parsers.food import FoodParser 

from spiderStand.spider import Spider
from parsers.page import ReviewProductParser, ReviewPersonParser, GoodsParser

from buildering.models import Persons, Goods, Reviews, engine
from sqlalchemy.orm import sessionmaker
from db import init_db


def ProcessGoodsPages(goodsPages):
    goods = []
    goodsParser = GoodsParser()

    for page in goodsPages:
        goods.append(goodsParser.getGoods(page))

    return goods


def ProcessPersonReview(personReviewMainPages):
    rootSpider   = Spider('', '')
    
    reviewPersonParser  = ReviewPersonParser ()
    
    for page in personReviewMainPages:
        person = reviewPersonParser.getPersonInfo(page)
        urls = reviewPersonParser.getPages(page)
            
        PersonReviewPages =[] 
        reviews = []
        if len(urls) > 0:                
            PersonReviewPages = rootSpider.load(urls)
        else:
            PersonReviewPages = [page]
           
        urls = []    
            
        for reviewPage in PersonReviewPages:
            reviews += reviewPersonParser.getReviews(reviewPage)
            urls += reviewPersonParser.getUrlsGoods(reviewPage)
        
        goodsPages = rootSpider.load(urls)
        goods = ProcessGoodsPages(goodsPages)
        
        for i in len(goods):
            reviews[i].product_id = goods[i]
            reviews[i].person_id  = person
            reviews.save()


def ProcessProductReview(idReviews):
    
    reviewSpider = Spider('http://www.amazon.com/review/', '')
    rootSpider   = Spider('', '')
    
    reviewProductParser = ReviewProductParser()

    for review in idReviews:
        urls = reviewProductParser.getPages(reviewSpider.load( [ review] )[0])  # урлы отзывов продуктов
        
        productReviewPages = rootSpider.load(urls)    # все страницы отзывов о продуктах
        personReviewMainPages = []
        
        for page in productReviewPages:
            urls = reviewProductParser.getUrlPersonalReviews(page, review) # урлы всех отзывов покупателей    
            personReviewMainPages += rootSpider.load(urls)

        ProcessPersonReview(personReviewMainPages)
     
   
if __name__ == '__main__':
    init_db()
    Session = sessionmaker(bind=engine)
    
    pers = Persons()

    session = Session()
    session.add(pers)
    session.commit()
   
    goods = FoodParser()
    
    idReviews = list(goods.getGoods('/home/feelosoff/foods.txt'))    # список отзывов продуктов 
    
    ProcessProductReview(idReviews)    