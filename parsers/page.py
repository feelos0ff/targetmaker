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
        match = re.findall(r'/gp/cdp/member-reviews/.*sort_by=MostRecentReview', html)
        if match != None:
            return match
        print "error : " + strId
        return None
    
    def getPages(self, html):
        match = re.search(r'Previous.*Next', html)
        if match == None:
            print "error"
            return []
        prevNextStr = match.group()
        return re.findall(r'http://www.amazon.com.*sortBy=byRankDescending', prevNextStr) 
    

class ReviewPersonParser(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        pass
    
    def getPersonInfo(self, html):
        match = re.search(r'Reviews Written by <br /> .*</b>', html)
        line = match.group()[ len('Reviews Written by <br /> '): ]
        if line == None:
            return None
        
        person = Persons()
        
        author = line[: line.find(' <span class=')]
        person.addAuthor(author)
        
        nation = line[line.find('</span>') + len('</span>') : line.find('</b>')]
        person.location = nation.strip()
        
        return person
    
    def getPages(self, html):
        match = re.search(r'Page:.*</div>', html)
        if match == None:
            print 'error'
            return []
        prevNextStr = match.group()
        return re.findall(r'/gp/cdp/member-reviews.*sort_by=MostRecentReview', prevNextStr) 
    
    def getReviews(self, html):
        headText  = r'<div class="reviewText">'
        tailText  = r'</div>'
        
        headStars = r'stars" title="'
        tailStars = r'out'
        
        headDate  = r'<nobr>'
        tailDate  = r'</nobr>'
        
        headTitle = '<b>'
        tailTitle = '</b>, <nobr>'
        
        res = []
        
        text  = re.findall(headText  + r'.*' + tailText,  html)
        stars = re.findall(headStars + r'.*' + tailStars, html)
        title = re.findall(headTitle + r'.*' + tailTitle, html)
        datePub = re.findall(headDate + r'.*' + tailDate, html) 
        
        for i in xrange(len(text)) :
            
            review = Reviews()
            review.review = text[i][ len(headText) : 
                                   ( len(text[i]) - len(tailText) ) ]
            
            review.stars = float(stars[i][ len(headStars) : 
                                         ( len(stars[i]) - len(tailStars) ) ])
            
            review.date_review = datetime.strptime( datePub[i][ len(headDate) :
                                                            ( len(datePub[i]) - len(tailDate))],
                                                   '%B %d, %Y')
            
            review.title = title[i][ len(headTitle[i]) :
                                   ( len(title[i]) - len(tailTitle))]
            
            res.append(review)
        return res

    def getUrlsGoods(self,html):
        return re.findall(r'http://www.amazon.com/.*/dp/.*ref=cm_cr-mr-title',html)
    

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
        