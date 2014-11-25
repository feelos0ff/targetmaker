# -*- coding: utf-8 -*-
'''
Created on 24 нояб. 2014 г.

@author: feelosoff
'''
import nltk
from nltk.corpus import stopwords


class TextProcess(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        pass
    
    def processing(self,text, ngramm = 1):
        
        stops = stopwords.words('english')
        stemmer= nltk.PorterStemmer()
        
        text =nltk.tokenize.wordpunct_tokenize(text.lower())
        text = [stemmer.stem(word) for word in text if (not stemmer.stem(word) in stops) and (word.isalpha()) and (not word in stops)]
        text = nltk.ngrams(text,ngramm) 
    
        return nltk.Text(text).vocab()
    
    
