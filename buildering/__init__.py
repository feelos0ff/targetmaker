# -*- coding: utf-8 -*-
import Levenshtein
print Levenshtein.jaro('cat','cetss')
print Levenshtein.jaro('cat','cets')
print Levenshtein.jaro('cat','cet')
print Levenshtein.jaro('cat','cats')
print Levenshtein.jaro('cat','ctss')
'''
from nltk.corpus import stopwords
import nltk


stops = stopwords.words('english')
text =nltk.tokenize.wordpunct_tokenize("cat is a cast of cats which cat's dog dog's cast") 
stemmer= nltk.PorterStemmer()
text = [stemmer.stem(word) for word in text if not stemmer.stem(word) in stops]
txt = nltk.Text(text)
print len(txt)
for key,val in txt.vocab().items():
    print txt.vocab()['azaza']

nltk.Text(text)
'''