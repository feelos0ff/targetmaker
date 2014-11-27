# -*- coding: utf-8 -*-
'''
Created on 24 нояб. 2014 г.

@author: feelosoff
'''
import nltk
from nltk.corpus import stopwords
from nltk import wordnet 
import re
class TextProcess(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        self.pattern = re.compile(r"https?\S*")
        #(r"""~^(?:(?:https?|ftp|telnet)://(?:[a-z0-9_-]{1,32}(?::[a-z0-9_-]{1,32})?@)?)?(?:(?:[a-z0-9-]{1,128}\.)+(?:ru|su|com|net|org|mil|edu|arpa|gov|biz|info|aero|inc|name|[a-z]{2})|(?!0)(?:(?!0[^.]|255)[0-9]{1,3}\.){3}(?!0|255)[0-9]{1,3})(?:/[a-z0-9.,_@%&?+=\~/-]*)?(?:#[^ '\"&]*)?$~i""")

    
    def processing(self,text, ngramm = 1, syns = False):
        
        stops = stopwords.words('english')
        #print text
        try:
            text = self.pattern.sub(' ',text) 
        except Exception as e:
            print e
        #print text
        text = nltk.tokenize.wordpunct_tokenize(text.lower())
        text = [word
                for word in text 
                    if (not word in stops) and word.isalpha()]
        return ' '.join(text)
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
        '''
