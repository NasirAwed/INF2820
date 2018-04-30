
# -*- coding:utf-8 -*-

## Jan Tore Loenning, V2017
##
## This program constructs a set of fcfg-rules from the Scarrie Lexicon.
## It assumes that the original Scarrie Lexicon is already tranformed to the
## form defined by the program scarrie-lexicon, and that it is contained in
## the same folder as the lexicon. It uses read_lexicon_py3.py to read in
## the Scarrie Lexicon.
## 
## The lexical rules are combined with a set of syntactic rules to a
## fcfg of the NLTK format. The syntactic rules may be written into this file
## or be stored in a separate file.
##
## The easiest way to use the program is to build a grammar and an NLTK
## fcfg-parser by
## >>> grammar1 = build_grammar(<filename>) # or no filename if the rules are
##                                    # in this file
## >>> parser1 = build_parser(grammar1)
##
## The parser command have optional arguments for parsing strategy
## and for tracing.
##
## There are included some additional routines for inspecting
## the lexicon and the generated rules.


import nltk
from read_lexicon_py3 import ScaryLexicon

sclex = ScaryLexicon()
words = sclex.words
  

def build_grammar(fcfg_file=""):
    """Build a fcfg grammar

    fcfg_file is the name of a NLTK fcfg-grammar file with syntactic rules

    return a NLTK fcfg-grammar consisting of the rules
    from fcfg_file extended with lexical rules form the scarry lexicon
    """
    if not fcfg_file: 
         syntactic_rules=rules()
         # use grammar rules from this file if no grammar file is given
    else:
        with open(fcfg_file, 'r') as infile:
            syntactic_rules = infile.read()
    lexical_rules = extract_lexical_rules()
    rule_strings  = syntactic_rules + '\n'.join(lexical_rules)
    grammar = nltk.grammar.FeatureGrammar.fromstring(rule_strings)
    return grammar


def extract_lexical_rules():
    """Extract a set of grammatical rules from the Scary lexicon

    Return a set of strings.
    Each string is a rule
    """
    lex_rules = []
    for word in words.values():
        rules = rules_from_word(word)
        lex_rules.extend(rules)
    # Remove duplicates
    return list(set(lex_rules))


def rules_from_word(word):
    """ Skeleton for extracting rules from lexicon

    shows one example of the use of features:
    how subcategories of verbs can be extracted.
    The format  must match the syntactic rules e.g. 'V_trans*

    The current procedure overgenerates and must be refined.
    """

    w = word.form
    synfeat = word.syn_feat
    rules = []
    feats = synfeat.split('_')
    cat = feats[0]
    if cat == 'V':
        if (feats[2] == 'indic' and
            feats[3] == 'active' and
            feats[4] == 'main'):
            rules = ["""V[SC={}] -> "{}" """.format(sc,w)
                     for sc in feats[-1].split('!') ]
    elif cat != 'no':
        # Not including words with 'no_syn_feat'
        rules = ["""{} -> "{}" """.format(cat, w)]
        # This is way too general
    return rules        


def build_parser(grammar, strategy=nltk.FeatureChartParser, trace=0):
    return strategy(grammar, trace=trace)


######################################################################
#####
#####  A samll example grammar
#####  Shows application of subcategories of verbs extracted from the lexicon
#####
######################################################################

def rules():
    return """
S -> NP VP
NP -> PN | N | Det N
N -> Adj N

VP -> V[SC=intrans]
VP -> V[SC=trans] NP
VP -> V[SC=ditrans] NP NP

PN     -> 'Ola' | 'Kari'

"""




#######################################################################
####
####  Additional useful procedures
####
#######################################################################

## form_to_ids is constructed as a dictionary to be used to go from
## a word identifier and eventually from a word form to the word object
form_to_ids = {}
for i in words.keys():
    form = words[i].form
    if form not in form_to_ids:
        form_to_ids[form] = []
    form_to_ids[form].append(i)

def rules_from_wordid(ident):
    return rules_from_word(words[ident])

def rules_from_wordform(word_form):
    """Find all syntactic rules for the word_form """
    rules = []
    if word_form in form_to_ids:
        for key in form_to_ids[word_form]:
            rules.extend(rules_from_wordid(key))
    # Remove duplicates
    return list(set(rules))

def analyze(word_form):
    """Find all entries for the *word_form* in Scarrie lexicon. Return features"""
    if word_form in form_to_ids.keys():
        wf_ids = form_to_ids[word_form]
        wfs = [words[id] for id in wf_ids]
        return [(wf.morf_feat, wf.syn_feat) for wf in wfs]


