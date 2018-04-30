# -*- coding:utf-8 -*-

## Jan Tore Loenning, V2017

def test_sr(recognizer, grammar, exfile):
    """Test whether *recognizer* with *grammar* regognizes items in *exfile*.

    - recognizer is a home-brewn recognizer, e.g. sr_recognizer
    - grammar is a NLTK-grammar
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
        if recognizer(grammar, s): print(s)
    print("\nShould have been recognized, but wasn't:")
    for s in grammatical:
        if not recognizer(grammar, s): print(s)
    print("\nCorrectly not recognized:")
    for s in ungrammatical:
        if not recognizer(grammar, s): print(s)
    print("\nShould not have been recognized, but was:")
    for s in ungrammatical:
        if recognizer(grammar, s): print(s)


            
