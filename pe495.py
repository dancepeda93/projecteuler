primes = [2,3]

def findfactors(n):
	build_primes(n)
	if n in primes:
		return {n:1}
	factors = {}
	for i in primes:
		while n % i == 0:
			if i not in factors:
				factors[i] = 0
			factors[i] += 1
			n /= i
		if n == 1:
			break
	return factors


def factorialdictionarygenerator(n):
	build_primes(n)
	d = {}
	for i in primes:
		if i > n:
			break
		present = n/i
		d[i] = 0
		while present:
			d[i] += present
			present /= i
	return d

def Wfactorial(n,k,mod=None):
	return Wd(factorialdictionarygenerator(n),k,mod)

def W(n,k,mod=None):
	return Wd(findfactors(n),k,mod)

@memoize
def reversemerge(state):
	if len(state) > 2:
		l1 = reversemerge(state[:len(state)/2])
		l2 = reversemerge(state[len(state)/2:])
		return reversemerge((l1,l2))
	x = tuple()
	for i in state:
		x += i
	return tuple(sorted(x,reverse=True))


def overlaphelper(value,freq,food):
	if freq == 1:
		last = None
		for i in range(len(food)):
			if food[i] != last:
				last = food[i]
				yield (value + last,), 0, food[i+1:], food[:i]
		yield (value + 1,), 0, tuple(), food

	else:
		for i in overlaphelper(value,freq-1,food):
			last = None
			for j in range(len(i[2])):
				if i[2][j] != last:
					last = i[-2][j]
					yield i[0] + (value + last,), i[1], i[2][j+1:], i[2][:j]+i[3]
			if i[1] == 0:
				yield i[0] + (value + 1,), i[1], tuple(), i[2] + i[3]
			yield i[0], i[1]+1, tuple(), i[2] + i[3]

@memoize
def getoverlapstates(state):
	value = state[0]
	freq = state.count(value)
	food = state[freq:]
	overlapstates = []
	for i in overlaphelper(value,freq,food):
		overlapstates.append(i[0] + (value,) * i[1] + i[3] + i[2])
	return overlapstates

@memoize
def minimum(k,state,s):
	m = sum([i*state[i] for i in range(len(state))])
	k -= s
	return m + (2*len(state) + k - 1)*k / 2

def allsame(state):
	for i in state[1:]:
		if i != state[0]:
			return False
	return True

@memoize
def gcf(state):
	if state == tuple():
		return False
	if allsame(state):
		return state[0]
	factors = set(findfactors(state[0]))
	for i in state[1:]:
		factors = factors.intersection(findfactors(i))
		if factors == set([]):
			return False
	return max(factors)


@memoize
def count(distribute,k,state=tuple()):
	if state and state[0] == k:
		return int(distribute % state[0] == 0)
	if k == 1:
		return 1
	if k == 2:
		return (distribute+1)/2

	s = sum(state)
	if s == k:
		g = gcf(state)
		if g:
			if distribute % g == 0:
				newstate = tuple([i/g for i in state if i > g])
				return count(distribute/g,k/g,newstate)
			else:
				return 0
	if s > k or distribute < minimum(k,state,s):
		return 0


	total = 0
	if state == tuple():
		for i in range(distribute/k):
			remove = k*(i+1) - 1
			total += count(distribute-remove,k-1)
	else:
		c = state.count(state[0])
		start = state[0]*minimum(c,tuple(),0)
		stop = distribute - minimum(k-state[0]*c,state[c:],s-c*state[0]) + 1
		for i in range(start,stop,state[0]):
			next = count(distribute-i,k-state[0]*c,state[c:])
			if next != 0:
				first = count(i/state[0],c)
				assert first*next != 0, "%s %s %s" % (distribute, k, state) # deleteme
				total += first*next
		for j in getoverlapstates(state):
			total -= count(distribute,k,j)
	return total


@memoize
def partition(k):
	if k == 1:
		return [(2,), tuple()]

	states = []
	for p in partition(k-1):
		s = sum(p)
		if p and s == k-2:
			newstate = p+(2,)
			states.append(newstate)
		elif s == k-1 and (len(p) < 2 or p[-2] > p[-1]):
			newstate = p[:-1] + (p[-1]+1,)
			states.append(newstate)
		states.append(p)
	return states


@memoize
def getnextstates(state,distribute,k,mod):
	if state == tuple():
		return {tuple(): choose(distribute + k - 1, k - 1)}

	if distribute == 0:
		return {state:1}


	nextstates = {}
	if state[0] == k:
		for state in partition(k):
			c = count(distribute,k,state)
			if c:
				nextstates[state] = c
		return nextstates

	for i in range(distribute+1):

		first = getnextstates(state[:1],i,state[0],mod)
		next = getnextstates(state[1:],distribute-i,k-state[0],mod)	

		for x in first:
			for y in next:
				newstate = reversemerge((x,y))
				if newstate not in nextstates:
					nextstates[newstate] = 0
				nextstates[newstate] += first[x] * next[y]
				if mod:
					nextstates[newstate] = nextstates[newstate] % mod

	return nextstates

def update(possible,distribute,k,mod):
	new = {}
	for state in possible:
		nextstates = getnextstates(state,distribute,k,mod)
		for nextstate in nextstates:
			if nextstate not in new:
				new[nextstate] = 0
			new[nextstate] += nextstates[nextstate] * possible[state]
			if mod:
				new[nextstate] = new[nextstate] % mod
	return new

def Wd(d,k,mod=None):
	possible = {(k,):1}
	values = sorted(d.values(), reverse=True)

	for distribute in values:
		# print "possible = %s" % possible
		# print "distribute = %s" % distribute
		# print;print;print
		possible = update(possible,distribute,k,mod)

	if tuple() not in possible:
		return 0
	return possible[tuple()]


def main():
	mod = 1000000007
	known = {}
	known[(10,4)] = 18157
	known[(30,8)] = 751250442
	known[(100,10)] = 287549200
	known[(200,12)] = 330592491
	known[(300,13)] = 320072954
	known[(500,15)] = 635188108
	known[(600,20)] = 985314156


	n = 500
	k = 15

	w = Wfactorial(n,k,mod)
	if (n,k) in known:
		assert w == known[(n,k)], w
	else:
		print "known[(%s,%s)] = %s" % (n,k,w)



import cProfile
if "cProfile" in globals():
	cProfile.run("main()")
else:
	main()