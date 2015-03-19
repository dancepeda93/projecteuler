from eulertools import *
from pi import *

def f(n,exp):
	top = int(n**(1./exp))
	return pi(top)
	

def aaab(n):
	threeone = 0
	for i in range(pi((n/2)**(1.00001/3))):
		first = primes[i]**3
		threeone += pi(n/first)
	threeone -= f(n,4)
	return threeone

def abc(n):
	oneoneone = 0
	maxp1 = math.sqrt(n/2)
	for i in range(1,pi(maxp1)):
		p1 = primes[i]
		maxj = min(i, pi(n/(p1**2)))
		for j in range(maxj):
			ij = p1 * primes[j]
			oneoneone += pi(n/ij)
			oneoneone -= pi(p1)
	return oneoneone

def f8(n):
	seven = f(n,7)
	threeone = aaab(n)
	oneoneone = abc(n)
	return seven + threeone + oneoneone

def main(exp):
	global primes
	n = 10**exp
	topprime = n**(7./10)
	primes = buildprimes(topprime)
	setprimes(primes)
	print "calculating using %s primes..." % len(primes)
	rval = f8(n)
	print rval
	return rval

exp = 12

# import cProfile
if "cProfile" in globals():
	cProfile.run("main(%s)" % exp)
else:
	main(exp)