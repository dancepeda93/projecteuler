import math

def memoize(func):
	memo = {}
	def memoizewrapper(*args):
		if args not in memo:
			memo[args] = func(*args)
		return memo[args]
	memoizewrapper.__name__ = func.__name__
	return memoizewrapper

def counter(func):
	memo = {"counter":0}
	def counterwrapper(*args):
		if args not in memo:
			memo[args] = 0
		else:
			memo[args] += 1
		memo["counter"] += 1
		if memo["counter"] % 1 == 0:
			print func.__name__, args, memo[args], memo["counter"]
		return func(*args)
	counterwrapper.__name__ = func.__name__
	return counterwrapper

@memoize
def factorial(n):
	if n < 2:
		return 1
	return n * factorial(n-1)

@memoize
def choose(n,k):
	if k > n/2:
		return choose(n,n-k)
	p = 1
	for i in range(k):
		p *= n-i
		p /= i+1
	return p


def buildprimes(limit):

	def flip(n):
		if n in builtprimes:
		    builtprimes.remove(n)
		else:
		    builtprimes.add(n)



	builtprimes = set([2,3,5])

	s1 = set([1, 13, 17, 29, 37, 41, 49, 53])
	s2 = set([7, 19, 31, 43])
	s3 = set([11, 23, 47, 59])




	for x in range(1,int(math.sqrt(limit/4))+1):
	    fourtwo = 4*x**2
	    for y in range(1,int(math.sqrt(limit-fourtwo))+1):
	        n = fourtwo + y**2
	        if n%60 in s1:
	            flip(n)
	            
	for x in range(1,int(math.sqrt(limit/3))+1):
	    threetwoa = 3*x**2
	    for y in range(1,int(math.sqrt(limit-threetwoa))+1):
	        n = threetwoa+y**2
	        if n%60 in s2:
	            flip(n)

	for x in range(1,int(math.sqrt(limit/2))+1):
	    threetwob = 3*x**2
	    for y in range(int(math.ceil(math.sqrt(max(threetwob-limit,0)))),x):
	        n = threetwob - y**2
	        if n%60 in s3:
				flip(n)

	for n in range(5,int(math.sqrt(limit))+1):
	    if n in builtprimes:
	        for k in range(n**2,int(limit+1),n**2):
	            if k in builtprimes:
	                builtprimes.remove(k)

	return sorted(builtprimes)