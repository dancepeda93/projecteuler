from eulertools import *

primes = buildprimes(10)


def mex(a,b):
	for i in primes:
		if i > a or i > b:
			break
		if a % i == 0:
			if b % i == 0:
				return False
			while a % i == 0:
				a /= i
		while b % i == 0:
			b /= i
	return True

def getn(m,n,slope):
	longest = min(m/slope[0], n/slope[1])
	rows = m - longest*slope[0] + 1
	columns = n - longest*slope[1] + 1
	lengths = {longest+1:columns*rows}
	for length in range(1,longest+1):
		lengths[length] = 2*slope[0]*slope[1]
	return lengths

# print getn(2,2,(1,2))

def threerow(m,n):
	remove = 0
	N = (m+1)*(n+1)
	for rise in range(1,(n+1)/3):
		print rise
		for run in range(1,(m+1)/3):
			if mex(rise,run):
				slope = (rise,run)
				lengths = getn(m,n,slope)
				# print slope,lengths
				for length in lengths:
					if length >= 3:
						remove += (choose(length,3) * (N-length))
						if length >= 4:
							remove += choose(length,4)
	return remove


def Q(m,n):
	full = choose((m+1)*(n+1),4)
	removeslope = 2*threerow(m,n)
	removestraight = 0
	if m >= 2:
		removestraight += choose((m+1),3) * m * (m+1) * (n+1)
		if m >= 3:
			removestraight += choose((m+1),4) * n
	if n >= 2:
		removestraight += choose((n+1),3) * (m+1) * n * (n+1)
		if n >= 3:
			removestraight += choose((n+1),4) * m
	return full - removeslope - removestraight

print Q(12345,6789)