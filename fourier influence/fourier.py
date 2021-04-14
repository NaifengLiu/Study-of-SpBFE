import numpy as np

# INPUTS #
n = 6
expression = lambda x : [1,-1][(x[0] and x[1]) or x[2]] # function
expression = lambda x : [1,-1][((x[1] or x[2]) and x[0]) or (x[5] and (x[3] or x[4]))] # function
distribution = np.array([1/2**n]*2**n) # distribution for inner product

# DECOMPOSE #
# number to binary string
convert = lambda num, n: bin(num)[2:].zfill(n) 
# n-bit binary strings
binary = np.array([convert(num, n) for num in np.arange(2**n)]) 
# binary string to subset
subset = lambda bstring : np.array(np.where(np.array([int(x) for x in bstring])==1)) 
# parity of bit string on subset S
parity = lambda x, S : [1, -1][sum(int(x[i.item()]) for i in S.T)%2] 
# binarystring (to subset) to parity vector
pvec = lambda S : np.array([parity(x,S) for x in binary])
# binarystring (to subset) to fourier coefficient
fcoeff = lambda S : np.multiply(pvec(S), distribution).dot(fvec)
# expression in vector form
fvec = np.array([expression([int(xi) for xi in x]) for x in binary]) 
# fourier coefficients
fcoeffs = np.array([fcoeff(subset(bstring)) for bstring in binary])

# TEST #
# reconstructed f
fvec2 = np.sum([fcoeff(subset(x))*np.array([parity(bstring,subset(x)) for bstring in binary]) for x in binary], 0)
assert np.all(fvec == fvec2)

# INFLUENCE #
infi = lambda i : sum([fcoeffs[num]**2 for num in np.arange(2**n) if convert(num,n)[i]=='1'])
inf = sum([fcoeffs[num]**2*convert(num,n).count('1') for num in np.arange(2**n)])
assert inf == sum([infi(i) for i in range(n)])



