# -*- coding:utf-8 -*-

## Jan Tore Loenning, V2017
##
## This is a program for reading the prepare scary Lexicon into Python 3.
## It assumes that the original ScaryLexicon is already tranformed to the
## form defined by the program scarrie-lexicon, and that it is contained in
## the same folder as the lexicon. The command ScaryLexicon() returns
## the lexicon.
##
"""
Oppgave Løsning ligger lenger under.
"""
import json
from collections import defaultdict

class Word:
    """Simple class collecting the different features of a word (form)"""

    def __init__(self,ident,form,morf_feat,syn_feat='no_syn_feat'):
        self.ident = ident
        self.form = form
        self.morf_feat = morf_feat
        self.syn_feat = syn_feat


class Lexeme:
    """Class collecting the word identifiers belonging to the same lexeme"""

    def __init__(self,ident,word_ids):
        self.ident = ident
        self.word_ids = word_ids


class ScaryLexicon(dict):
    """Read in the Scarrie Lexicon in enclosed format.

    First construct a sublexicon corresponif # NOTE:ding to each file
    Then make a dicionary *words* containing all words from sublexica
    except affixes and suffixes, and similarly for lexemes.
    """

    def __init__(self):
        for (lexicon, i) in zip(['main',
                        'gramwords',
                        'gramwords2x',
                        'idiomwords',
                        'abbrevwords',
                        'prefixes',
                        'suffixes'],
                        ['', 'gr', 'g2', 'idi', 'ab', 'pre', 'suf']):
            self[lexicon]= SubLexicon(lexicon, i)
        self.words =  {k: v for lex in ['main',
                        'gramwords',
                        'gramwords2x',
                        'idiomwords',
                        'abbrevwords']
                        for (k,v) in self[lex].words.items()}
        self.lexemes =  {k: v for lex in ['main',
                        'gramwords',
                        'gramwords2x',
                        'idiomwords',
                        'abbrevwords']
                        for (k,v) in self[lex].lexemes.items()}


class SubLexicon:
    """Read in a sublexicon file in the provided format.

    Store in 2 dictionaries:
    *words*: a dictionary which maps word identifiers to words
    *lexemes*: a dictionary mapping lexeme ids to lexemes.
    """

    def __init__(self, lexicon, sort):
        words = {}
        lexemes = {}
        lex_nr = -1
        wf_nr = -1
        with open(lexicon, 'r') as infile:
            for line in infile:
                posts = line.strip().split(';')
                if posts[0] == 'Lexeme':
                    # Start a new lexeme
                    lex_nr += 1
                    ident = sort+'x'+str(lex_nr)
                    forms = []   # Identifiers of word forms in this lexeme.
                    # To be filled.
                    this_lexeme = Lexeme(ident, forms)
                    lexemes[ident]=this_lexeme
                else:
                    # Start a new word
                    wf_nr += 1
                    ident = sort+'w'+str(wf_nr)
                    form = posts[0]
                    if len(posts) == 2:
                        posts.append('no_syn_feat')
                        # Some words lack syntactic feature.
                    this_word = Word(ident, form, posts[1], posts[2])
                    # Make new word form. Include current position in word.
                    words[ident]=this_word
                    forms.append(ident)
                    # Put word identifier into the list of its lexeme.
        self.words, self.lexemes = words, lexemes

"""
Oblig 2. Del 1:
Nasir Awed
"""

"""
(e)
"""
def lemmatizer(word):
    inv_map = {}
    i= 0
    for k, v in lex.items():
        inv_map[v] = inv_map.get(v, [])
        ider = v.word_ids
        while len(ider) > 0:
            inv_map[ider[i]].append(k)
            i += 1
        i = 0
    print(inv_map[word])


"""
(d)
"""
def lemma(word):
    """
    Her finner jeg ordets common form, sender med ordet som string.
    Finner alle variasjoner av ordet. Og bruker morf_feat til å sjekke om
    """
    if len(lex[word].word_ids)==1: return lex[word].word_ids[0]
    for x in lex[word].word_ids:
        morf= words[x].morf_feat.split(',')
        if 'V' in morf and 'inf' in morf: return words[x]
        elif 'N' in morf and 'indef' in morf: return words[x]
        elif 'A' in morf and 'pos' in morf: return words[x]


"""
(c)
"""

def pretty_print(ordet):
    for x in form_to_ids[ordet]:
        line = words[x].syn_feat
        liste = line.split("_")
        print("ordet" +":"+ ordet)
        print("cat" +":"+liste[0])
        print("gen" +":"+ liste[1])
        print("num" +":"+ liste[2])
        if(len(liste) > 3):
            #print("lemma"+":"+ lemmatizer(ordet).form)
            print("def" +":"+ liste[3])
        print()

"""
(a)
"""
def analyse(ordet):
    i = 0
    ident = form_to_ids[ordet]
    while i < len(ident):
        w = words[ident[i]]
        print(w.syn_feat)
        print(w.morf_feat)
        i += 1


sclex = ScaryLexicon()
words=sclex.words
form_to_ids= defaultdict(list)


for key in words:
    form_to_ids[words[key].form].append(key)



lex = sclex.lexemes
flipped_lex = defaultdict(list)
for key in words:
    flipped_lex[words[key].form].append(key)


print("------Analyse av 'kaster' og 'øyer----------------' ")
analyse("kaster")
analyse("øyer")
print()
print("-------------pen utskrift--------------------")
pretty_print("kaster")
pretty_print("kastet")
pretty_print("noen")
pretty_print("et")
print()
print("------ Lemma ---------------------")
print(lemma('x30027').form)
print(lemma('x30049').form)
print(lemma('x30061').form)
print(lemma('x29482').form)


"""
(b)

forklaring utskriften til analyse av 'kaster':
-----------------------------------
Her er kaster et Substantiv, Hannkjønn, flertall og ubestemt form

ordet:kaster
cat:N
gen:m
num:pl
def:indef
-----------------------------------
Her er 'kaster' et verb, presens, indikativ, aktivstemme,

ordet:kaster
cat:V
gen:pres
num:indic
def:active
-----------------------------------
Her er ordet et Substantiv, hannkjønn, entall, ubestemt form.

ordet:kaster
cat:N
gen:m
num:sg
def:indef
-------------------------------

"""
