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
start = time.time()
"""
Oblig 4

Oppgave 1:
"""
#obs, koden under tar litt tid

#document_features funksjonen fant jeg på forelesning slidene, mandag 9.apr.
def document_features(word_features, document):
    document_words= set(document)
    features= {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words) #True or False
    return features


def n_fold(featuresetsx, tall):
    gjennomsnitt = []
    fold = 10
    print("kryssvalideringen med :", tall, "mest frekvente ord ")
    train_set = featuresetsx
    for x in range(fold):
        #det er her kryssvalideringen skjer
        start = int(len(featuresetsx)/fold * x)
        end = int(len(featuresetsx)/fold*(x + 1))
        print("Test-nr ={}, start-indeks ={}, end-indeks ={}".format(x, start, end))
        t_train_set = train_set[:start]+train_set[end:]
        t_test_set = train_set[start:end]
        #klassifikatoren finner nå nøyaktigheten til featuresetsa, for vær del av 10-fold kryssvalideringen
        classifier2= nltk.NaiveBayesClassifier.train(t_train_set)
        accuracy = nltk.classify.accuracy(classifier2,t_test_set)
        print(accuracy)
        gjennomsnitt.append(accuracy)

    #Her finner jeg gjennomsnittet av Accuracy
    svar = sum(gjennomsnitt)/len(gjennomsnitt)
    print("svar",svar)
    print("--------------------")


def word_feats(words):
    return dict([(word, True) for word in words])



documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)

all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())

word_featuress = list(all_words)[:2000]

word_features = [w for (w,_) in all_words.most_common(2000)]

#Tester med word_features = [w for (w,_) in all_words.most_common(2000)]
featuresets1 = [(document_features( word_features , d), c) for (d,c) in documents]
train_set1,test_set1 = featuresets1[100:], featuresets1[:100]

#Tester med word_featuress = list(all_words)[:2000]
featuresets2 = [(document_features( word_featuress , d), c) for (d,c) in documents]
train_set2,test_set2 = featuresets2[100:], featuresets2[:100]

print("Test med linjen word_features = [w for (w,_) in all_words.most_common(2000)]")

#Her trener algorithmen på featuresets
classifier= nltk.NaiveBayesClassifier.train(train_set1)

print(nltk.classify.accuracy(classifier,test_set1))

print()

print("Test med linjen word_featuress = list(all_words)[:2000]")

classifier= nltk.NaiveBayesClassifier.train(train_set2)

print(nltk.classify.accuracy(classifier,test_set2))

"""
Resultat for oppgave 1:

Test med linjen word_features = [w for (w,_) in all_words.most_common(2000)] får:
0.74

Test med linjen word_featuress = list(all_words)[:2000] får:
0.69
"""

"""
Resultat for oppgave 2:

Her er resultatet av 10-fold kryssvalideringen av utviklingstet(dev_set):
test1: 0.8055555555555556
test2: 0.8
test3: 0.8
test4: 0.8333333333333334
test5: 0.8277777777777777
test6: 0.8222222222222222
test7: 0.7833333333333333
test8: 0.8
test9: 0.7888888888888889
test10: 0.8611111111111112

gjennomsnitt av alle testene: 0.8122222222222222
"""
s = documents
random.seed(1903)
random.shuffle(s)
test_set = s[1800:]
dev_set =  s[:1800]


featuresets2 = [(document_features(word_features , d), c) for (d,c) in dev_set]

n_fold(featuresets2, 1800)


"""
oppgave 3, forskjellige tester med forskjellige verdier
"""

word_features1 = [w for (w,_) in all_words.most_common(500)]
featuresets3 =  [(document_features(word_features1 , d), c) for (d,c) in dev_set]
n_fold(featuresets3, 500)

word_features2 = [w for (w,_) in all_words.most_common(1000)]
featuresets4 = [(document_features(word_features2 , d), c) for (d,c) in dev_set]
n_fold(featuresets4, 1000)

word_features4 = [w for (w,_) in all_words.most_common(2000)]
featuresets6 = [(document_features(word_features4 , d), c) for (d,c) in dev_set]
n_fold(featuresets6, 2000)

word_features3 = [w for (w,_) in all_words.most_common(5000)]
featuresets5 = [(document_features(word_features3 , d), c) for (d,c) in dev_set]
n_fold(featuresets4, 5000)




"""
Resultat for oppgave 3:

Tabell for testene til 500,1000,2000 og 5000:
(tallene er rundet for plass)

Verdi       test1 | test2 |  test 3 | test4  | test5  | test6  | test7 | test8 | test9 | test10  | gjennomsnitt
500:        0.77  | 0.81  |   0.72  | 0.8    | 0.75   |  0.86  |  0.84 |  0.75 |  0.76 |   0.77  |  0.78
1000:       0.77  | 0.81  |   0.72  | 0.8    | 0.75   |  0.86  |  0.84 |  0.76 |  0.76 |   0.77  |  0.78
2000:       0.81  | 0.82  |   0.75  | 0.82   | 0.78   |  0.87  |  0.84 |  0.82 |  0.79 |   0.83  |  0.82
5000:       0.79  | 0.84  |   0.74  | 0.83   | 0.78   |  0.87  |  0.84 |  0.86 |  0.84 |   0.82  |  0.82

Gjennomsnittet øker jo flere ord jeg bruker. Men jeg vil anta at det vil bli marginale forskjeller jo flere ord du bruker,
det ser du på 2000 ord og 5000 ord.
"""


"""
oppgave 4:
Regner ut accuracy for hvilken mengde ord som fikk best resultat på oppgave 3 og,
regner ut presisjon, gjenfinning ("recall") og F-score for klassen pos og neg.
"""

word_features1 = [w for (w,_) in all_words.most_common(2000)]
featuresets4 =  [(document_features(word_features1 , d), c) for (d,c) in dev_set]
featuresets5 =  [(document_features(word_features1 , d), c) for (d,c) in test_set]


# Her trener jeg heleutviklingsetet og tester det på test_set som jeg la til side i oppgave 2.
classifier2= nltk.NaiveBayesClassifier.train(featuresets4)
z = nltk.classify.accuracy(classifier2,featuresets5)
print("Accuracy for oppgave 4.")
print(z)
print("................")
"""
Accuracy for oppgave 4.
 0.86

"""

"""
Jeg har allerede trent klassifikator, så da finner jeg ut om et dokument har katogorien 'neg' eller 'pos'.
Precision måler nøyaktigheten til en klassifikator, da finner jeg hvor mange falske-positive det finnes.
Mindre falske-positive gir høyere presisjon.

Recall finner fullstendigheten til en klassifikator, høyere recall betyr mindre falske-negative.

F.score finner den vektede harmoniske gjennomsnitt av presisjon og recall. 

"""

classifier = classifier2
refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)

for i, (feats, label) in enumerate(featuresets5):
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

"""
Resultat:

-----------------------------------------------------------
pos precision: 0.9047619047619048
pos recall: 0.7916666666666666
pos F-measure: 0.8444444444444446
-----------------------------------------------------------
neg precision: 0.8275862068965517
neg recall: 0.9230769230769231
neg F-measure: 0.8727272727272728
-----------------------------------------------------------
"""

end = time.time()
import datetime
tid = int(round(end-start))
realtime = str(datetime.timedelta(seconds= tid))
print("Tidsbruk for programmet", realtime)
