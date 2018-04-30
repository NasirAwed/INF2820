import nltk
from nltk.corpus import movie_reviews
from sklearn.cross_validation import train_test_split
from nltk.classify import NaiveBayesClassifier
import nltk.metrics
from nltk.metrics.scores import precision
from nltk.metrics.scores import recall
from nltk.metrics.scores import f_measure
import random
import warnings
import collections
import time


def document_features(word_features, document):
    document_words= set(document)
    features= {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words) #True or False
    return features

y = [("1dfas"),("2asdffsda"),("fsdaaf3"),("afafsd4"),("afsdfads5"),("fasdasfd6"),("afsdf7"),"asdffasd8","afsdafsd9","10","11","12","13","14","15","16","17","18","19","20"]
x,z =train_test_split(y, test_size= 2)
dev_set = x
test_set = y

from nltk.tokenize import word_tokenize # or use some other tokenizer

all_words = set(word.lower() for passage in dev_set for word in word_tokenize(passage[0]))
t = [({word: (word in word_tokenize(x[0])) for word in all_words}, x[1]) for x in dev_set]




classifier2= nltk.NaiveBayesClassifier.train(dev_set)
z = nltk.classify.accuracy(classifier2,test_sent_features)
print(x)
print(z)

























"""n_fold = 10
train_set = y
test_set = []

for x in range(n_fold):
    start = int(len(y)/n_fold * x)
    end = int(len(y)/n_fold*(x + 1))

    print("x={}, start={}, end={}".format(x, start, end))

    t_train_set = train_set[:start]+train_set[end:]
    t_test_set = train_set[start:end]

    print(t_test_set)
    print(t_train_set)
    print()
"""
"""

def n_fold(featuresets, tall):
    featuresets2 = featuresets
    gjennomsnitt = []
    fold = tall
    print(len(featuresets2))
    print("kryssvalideringen med :", tall*10, "mest vanlig ord ")
    train_set = featuresets2
    for x in range(fold):
        #det er her kryssvalideringen skjer
        start = int(len(featuresets2)/fold * x)
        end = int(len(featuresets2)/fold*(x + 1))
        print("x={}, start={}, end={}".format(x, start, end))
        t_train_set = train_set[:start]+train_set[end:]
        t_test_set = train_set[start:end]
        classifier2= nltk.NaiveBayesClassifier.train(t_train_set)
        z = nltk.classify.accuracy(classifier2,t_test_set)
        print(z)
        gjennomsnitt.append(z)

    #Her finner jeg gjennomsnittet av Accuracy
    svar = sum(gjennomsnitt)/len(gjennomsnitt)
    print("svar",svar)
    print("--------------------")





def n_fold(featuresets, testSize):
    featuresets2 = featuresets
    gjennomsnitt = []
    ferdig = 1
    slutt = True
    print(len(featuresets2))
    print("kryssvalideringen med :", testSize*10, "mest vanlig ord ")
    while(slutt == True):
        #det er her kryssvalideringen skjer
        train_set3,test_set3 = train_test_split(featuresets2,test_size=testSize)
        classifier2= nltk.NaiveBayesClassifier.train(train_set3)
        z = nltk.classify.accuracy(classifier2,test_set3)
        print(z)
        gjennomsnitt.append(z)
        if ferdig == 10:
            slutt = False
        else:
            ferdig += 1
    #Her finner jeg gjennomsnittet av Accuracy
    svar = sum(gjennomsnitt)/len(gjennomsnitt)
    print("svar",svar)
    print("--------------------")
"""
