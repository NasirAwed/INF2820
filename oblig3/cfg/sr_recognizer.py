##//////////////////////////////////////////////////////
##  Shift-Reduce Recognizer with Python 3
##  INF2820 V2017
##  Jan Tore Loenning
##//////////////////////////////////////////////////////

"""
A simple Shift-Reduce recognizer.

This recognizer checks all possible analyses until it succeeds,
i.e. it backtracks when failure.
If and when it succeeds, it interrupts and returns with True.

The recognizer takes the grammar as an argument.
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

A grammar is loaded like
g1 = nltk.data.load('file:../grammar1.cfg'), or simpler
g1 = load('../gramar1.cfg') which facilitates auto-completion when available.


"""

from __future__ import division
import nltk

        
def load(filename):
    address='file:'+filename
    return nltk.data.load(address)


def sr_recognize(grammar, words, trace = 0):
    """Recognize the words according to the grammar using an SR-procedure"""
    if trace > 1:
        print("Initialize:\t\t", end='')
    return recognize(grammar,[], words, trace)

 
## The structure of the recognize-procedure without comments and tracing:
## To see that it is correct, uncomment it and comment out the
## long version of recognize. 
##
##def recognize(grammar, stack, rwords, trace):
##    if rwords == [] and len(stack) == 1 and stack[0] == grammar.start():
##        return True
##    else:
##        for p in grammar.productions():
##            rhs = list(p.rhs())
##            n = len(rhs)
##            if stack[-n:] == rhs:
##                newstack = stack[0:-n]
##                newstack.append(p.lhs())
##                if recognize(grammar, newstack, rwords, trace):
##                    return True
##        if not len(rwords) == 0:
##            newstack = stack[:]
##            newstack.append(rwords[0])
##            if recognize(grammar, newstack, rwords[1:], trace):
##                return True
##    return False

def recognize(grammar, stack, rwords, trace):
    """SR-recognize rwords according to grammar and current stack.

    grammar - a CF-PSG of the nltk-format
    stack - a list of symbols where each symbol is either
        a terminal of type str, or
        a non-terminal of type nltk-nonterminal
    rwords - a list of remaining words, each of type str
    trace - 0, 1 or 2. Default is 0.

    Try to recognize the rwords by two operations
        - shifting words from rwords to stack
        - reducing the stack
     Return True on first success.
     """
    if trace > 0:
        print_current_state(stack, rwords) 
    if rwords == [] and len(stack) == 1 and stack[0] == grammar.start():
        # Success!
        return True 
    else:
        for p in grammar.productions():
            # Try all possible reductions in turn.
            rhs = list(p.rhs())
            n = len(rhs)
            if stack[-n:] == rhs:
                # Reduce!
                if trace > 1:
                    print("Reduce: {}\t".format(p), end='')  
                newstack = stack[0:-n]
                # Make a copy to avoid conflicts.
                newstack.append(p.lhs())
                if recognize(grammar, newstack, rwords, trace):
                    return True
                if trace > 1:
                    print("Backtrack: {}\t".format(p), end='') 
                    print_current_state(stack, rwords)  
        if not len(rwords) == 0:
            # Shift!
            newstack = stack[:]
            newstack.append(rwords[0])
            # Make a copy to avoid conflicts.
            if trace > 1:
                    print("Shift: {}\t\t".format(rwords[0]), end = '')
            if recognize(grammar, newstack, rwords[1:], trace):
                return True
            if trace > 1:
                print("Backtrack shift: {}\t".format(rwords[0]), end='') 
                print_current_state(stack, rwords) 
    return False


def print_current_state(stack, rwords):
    for symbol in stack:
        print(symbol, end=' ')
    if len(stack) == 0: print("#", end ='')
    print(" <> ", end = ' ')
    for word in rwords:
        print(word, end = ' ')
    if len(rwords) == 0: print("#", end = '')
    print('')


def demo():
    """A demonstration."""

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
    print("\nRecognition with trace = 1, of the sentence:")
    print(sent, end="\n\n")
    print(sr_recognize(grammar, sent.split(),1))
    print("\n\nRecognition with trace = 2, of the sentence:")
    print(sent, end="\n\n")
    print(sr_recognize(grammar, sent.split(),2))
