def I(n):
	nsmall = n % N
	for i in range((n-2)/N,-1,-1):
		big = i*N
		for j in d[nsmall]:
			test = big + j
			if test < n-1:
				if test**2 % n == 1:
					return test
	return 1


exp = 7

depth = 4
N = 10**depth
d = {i:tuple() for i in range(N)}
for i in range(N):
	if i == 0:
		for j in range(N,-1,-1):
			if j**2 % N == 1:
				d[0] += (j,)
		continue
	if i == 1: continue
	for j in range(N,-1,-1):
		if (j**2 % N) % i == 1:
			d[i] += (j,)

print "starting..."

s = 0
for i in range(3,2*10**exp+1):
	if i % N == 0:
		print i
	s += I(i)
print
print s