##//////////////////////////////////////////////////////
##  Shift-Reduce Parser with Python 3
##  INF2820 V2017
##  Jan Tore Loenning
##//////////////////////////////////////////////////////

"""
A simple Shift-Reduce parser.

This parser finds all possible trees for a list of words.

The parser takes the grammar as an argument.
The grammar is an nltk grammar.

It accepts grammars where the right-hand side
of a rule is a mixture of terminals and non-terminals,
as long as it is non-empty.
The price for this flexibility is less efficiency,
i.e. it shifts many times where a reduction is mandatory.

There are three levels of tracing determined by the optional
argument to the recognizer:
0 - default - no tracing
1 - prints out the value of the stack and rest of words
2 - prints the value of the stack and rest of words and describes action


"""

import nltk
from nltk.tree import Tree


def sr_parse(grammar, words, trace = 0):
    """Parse the words with the grammar using an SR-procedure"""
    if trace > 1:
        print("Initialize:\t\t", end = ' ')
    l = len(' '.join(words))+ 2 #allocate place for printing stack
    return parse(grammar,[], words, trace, l)

def parse(grammar, stack, rwords, trace, l):
    if trace > 0:
        print_current_state(stack, rwords, l)
    if (rwords == [] and
        len(stack) == 1 and
        isinstance(stack[0], nltk.tree.Tree) and
        stack[0].label() == grammar.start().symbol()):
        yield stack[0]
    else:
        for p in grammar.productions():
            rhs = list(p.rhs())
            n = len(rhs)
            for i, symbol in enumerate(rhs):
                if not isinstance(symbol, str):
                    # a non-terminal
                    rhs[i] = symbol.symbol()
            top = stack[-n:]
            for i, node in enumerate(top):
                if not isinstance(node, str):
                    # not a leaf node
                    top[i] = node.label()
            if top == rhs:
                if trace>1: print("Reduce: {}\t".format(p), end=' ')
                newstack = stack[0:-n]
                newstack.append(Tree(p.lhs().symbol(), stack[-n:]))
                for tre in parse(grammar, newstack, rwords, trace, l):
                    yield tre
                if trace > 1:
                    print("Backtrack: {}\t".format(p),end = ' ')
                    print_current_state(stack, rwords, l)
        if not len(rwords) == 0:
            # Shift!
            word = rwords[0]
            if trace > 1:
                print("Shift: {}\t\t".format(word), end=' ')
            newstack = stack[:]
            # A new copy of the stack to be able to build several trees.
            newstack.append(word)
            for tre in parse(grammar, newstack, rwords[1:], trace, l):
                yield tre
            if trace > 1:
                print("Backtrack shift: {}\t".format(word), end=' ')
                print_current_state(stack, rwords,l)


def print_current_state(stack, rwords,l):
    stack_symbols = []
    for element in stack:
        if isinstance(element, str): stack_symbols.append(element)
        else: stack_symbols.append(element.label())
    print("{:>{width}} <> {}".format(' '.join(stack_symbols), ' '.join(rwords),width=l))


def demo(trace=0):
    """A demonstration. Can be run with different levels of tracing"""

    grammar = nltk.CFG.fromstring("""
    S -> NP VP
    VP -> V NP | V NP PP
    PP -> P NP
    V -> 'saw' | 'ate' | 'walked'
    NP -> PN | Det N | Det N PP | 'I'
    PN -> 'John' | 'Mary'
    N -> 'dog' | 'man' | 'telescope' | 'park'
    P -> 'in' | 'by' | 'on' | 'with'
    Det -> 'a' | 'an' | 'the' | 'my'
    """)
    print("Grammar rules:")
    for prod in grammar.productions():
        print(prod)
    sent = "Mary saw a man in the park"
    print("\nParsing with trace = {} of sentence:\n{}".format(trace,sent))
    for t in sr_parse(grammar, sent.split(), trace):
        t.pretty_print()


grammar = nltk.CFG.fromstring("""
S -> NP VP
VP -> VTV NP
VP -> VS CP
CP -> C S
NP -> DET N
NP -> NP PP
VP -> VP PP
PP -> P NP
NP -> 'dyret' | 'treet' | 'Kari'| 'Ola'
N -> 'dyr' | 'tre'
DET -> 'et' | 'ethvert'
VP -> 'sov' | 'smilte'| 'danset'
VTV -> 'kjente' | 'likte' |'dyttet'
VS -> 'trodde'|'så' | 'fortalte'
C -> 'at'
P -> 'fra' | 'til' | 'ved'
""")
sent = "Kari så at Ola dyttet et dyr fra treet".split()

sr_parse(grammar, sent, trace=1)
print_current_state(2,3,4)
