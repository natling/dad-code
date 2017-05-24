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


if __name__ == '__main__':
    from random import randrange

    def test(max_num, target_sum):
        next_number = lambda: 1 + randrange(max_num)
        print
        print max_num, target_sum
        for _ in range(5):
            print sum_of_randoms(next_number, target_sum)

    test(5, 10)
    test(10, 50)
    test(20, 100)
