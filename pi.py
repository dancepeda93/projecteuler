import math
from eulertools import *

@memoize
def P2(x,a):
    x05 = int(math.sqrt(x))
    n = 0
    for i in range(a,pi(x05)):
        n += pi(x/primes[i]) - i
    return n

@memoize
def P3(x,a):
    n = 0
    top = pi(x/(primes[a]**2))
    for i in range(a,top):
        n += P2(x/primes[i],i)
    return n

@memoize
def pi(x):
    if x <= primes[-1]:
        return linearpi(x)

    x025 = int(math.sqrt(math.sqrt(x)))
    pi025 = linearpi(x025)
    return pi025 + phi(x,pi025) - 1 - P2(x,pi025) - P3(x,pi025)

@memoize
def linearpi(x):
    bottom = 0
    top = len(primes)
    while bottom != top:
        middle = (bottom+top)/2
        if primes[middle] > x:
            top = middle
        else:
            bottom = middle + 1
    return top

@memoize
def phi(m,n):
    if n == 0:
        return int(m)
    if n == 1:
        return (int(m) + 1)/2
    if m == 0:
        return 0
    if m < 4:
        return 1
    return phi(m,n-1) - phi(m/primes[n-1],n-1)

def setprimes(p):
    global primes
    primes = p