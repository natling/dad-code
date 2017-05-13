'''
Created on May 12, 2017

@author: lbraginsky

the problem is
given an array of integers
and a number m
and a number n

make a new array that is the "densest packing" of the original array, meaning 
that for each element of the original array the new array contains either that 
same number or that number plus a multiple of n, and the difference between 
each pair of adjacent elements in it is greater or equal than the minimum 
difference m

minimize differences between adjacent numbers
'''

def densest_packing(nums, n, m):
    # compute all numbers with minimal differences
    ans = [nums[0]]
    for b in nums[1:]:
        a = ans[-1]
        # high value - minimal value at least m higher than a
        hi = b + (m + a - b + n - 1) // n * n
        # low value - maximal value at least m lower than a
        lo = b + (-m + a - b) // n * n
        # high or low value, whichever is closer to a
        x = min(hi, lo, key=lambda v: abs(v - a))
        ans.append(x)
#         print a, hi, lo, x, ans
    # make all numbers non-negative and minimal
    shift = min(ans) // n * n
    ans = [x - shift for x in ans]
#     print min_x, shift, ans
    return ans

if __name__ == '__main__':
    def test(nums, n, m):
        print
        print nums, "n:", n, "m:", m
        print densest_packing(nums, n, m)
    
    def simple_tests():
        for n in [1, 2, 3]:
            for m in [0, 1, 2]:
                test([10, 20, 30], n, m)
    
    def random_tests():
        from random import randrange    
        for _t in range(10):
            test([randrange(-100, 100) for _ in range(10)], 10, randrange(5, 11))
    
    simple_tests()
    random_tests()
