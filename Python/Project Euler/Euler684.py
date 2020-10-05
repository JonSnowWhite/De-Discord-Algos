from datetime import datetime

def fib(i):
    """
    Caluculates fibonacci numbers up to i

    Returns: a list of all fibonacci numbers up to an including the i'th
    """
    f1 = 0
    f2 = 1
    fib = [f1,f2]
    for i in range(2,i+1):
        f3 = f1+f2
        fib.append(f3)
        f1 = f2
        f2 = f3
    return fib


###########################################################
#
# Solves Project Euler Problem 684
# https://projecteuler.net/problem=684
#
###########################################################

# Give your answer modulo 1'000'000'007
mod = 10**9 + 7

def s(x):
    """
    Define s(x) to be the smallest number that has a digit sum of x. 
    For example s(10) = 19

    Basically, fill up the back with as many 9'th as possible: 10^(x//9)-1
    and add the rest of the sum to the front: + 10^(x//9)*(x%9)

    Can be formed into: 10^(x//9)(1+(x%9))-1
    """
    # calculate pre-results faster with mod
    # 10^(x//9) % 10^9+7
    tmp2 = pow(10,x//9,mod)
    return tmp2*(1+(x%9))-1 % mod

def S_single(k):
    """
    Let S(k) = sum_{n=1}^k s(n). You are given S(20 = 1074).

    This is the brute force sum method which is way too slow for larger k.

    Helpful for sanity checks of more sophisticated functions though.

    Runtime: O(k)
    """
    return sum(s(i) for i in range(1,k+1)) % mod

def S_easy(k):
    """
    Faster method to calculate S as defined in S_single.

    Idea: All s(n) look like    1,19,199,...,199...999
                                2,29,299,...,299...999
                                ...
                                9,99,999,...,999...999
    
    So we have these 9 'chains' for each digit 1 to 9. The first chain neatly sums up to
    some form of 22...222-i where i is the numbers of digits in the chain
    
    Adding all chains together yields 222+777+333+666+444+555+999+888+1110-9*3 = 6*999-9*3 = 6*(10^(3)-1)-9*3 
    for i=3 and 6*(10^(i)-1)-9*i for any i

    Should k be a multiple of nine we are good to go. If not we just use S(k)=S(k-1)+s(k) and find the l for which k-l//9=0
    For k-l we use the formula above and simply add up the remaining l many s().

    Runtime: O(1)
    """
    # the number of full chain blocks
    n = k//9
    # l excess numbers
    l = k%9
    # sum up the excess numbers
    sum1 = sum(s(k-i) % mod for i in range(l))
    # 10^n % 10^9+7
    tmp1 = pow(10,n,mod)
    # use the neat formula as described above
    sum2 = 6*(tmp1-1)-(9*n % mod) % mod
    # and return both
    return (sum1 + sum2) % mod

def InverseDigitSum():
    """
    Further let f_i be the Fibonacci sequence defined by f_0=0, f_1=1, and f_i=f_{i-2}+f_{i-1} for all i>=2

    Find sum_{i=2}^90 S(f_i) mod 1000000007.
    """
    my_fib = fib(90)
    return sum(S_easy(my_fib[i]) for i in range(2,91)) % mod

start = datetime.now()
sol = InverseDigitSum()
end = datetime.now()
delta = (end-start).microseconds/1000
print("Solution Euler: {}".format(InverseDigitSum()))
print("Solved in {} milliseconds".format(delta))