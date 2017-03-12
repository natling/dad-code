
# coding: utf-8

# In[199]:

'''
Created on Feb 9, 2017

@author: lbraginsky
'''
from __future__ import print_function

CORPORA = ["~/n-grams_data/w5.txt"]
# CORPORA = ["~/n-grams_data/w3.txt", "~/n-grams_data/w4.txt", "~/n-grams_data/w5.txt"]
# CORPORA = ["~/Dropbox/Public/Miscellaneous/Code/Python/5-grams non case sensitive.txt"]
TEXT_LEN = 200
TEXT_LEN2 = 300
SHOW_GENERATION = False


# In[180]:

from random import random
from bisect import bisect

def weighted_choice(choices):
    """Random choice from weighted values"""
    values, weights = zip(*choices)
    total = 0
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    x = random() * total
    i = bisect(cum_weights, x)
    return values[i]


# In[181]:

from collections import defaultdict, Counter

class Trie(object):
    """Trie structure to hold the grams"""
    def __init__(self):
        self.count = 0
        self.dict = defaultdict(Trie)
    def add(self, gram, count=1):
        """Add the gram to the trie"""
        node = self
        node.count += count
        for word in gram:
            node = node.dict[word]
            node.count += count
    def random_tail(self, prefix):
        """Find the prefix in the trie and generate a random continuation.
        If the prefix is not in the trie return None.
        At each node select a random branch with probability proportional to the branch frequency."""
        node = self
        for word in prefix:
            node = node.dict.get(word)
            if not node: return None
        tail = []
        while node.dict:
            choices = [(word, sub.count) for word, sub in node.dict.iteritems()]
            word = weighted_choice(choices)
            tail.append(word)
            node = node.dict[word]
        return tail
    def count_nodes(self):
        return 1 + sum(node.count_nodes() for node in self.dict.values())
    def count_grams(self):
        return sum(node.count_grams() for node in self.dict.values()) if self.dict else 1
    def branching(self):
        def br(node):
            if node.dict:
                for sub in node.dict.values():
                    for factor in br(sub): yield factor
                yield len(node.dict)
        bc = Counter(br(self))
        return sorted(bc.iteritems())


# In[182]:

from os.path import expanduser

def load_corpora(corpora):
    try:
        print("Corpora: {}".format(corpora))
        trie = Trie()
        for corpus_file in corpora:
            corpus_file = expanduser(corpus_file)
            with open(corpus_file) as f:
                data = list(f)
            print("{} {:,} lines".format(corpus_file, len(data)))
            add_corpus_to_trie(trie, data)
        return trie
    except IOError as err:
        print("OS error: {}".format(err))

def add_corpus_to_trie(trie, corpus):
    print("adding to trie")
    i = 0
    for line in corpus:
        words = line.split()
        trie.add(words[1:], int(words[0]))
        i += 1
        if i % 10000 == 0: print(i/100000 if i%100000==0 else '.', end='')
    print("done {:,}".format(i))
    return trie


# In[197]:

def generate_text(trie, prefix='', break_cycles=True):
    print("prefix={}\nbreak_cycles={}".format(repr(prefix), break_cycles))
    prefix = prefix.split()
    raw_text, text = [], []
    def out(tail):
        if not tail: return 0
        raw_text.extend(tail)
        if not text: text.append([])
        words = text[-1]
        count = 0
        for w in tail:
            if w == "n't" and words:
                words[-1] += w
            else:
                words.append(w)
                count += 1
        return count
    count = out(prefix)
    while count < TEXT_LEN2:
        while True:
            tail = trie.random_tail(prefix)
            if tail: break
            prefix = prefix[1:]
        if SHOW_GENERATION:
            print('{:>30} | {}'.format(' '.join(prefix), ' '.join(tail)))
        if not prefix:
            if count >= TEXT_LEN: break
            text.append([])
        count += out(tail)
        if break_cycles and detect_cycle(raw_text):
            prefix = []
        else:
            prefix = raw_text[-3:]
    print("words: {}\nparagraphs: {}".format(count, len(text)))
    return text

def detect_cycle(words):
    n = len(words)
    for cyclen in range(2, 10):
        if n < 3 * cyclen: break
        cyc = words[n-cyclen:n]
        if all(words[n-(k+2)*cyclen:n-(k+1)*cyclen] == cyc for k in range(2)):
            return True
    return False


# In[184]:

trie = load_corpora(CORPORA)


# In[200]:

prefix = "once upon a"
text = generate_text(trie, prefix)
print("\nGenerated Text\n")
print('\n\n'.join(' '.join(words) for words in text))


# In[201]:

print("Trie stats")
print("Grams: {:,}".format(trie.count_grams()))
print("Nodes: {:,}".format(trie.count_nodes()))


# In[202]:

import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')

def branching_plot(data):
    x, y = zip(*data)
    plt.loglog(x, y)
    plt.title('Trie Branching')
    plt.xlabel('Branching')
    plt.ylabel('Count')
    plt.grid(True)

branching = trie.branching()
filtered = [(factor, count) for factor, count in branching if factor >= 20 and factor <= 1000]

plt.figure(figsize=(16, 5))
plt.subplot(121)
branching_plot(branching)
plt.subplot(122)
branching_plot(filtered)

