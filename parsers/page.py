# -*- coding: utf-8 -*-
'''
Created on 30 авг. 2014 г.

@author: feelosoff
'''
import re
from buildering.models import Persons, Reviews
from datetime import datetime


class ReviewProductParser(object):
    '''
    classdocs
    '''

    def __init__(self):
        pass
    
    def getUrlPersonalReviews(self, html, strId):
        match = re.findall(r'/gp/cdp/member-reviews/.*sort_by=MostRecentReview', html.text)
        if match != None:
            return match
        print "error : " + strId
        return None
    
    def getPages(self, html):
        pages = html.find_element_by_class_name('CMpaginate').find_elements_by_tag_name('a')
        
        res = { i.get_attribute('href') for i in pages }
        
        res.add(html.current_url)
        return list(res)
    

class ReviewPersonParser(object):
    '''
    classdocs
    '''
    
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
        
        tr = body.find_elements_by_tag_name('tr')
        tr = [ tr[i] for i in xrange(1, len(tr),3)]
        
        text  = [txt.text 
                    for txt in body.find_elements_by_class_name('reviewText') ]
        
        title = [i.find_element_by_tag_name('b').text 
                    for i in tr]
        
        stars = [re.findall(r'\d\.\d', 
                            i.find_element_by_tag_name('img').get_attribute('title') )[0]
                                for i in tr]
        
        datePub = [i.find_element_by_tag_name('nobr').text 
                    for i in tr]
        
        for i in xrange(len(text)) :
            
            review = Reviews()
            
            review.review = text[i]
            review.title = title[i]
            
            review.stars = float(stars[i])
            review.date_review = datetime.strptime( datePub[i], '%B %d, %Y')
                        
            res.append(review)
            
        return res

    def getUrlsGoods(self,html):
        body = html.find_elements_by_tag_name('tbody')[1] 
        
        tr = body.find_elements_by_tag_name('tr')
        tr = [ tr[i] for i in xrange(0, len(tr),3)]
        
        return [i.find_element_by_tag_name('a').get_attribute('href') for i in tr] 
    

class GoodsParser(object):
    def __init__(self):
        pass
    def getGoods(self, html):
        headTitle = r'<span id="productTitle" class="a-size-large">'
        tileTitle = r'</span>'
        
        headBrand = r'<a id="brand"'
        tileBrand = r'</a>'
        
        headPrice = r'<span id="priceblock_ourprice"'
        tilePrice = r'</span>'
        
        headDescr = r''
        