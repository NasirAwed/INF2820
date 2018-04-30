##//////////////////////////////////////////////////////
##  CKY Recognizer
##  INF2820 V2017
##  Jan Tore Loenning
##//////////////////////////////////////////////////////"""

"""
A simple CKY recognizer.

Given a list of tokens (words), it constructs the cky table
and prints the cky table.

The grammar is an nltk grammar.
It has to be on Chomsky normal form (CNF), i.e. the right-hand side
of a rule must consist of either
- one single terminal, or
- two non-terminals

There are two varaints of the recognizer:
cky() which constructs and returns the table, and
cky_table() which constructs and prints the table.

A grammar is loaded like
g1 = nltk.data.load('file:../grammar1.cfg'), or simpler
g1 = load('../gramar1.cfg') which facilitates auto-completation when available.

"""

import nltk


def load(path_to_grammar):
    address = "file:"+path_to_grammar
    return nltk.data.load(address)


def cky_table(words, grammar):
    """Recognize *words* according to *grammar*. Print CKY-table"""
    tabl = cky(words, grammar)
    display(tabl, words)


def cky_recognize(words, grammar):
    """Recognize *words* according to *grammar*. Return truth value"""
    tabl = cky(words, grammar)
    top = grammar.start()
    return top in tabl[0][len(words)]


def cky(words, grammar):
    """Recognize *words* according to *grammar*. Return CKY-table"""
    tabl = [[[] for j in range(len(words)+1) ]
                for i in range(len(words))]
    # Make a table, tabl[i][j],
    # where 0<=i<=range(len(words)) and 0<=j<=range(len(words))+1
    # Each cell is an empty list
    for j in range(len(words)):
        # Process sentence from left to right.
        # Fill all cells ending  in (j+1)
        tabl[j][j+1] = [p.lhs() for p in grammar.productions()
                        if  p.rhs() == (words[j],)]
        # Fill in the lexical categories.
        for i in range(j-1,-1,-1):
            # Fill the box tabl[i][j+1]
            # Start with i = j-1
            # Stop when i > -1 (i.e. i >= 0)
            # Step 1
            for k in  range (i+1, j+1, 1):
                # Put together tabl[i][k] and tabl[k][j+1]
                # Start with k = i+1
                # Stop when k < j+1 (i.e. k<= j)
                # Step 1
                for p in grammar.productions():
                    # Loop through the grammar rules
                    if (p.rhs()[0] in tabl[i][k] and
                        p.rhs()[1] in tabl[k][j+1]):
                        if not p.lhs() in tabl[i][j+1]:
                            # Only add p.lhs() if it is not already there.
                            tabl[i][j+1].append(p.lhs())
    return tabl


## The structure of the cky procedure without comments and tracing:
## To see that it is correct, uncomment it and comment out the
## long version.
##
##def cky(words, grammar):
##    tabl = [[[] for j in range(len(words)+1) ] for i in range(len(words))]
##    for j in range(len(words)):
##        tabl[j][j+1] = [p.lhs() for p in grammar.productions()
##                        if  p.rhs() == (words[j],)]
##        for i in range(j-1,-1,-1):
##            for k in  range (i+1, j+1, 1):
##                for p in grammar.productions():
##                    if (p.rhs()[0] in tabl[i][k] and
##                        p.rhs()[1] in tabl[k][j+1]):
##                        if not p.lhs() in tabl[i][j+1]:
##                            tabl[i][j+1].append(p.lhs())
##    return tabl



########################################################
#   Output
#   The rest is related to producing readable outputs.
#   It is not part of the cky-parsing algorithm
#   Not inf2820 curriculum
########################################################


def display(tabl, words):
    """
    Display the *words* and the *table* which is constructed from the words.
    """
    n = len(words)
    space = [0 for i in range(n)]
    for j in range(n):
        space[j] = max([len(item.symbol()) for i in range(j+1)
                                           for item in tabl[i][j+1]]+
                       [len(words[j])+2])
    # Allocate *space[j]* for the width of column j
    print(" ".ljust(2), end='')
    # Before first word.
    for i in range(n):
        # Print the words[i] using *space[i]* many characters for i = 0,..,n-1
        node = '('+str(i)+')'
        print(node.ljust(3), end='')
        #transform "(2)" to "(2) " taking the same space as "(10)" by ljust
        print(words[i].ljust(space[i]-3), end='')
    print('('+str(n)+')')
    totalspace = 0
    for i in range(n):
        totalspace += space[i]
    print((totalspace+5+3*n)*'-')
    # A horizontal line
    for start in range(n):
        # One row of cells. All cells starting in *start*.
        print(str(start).rjust(2)+') |',end='')
        # Number the cell row and print wall
        height = max([len(tabl[start][j]) for j in range(n+1)])+1
        # The number of lines allocated for this row +1 blank line
        for count in range(height):
            # One line in the row
            if not count == 0:
                print("    |",end='')
                # Print wall before first cell
            for end in range(1,n+1):
                if count < len(tabl[start][end]):
                    # There is more to print
                    item = list(tabl[start][end])[count].symbol()
                    print(item.ljust(space[end-1]),'|',end='')
                else:
                    # Leave this line empty in this cell
                    print(" ".ljust(space[end-1]),'|',end='')
            print(' ')
        print((totalspace+5+3*n)*'-')


f= load("cnf.cfg")
b = ["Ola", "fortalte", "at", "Kari", "ga", "barnet", "dyret", "i", "huset"]
cky_table(b, f)
