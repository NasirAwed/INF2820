import nltk
from nltk.corpus import movie_reviews
#from sklearn.cross_validation import train_test_split
from nltk.classify import NaiveBayesClassifier
import nltk.metrics
from nltk.metrics.scores import precision
from nltk.metrics.scores import recall
from nltk.metrics.scores import f_measure
import random
import warnings
import collections
import time




def word_feats(words):
    return dict([(word, True) for word in words])

negids,  posids = movie_reviews.fileids('neg'), movie_reviews.fileids('pos')
negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

trainfeats = negfeats[:int(len(negfeats)*3/4)] + posfeats[:int(len(posfeats)*3/4)]
testfeats = negfeats[int(len(negfeats)*3/4):] + posfeats[int(len(posfeats)*3/4):]

classifier = NaiveBayesClassifier.train(trainfeats)
refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)

for i, (feats, label) in enumerate(testfeats):
    refsets[label].add(i)
    observed = classifier.classify(feats)
    testsets[observed].add(i)

print("-----------------------------------------------------------")
print( 'pos precision:', precision(refsets['pos'], testsets['pos']))
print ('pos recall:', recall(refsets['pos'], testsets['pos']))
print ('pos F-measure:', f_measure(refsets['pos'], testsets['pos']))
print("-----------------------------------------------------------")
print ('neg precision:',precision(refsets['neg'], testsets['neg']))
print ('neg recall:', recall(refsets['neg'], testsets['neg']))
print ('neg F-measure:', f_measure(refsets['neg'], testsets['neg']))
print("-----------------------------------------------------------")



negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')

negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

negcutoff = len(negfeats)*3/4
poscutoff = len(posfeats)*3/4
x= int(negcutoff)
y= int(poscutoff)

trainfeats = negfeats[:x] + posfeats[:y]
testfeats = negfeats[x:] + posfeats[y:]
print ('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))
classifier = NaiveBayesClassifier.train(trainfeats)
refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)

for i, (feats, label) in enumerate(testfeats):
    refsets[label].add(i)
    observed = classifier.classify(feats)
    testsets[observed].add(i)

print("-----------------------------------------------------------")
print( 'pos precision:', precision(refsets['pos'], testsets['pos']))
print ('pos recall:', recall(refsets['pos'], testsets['pos']))
print ('pos F-measure:', f_measure(refsets['pos'], testsets['pos']))
print("-----------------------------------------------------------")
print ('neg precision:',precision(refsets['neg'], testsets['neg']))
print ('neg recall:', recall(refsets['neg'], testsets['neg']))
print ('neg F-measure:', f_measure(refsets['neg'], testsets['neg']))
print("-----------------------------------------------------------")
