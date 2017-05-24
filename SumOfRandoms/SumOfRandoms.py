'''
Created on May 24, 2017

@author: lbraginsky
'''

def sum_of_randoms(next_number, target_sum):
    """
    Given a function next_number that returns some number and a target sum
    return the list of numbers.
    """
    s = 0
    nums = []
    while s != target_sum:
        x = next_number()
        if s + x > target_sum:
            x = target_sum - s
        s += x
        nums.append(x)
    return nums

def random_words(n_words, length, min_word=1):
    """
    Given number of words and the length of the string returns a list of word
    lengths such that each word length is at least min_word (by default 1).
    """
    from random import sample
    m = length - min_word * n_words - n_words + 1
    assert m >= n_words - 1
    delim = [0] + sorted(sample(range(m), n_words - 1)) + [m]
    return [b - a + min_word for a, b in zip(delim, delim[1:])]
    
if __name__ == '__main__':
    from random import randrange

    def test_sum_of_randoms(max_num, target_sum):
        next_number = lambda: 1 + randrange(max_num)
        print
        print "sum_of_randoms", max_num, target_sum
        for _ in range(5):
            print sum_of_randoms(next_number, target_sum)

    test_sum_of_randoms(5, 10)
    test_sum_of_randoms(10, 50)
    test_sum_of_randoms(20, 100)

    def test_random_words(n_words, length, min_word):
        print
        print "random_words", n_words, length, min_word
        for _ in range(5):
            words = random_words(n_words, length, min_word)
            s = ' '.join('x' * w for w in words)
            print words, repr(s)

    test_random_words(3, 15, 1)
    test_random_words(5, 20, 1)
