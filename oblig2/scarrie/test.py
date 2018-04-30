#encoding: UTF-8
import nltk
from nltk import CFG


def test(parser, exfile):
    """# -*- coding:utf-8 -*-

    ## Jan Tore Loenning, V2017"""

    """Test whether *parser* regognizes items in *exfile*.

    - parser is a NLTK parser
    - exfile is the path to the file containing the examples,
    e.g. 'norsk_testset.txt' or 'english_testset.txt'.
    The format is one sentence per line preceded by + for acceptable
    or - for non-acceptable.
    """
    grammatical = []
    ungrammatical = []
    with open(exfile, 'r') as infile:
        for line in infile:
            if line[0] == '+':
                grammatical.append(line[1:].strip())
            if line[0] == '-':
                ungrammatical.append(line[1:].strip())
    print("\nCorrectly recognized:")
    for s in grammatical:
        if len([t for t in parser.parse(s.split())]) > 0:
            print(s)
    print("\nShould have been recognized, but wasn't:")
    for s in grammatical:
        if not len([t for t in parser.parse(s.split())]) > 0:
            print(s)
    print("\nCorrectly not recognized:")
    for s in ungrammatical:
        if not len([t for t in parser.parse(s.split())]) > 0:
            print(s)
    print("\nShould not have been recognized, but was:")
    for s in ungrammatical:
        if  len([t for t in parser.parse(s.split())]) > 0:
            print(s)

"""
Del 2.
Oppgave 1: basic parser.

"""
data= nltk.data.load("basic.cfg")
basic = nltk.ChartParser(data)

"""
Oppgave 2: PP-ledd
"""
print("_------------------------------_")

data= nltk.data.load("pp.cfg")

pp = nltk.ChartParser(data)
test(pp, "norsk_testset.txt")
print("------------dyret i huset ved vannet sov----------------")
for n in pp.parse("dyret i huset ved vannet sov".split()): print (n)
#Huset ligger ved vannet, eller hunder sover ved et vann (i et hus)
print ("---------------- Kari sov i huset ved vannet ----------------")
for n in pp.parse("Kari fortalte barnet at dyret smilte".split()): print (n)
#-""-
print ("---------------- Kari likte huset ved vannet ----------------")
for n in pp.parse("Kari likte huset ved vannet".split()): print( n)
#Huset blir likt ved vannet, eller at huset som ligger vend vannet blir likt.
print ("---------------- Kari likte dyret i huset ved vannet ----------------")
for n in pp.parse("Kari likte dyret i huset ved vannet".split()): print(n)
#Kari likte dyret som er i huset, eller kari er i huset selv."""
