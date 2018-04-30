# -*- coding:utf-8 -*-

## Jan Tore Loenning, V2017

def test(parser, exfile):
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


            
