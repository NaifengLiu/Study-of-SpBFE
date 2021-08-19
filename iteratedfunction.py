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

def converge(iterations, numchild, probchild):
    s = 0
    polynomial = getpolynomial(probchild=probchild, numchild=numchild)
    for i in range(iterations):
        s = phi(s=s, polynomial=polynomial)
        print(s)


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

# Total number of nodes at generation d is k^d
# Expected number of alive nodes at generation d is mu^d=(k/(k-1))^d
# Probability a node is alive is (k/(k-1))^d/k^d=(1/(k-1))^d = (want) = 1/n

s = 0
k = 20
numchild = k
probchild = 1/(k-1)
iterations = 100
polynomial = getpolynomial(probchild, numchild)
probextinct = getextinction(polynomial)
print('Extinction probability:', probextinct)
print('Mu:', np.dot(polynomial, np.array(list(range(len(polynomial)-1, -1, -1)))))

#converge(iterations=100, numchild=numchild, probchild=probchild)