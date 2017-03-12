'''
Created on Feb 9, 2017

@author: lbraginsky
'''

from __future__ import print_function
from collections import defaultdict
from random import random
from bisect import bisect
from os.path import expanduser

# CORPORA = ["n-grams_data/w3.txt", "n-grams_data/w4.txt", "n-grams_data/w5.txt"]
CORPORA = ["~/n-grams_data/w5.txt"]
TEXT_LEN = 200
TEXT_LEN2 = 300

def weighted_choice(choices):
    values, weights = zip(*choices)
    total = 0
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    x = random() * total
    i = bisect(cum_weights, x)
    return values[i]

class Trie(object):
    def __init__(self):
        self.count = 0
        self.dict = defaultdict(Trie)
    def add(self, gram, count=1):
        node = self
        node.count += count
        for word in gram:
            node = node.dict[word]
            node.count += count
    def random_tail(self, prefix):
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

def read_corpus(corpus_file):
    print("read_corpus {} ... ".format(corpus_file), end='')
    with open(corpus_file) as f:
        data = list(f)
    print("done {:,}".format(len(data)))
    return data

def create_trie(corpora):
    print("create_trie")
    trie = Trie()
    for corpus_file in corpora:
        corpus = read_corpus(expanduser(corpus_file))
        add_corpus_to_trie(trie, corpus)
    print("create_trie done")
    return trie

def add_corpus_to_trie(trie, corpus):
    print("add_corpus_to_trie")
    i = 0
    for line in corpus:
        words = line.split()
        trie.add(words[1:], int(words[0]))
        i += 1
        if i % 10000 == 0: print('.', end='')
        if i % 100000 == 0: print("{:,}".format(i))
    print("\nadd_corpus_to_trie done {:,}".format(i))
    return trie

def detect_cycle(words):
    n = len(words)
    for cyclen in range(2, 10):
        if n < 3 * cyclen: break
        cyc = words[n-cyclen:n]
        if all(words[n-(k+2)*cyclen:n-(k+1)*cyclen] == cyc for k in range(2)):
            return True
    return False

def generate_text(trie, prefix='', break_cycles=True):
    print("generate_text prefix={}, break_cycles={}".format(repr(prefix), break_cycles))
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
        print('{:>30} | {}'.format(' '.join(prefix), ' '.join(tail)))
        if not prefix:
            if count >= TEXT_LEN: break
            text.append([])
        count += out(tail)
        if break_cycles and detect_cycle(raw_text):
            prefix = []
        else:
            prefix = raw_text[-3:]
    print("generate_text done words: {}, paragraphs: {}".format(count, len(text)))
    return '\n'.join(' '.join(words) for words in text)

def main():
    try:
        import sys
        corpora = CORPORA
        if len(sys.argv) > 1: corpora = sys.argv[1:]
        trie = create_trie(corpora)
        def gen_text(*args, **kwargs):
            print()
            text = generate_text(*args, **kwargs)
            print("\nGenerated Text\n")
            print(text)
        for _i in range(5):
            gen_text(trie)
    except IOError as err:
        print("OS error: {}".format(err))

main()

# from testing import timingTest, profile

# profile("create_trie()")

# timingTest(main)
# profile("main()")
