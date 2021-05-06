import numpy as np

# FUNCTIONS #
# number to binary string
convert = lambda num, n: bin(num)[2:].zfill(n) 
# n-bit binary strings
binary = lambda n : np.array([convert(num, n) for num in np.arange(2**n)])
# binary string to subset
subset = lambda bstring : np.array(np.where(np.array([int(x) for x in bstring])==1)) 
# parity of bit string on subset S
parity = lambda x, S : [1, -1][sum(int(x[i.item()]) for i in S.T)%2] 
# binarystring (to subset) to parity vector
pvec = lambda S, n : np.array([parity(x,S) for x in binary(n)])
# binarystring (to subset) to fourier coefficient
fcoeff = lambda S, n, fvec, distribution : np.multiply(pvec(S, n), distribution).dot(fvec)
# influence of i
infi = lambda i, fcoeffs, n : sum([fcoeffs[num]**2 for num in np.arange(2**n) if convert(num,n)[i]=='1'])

# FROM EXPRESSION FORM #

def decomposefromexpression(n, expression, distribution, test=True):
    # expression in vector form
    fvec = np.array([expression([int(xi) for xi in x]) for x in binary(n)]) 
    # fourier coefficients
    fcoeffs = np.array([fcoeff(subset(bstring), n, fvec, distribution) for bstring in binary(n)])
    # TEST #
    if test:
        # reconstructed f
        fvec2 = np.sum([fcoeff(subset(x), n, fvec, distribution)*np.array([parity(bstring,subset(x)) for bstring in binary(n)]) for x in binary(n)], 0)
        assert np.all(fvec == fvec2)
    return fcoeffs

def influencefromexpression(n, expression, distribution):
    fcoeffs = decomposefromexpression(n, expression, distribution)
    return sum([fcoeffs[num]**2*convert(num,n).count('1') for num in np.arange(2**n)])

def influenceifromexpression(n, expression, distribution, i, test=True):
    fcoeffs = decomposefromexpression(n, expression, distribution, test=test)
    if test:
        assert influencefromexpression(n, expression, distribution) == sum([infi(i, fcoeffs, n) for i in range(n)])
    return infi(i, fcoeffs, n)

def influencesfromexpression(n, expression, distribution, test=True):
    newexpression = lambda t : [-1, 1][expression(t)]
    influences = []
    for i in range(n):
        influences += [influenceifromexpression(n, newexpression, distribution, i, test=test)]
    return influences

# FROM VECTOR FORM #

def decomposefromvec(n, fvec, distribution):
    return np.array([fcoeff(subset(bstring), n, fvec, distribution) for bstring in binary(n)]) 
   
def influencefromvec(n, fvec, distribution):
    fcoeffs = decomposefromvec(n, fvec, distribution)
    return sum([fcoeffs[num]**2*convert(num,n).count('1') for num in np.arange(2**n)])

def influenceifromvec(n, fvec, distribution, i):
    fcoeffs = decomposefromvec(n, fvec, distribution)
    return infi(i, fcoeffs, n)

if __name__ == "__main__":
    # INPUTS #
    n = 3
    expression = lambda x : [1,-1][(x[0] and x[1]) or x[2]] # function
    #expression = lambda x : [1,-1][((x[1] or x[2]) and x[0]) or (x[5] and (x[3] or x[4]))] # function
    distribution = np.array([1/2**n]*2**n) # distribution for inner product
    infi = influenceifromexpression(n, expression, distribution, 2)
    print(infi)

