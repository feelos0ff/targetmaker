# -*- coding: utf-8 -*-
'''
Created on 30 авг. 2014 г.

@author: feelosoff
'''
import re
from buildering.models import Persons, Reviews, Goods
from datetime import datetime


class ReviewProductParser(object):

    def __init__(self):
        pass
    
    def getUrlPersonalReviews(self, html, strId):
        match = re.findall(r'/gp/cdp/member-reviews/.*sort_by=MostRecentReview', html.page_source)
        if match != None:
            return ['http://www.amazon.com' + url for url in match ]
        print "error : " + strId
        return None
    
    def getPages(self, html):
        pages = html.find_element_by_class_name('CMpaginate').find_elements_by_tag_name('a')
        
        res = { i.get_attribute('href') for i in pages }
        
        res.add(html.current_url)
        return list(res)
    

class ReviewPersonParser(object):

    def __init__(self):
        pass
    
    def getPersonInfo(self, html):
        
        line = html.find_element_by_class_name("h1").text[ len('Reviews Written by'): ]
        
        person = Persons()
        
        author = line[: line.find('(')]
        person.addAuthor(author)
        
        nation = line[line.find('(') : line.find(')')]
        person.location = nation.strip()
        
        return person
    
    def getPages(self, html):
        pages = html.find_elements_by_class_name('small')[-1].find_elements_by_tag_name('a')
        
        res = { i.get_attribute('href') for i in pages }
            
        res.add(html.current_url)
        return list(res)
    
    def getReviews(self, html):

        res = []
        
        body = html.find_elements_by_tag_name('tbody')[1]         
        text  = [txt.text for txt in body.find_elements_by_class_name('reviewText')]

        datePub = [d.text for d in body.find_elements_by_tag_name('nobr')]
        
        title = [ i.find_element_by_tag_name('b').text 
                 for i in body.find_elements_by_css_selector('div[style="margin-left:0.5em;"]')]    
        
        for i in xrange(len(text)) :
            
            review = Reviews()
            
            review.review = text[i]
            review.title = title[i]
    
            review.stars = 0.0
            print datePub[i]
            review.date_review = datetime.strptime( datePub[i], '%B %d, %Y')
                        
            res.append(review)
            
        return res

    def getUrlsGoods(self,html):
        body = html.find_elements_by_tag_name('tbody')[1] 
        return [ i.get_attribute('href') for i in body.find_elements_by_css_selector('span[class="h3color tiny"]+a') ]
    

class GoodsParser(object):
    
    def __init__(self):
        pass
    
    def getGoods(self, html):
        descriptions = html.find_elements_by_class_name('productDescriptionWrapper')
        description = ''
        
        for txt in descriptions:
            description = description + ' ' + txt.text
        
        details = []
        
        try:
            details = html.find_element_by_id('feature-bullets').find_elements_by_tag_name('li')
        except:
            details = []
        
        detail = ''
        
        for txt in details:
            detail = detail + ' ' + txt.text
        try: 
            salesRank = html.find_element_by_id('SalesRank').text
            salesRank = [[ salesRank[ salesRank.find('in') + len('in') : 
                                      salesRank.find('(' ) ] ]]
        except:
            salesRank = []
            
        bestSales = html.find_elements_by_class_name('zg_hrsr_ladder')
        
        for line in bestSales:
            bufferSales = []
            line = line.find_elements_by_tag_name('a')
        
            for elem in line:
                bufferSales.append(elem.text)
            
            salesRank.append(bufferSales)    
        
        try:
            brand = html.find_element_by_id('brand').text
        except:
            brand = 'unknown brand'
        try:
            name  = html.find_element_by_id('productTitle').text
        except:
            name  = 'unknown name'      
        try:
            price = html.find_element_by_id('priceblock_ourprice').text[1:]
        except:
            price = 0
            
        goods = Goods()
        
        for category in salesRank:
            goods.addGoods(category)
        
        goods.url = html.current_url
        goods.brand = brand
        goods.description = description
        goods.detail = detail
        goods.name = name
        goods.price = float(price)

        return goods
        