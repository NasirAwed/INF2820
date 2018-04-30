import nltk


data= nltk.data.load("cnf.cfg")
basic = nltk.ChartParser(data)


print("------------tree for cnf.cfg grammatikk----------------")
print()
for n in basic.parse("Ola fortalte at Kari ga barnet dyret i huset".split()): n.pretty_print()


data2= nltk.data.load("my.cfg")
my = nltk.ChartParser(data2)


print("------------tree for my.cfg grammatikk----------------")
print()
for n in my.parse("Ola fortalte at Kari ga barnet dyret i huset".split()): n.pretty_print()

"""
Forskjellen mellom hva cnf.cfg og hva my.cfg genererer på denne spesifikke settningen er,
 X2 -> DTV NP og NP -> "terminale" isteden for at NP -> PN | ND , PN -> "terminale", ND -> "terminale".

 Det jeg mener er at på my.cfg ville du fått:

        |
        VP
________|______
|        NP     NP
|        |      |
DTV       ND     ND
|        |      |
ga     barnet dyret

og i cnf.cfg blir:

        |
        VP
         |______
 - - - - X2     NP
|        |      |
DTV      NP
|        |      |
ga     barnet dyret
"""

myparser = nltk.load_parser("file:norsk.fcfg" )


#for t in myparser.parse("Kari sov  ".split()): t.draw()

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

test(myparser,"fcfg_testset.txt")
