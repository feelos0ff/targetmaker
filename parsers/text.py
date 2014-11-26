# -*- coding: utf-8 -*-
'''
Created on 24 нояб. 2014 г.

@author: feelosoff
'''
import nltk
from nltk.corpus import stopwords
from nltk import wordnet 

class TextProcess(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        pass
    
    def processing(self,text, ngramm = 1, syns = False):
        
        stops = stopwords.words('english')
        stemmer= nltk.PorterStemmer()
        
        text = nltk.tokenize.wordpunct_tokenize(text.lower())
        '''
        for word in text:
            if wordnet.wordnet.morphy(word) == 'chrome':
                print text
        '''
        normalizing = (lambda w: wordnet.wordnet.morphy(w) if wordnet.wordnet.morphy(w) else stemmer.stem(w))
        
        text = [normalizing(word)
                for word in text 
                    if isinstance(word, unicode) and
                        (not wordnet.wordnet.morphy(word) in stops) 
                     #   and (word.isalpha()) 
                        and (not word in stops)]
        
        if syns and ngramm == 1:
            try:
                res = []
                for word in text:
                    syn = wordnet.wordnet.synsets(word)
                    for w in syn:
                        res += w.lemma_names()
                text = list(set(res))
            except:
                pass
            
            text = [normalizing(word) 
                    for word in text 
                        if isinstance(word, unicode) and
                            (not wordnet.wordnet.morphy(word) in stops)  
                            and (not word in stops)]
           # print text
        text = [stemmer.stem(w) for w in text if w.isalpha()]
        text = nltk.ngrams(text,ngramm) 
    
        return nltk.Text(text).vocab()
       
