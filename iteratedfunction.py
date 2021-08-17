from scipy import special
import numpy as np

# Branching process
# https://www.math.ucdavis.edu/~gravner/MAT135B/materials/ch14.pdf
# Take a way: all 0 certificates appear with high probability
# in relatively few number of generations

def phi2(s, numchild, probchild):
    result = 0
    for i in range(numchild+1):
        prob = (probchild)**i*(1-probchild)**(numchild-i)
        coeff = special.binom(numchild, i)
        result += prob * coeff * s**i
    return result

def getpolynomial(probchild, numchild):
    return np.array([(probchild)**(numchild-i)*(1-probchild)**i* special.binom(numchild, i) for i in range(numchild+1)])

def getextinction(polynomial):
    modified = np.copy(polynomial)
    modified[-2] = modified[-2] - 1
    roots = np.real(np.roots(modified))
    return np.where(roots > 0, roots, np.inf).min()

def phi(s, polynomial):
    scoeff = np.array([s**i for i in range(len(polynomial)-1, -1, -1)])
    return np.dot(scoeff, polynomial)

s = 0
numchild = 10
probchild = 1/9
iterations = 100
polynomial = getpolynomial(probchild, numchild)
probextinct = getextinction(polynomial)
print('Extinction probability:', probextinct)

for i in range(iterations):
    #s = phi2(s=s, numchild=numchild, probchild=probchild)
    s = phi(s=s, polynomial=polynomial)
    print(s)