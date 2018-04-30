from nltk import *
import re

"""
Oppgave 3)
"""

"""
Oppgave a)
"""
pyt_raw = open("Python_INF2820_v2018.txt","r")
pyt_words1 = []
i = 0
x = 0
for line in pyt_raw:
    tweet = pyt_raw.readlines()

    tokenized_sents = [word_tokenize(i) for i in tweet]
    #for i in tokenized_sents:

    #    print(i)


print("----------------------------------------------")


pyt_rawx = open("Python_INF2820_v2018.txt","r")
for w in pyt_rawx:
    print(w.split(" "))



"""
Oppgave b) Forskjellen mellom å bruke splitt og nltk.word_tokenize er at når jeg bruker split,
så lager jeg en liste basert på mellomrom mellom ordene.
Mens nltk bruker komma, bindestrek og mellomrom, og sikkert noe annet.
"""


"""
Oppgave c) og d)
"""
pyt_rawy = open("Python_INF2820_v2018.txt","r")
d = 0
norske_ord = []
p_low = [w.lower().split(" ") for w in pyt_rawy]
print(len(p_low))
for w in p_low:
    if 'å' in w or 'ø' in w or 'æ' in w:
        norske_ord.append(w)

print("-------------------------")

norske_ord2 =[]
i= 0
while i < len(norske_ord):
    for s in norske_ord[i]:
        if 'å' in s or 'ø' in s or 'æ' in s:
            norske_ord2.append(s)
        #
            d = d+1
    i = i+1
"""
oppgave f)
"""
with open("norske.txt", mode="wt", encoding="utf-8") as myfile:
        for lines in norske_ord2:
            myfile.write("".join(str(line) for line in lines))
            myfile.write("\n")

"""
oppgave 4)
b) og c)
"""
def replace(tokens):
    stir = re.findall("\W[a-zA-z0-9]+", tokens)
    stir.replace(stir,"<path>")

    inter = re.findall('\d ', tokens)
    inter.replace(inter, "<num>")



pyt_rawyf = open("Python_INF2820_v2018.txt","r")
for x in pyt_rawyf:
    pyt_wordser = word_tokenize(x)

    replace(pyt_wordser)
