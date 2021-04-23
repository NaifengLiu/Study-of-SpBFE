import trees
import itertools
from copy import deepcopy as copy
import numpy as np

def getsiblings(tree, path):
    currentclass = []
    allpaths = []
    allclasses = []
    for i in range(len(tree['children'])):
        if tree['children'][i] == 'var':
            currentclass += [tree['children'][i]]
        else:
            classesi, pathsi = getsiblings(tree['children'][i], path + [i])
            allclasses += [*classesi]
            allpaths += [*pathsi]
    allpaths += [path]
    allclasses += [currentclass]
    return allclasses, allpaths

def getunit(tree):
    classes, paths = getsiblings(tree, [])
    unitcosts, unitprobs = [], []    
    for sibclass in classes:
        unitcosts += [[1]*len(sibclass)]
        unitprobs += [[.5]*len(sibclass)]
    return unitcosts, unitprobs

def getreducedtrees(sizeclasses):
    reducedtrees = {0: [(0,) * len(sizeclasses)]}
    for numvar in range(1, sum(sizeclasses)+1):
        reducedtrees[numvar] = []
        for reducedtree in reducedtrees[numvar-1]:
            for j in range(len(sizeclasses)):
                if reducedtree[j] + 1 <= sizeclasses[j]:
                    reducedtrees[numvar] += [reducedtree[:j] + (reducedtree[j]+1,) + reducedtree[j+1:]]
        reducedtrees[numvar].sort()
        reducedtrees[numvar] = list(tree for tree, _ in itertools.groupby(reducedtrees[numvar]))
    return reducedtrees

def getparent(tree, path):
    parent = tree
    for i in path:
        parent = parent['children'][i]    
    return parent

def findhighestr(tree, costs, probs, dtuple, sibnum):
    classes, paths = getsiblings(tree, [])
    parent = getparent(tree, paths[sibnum])
    if parent['gate'] == 'OR':
        ratios = [probs[sibnum][i]/costs[sibnum][i] for i in range(len(costs[sibnum]))]
    elif parent['gate'] == 'AND':
        ratios = [(1-probs[sibnum][i])/costs[sibnum][i] for i in range(len(costs[sibnum]))]
    return np.argsort(-np.array(ratios))[-dtuple[sibnum]]

def eradicatedescendants(tree, parentpath, dtuple):
    classes, paths = getsiblings(tree, [])
    for sibnum in range(len(dtuple)):
        if paths[sibnum][:len(parentpath)] == parentpath:
            dtuple = dtuple[:sibnum] + (0,) + dtuple[sibnum+1:]
    return dtuple

def livedescendants(tree, parentpath, dtuple):
    classes, paths = getsiblings(tree, [])
    numdescendants = 0
    for sibnum in range(len(dtuple)):
        if paths[sibnum][:len(parentpath)] == parentpath:
            numdescendants += dtuple[sibnum]
    return numdescendants > 0

def resolvetrue(tree, parentpath, truetuple):
    stoprecursion = parentpath == []
    parent = getparent(tree, parentpath)
    if parent['gate'] == 'OR':
        truetuple = eradicatedescendants(tree, parentpath, truetuple)
        if not stoprecursion:
            truetuple = resolvetrue(tree, parentpath[:-1], truetuple)
    elif parent['gate'] == 'AND':
        if not livedescendants(tree, parentpath, truetuple):
            if not stoprecursion:
                truetuple = resolvetrue(tree, parentpath[:-1], truetuple)
    return truetuple

def resolvefalse(tree, parentpath, falsetuple):
    stoprecursion = parentpath == []
    parent = getparent(tree, parentpath)
    if parent['gate'] == 'AND':
        falsetuple = eradicatedescendants(tree, parentpath, falsetuple)
        if not stoprecursion:
            falsetuple = resolvefalse(tree, parentpath[:-1], falsetuple)
    elif parent['gate'] == 'OR':
        if not livedescendants(tree, parentpath, falsetuple):
            if not stoprecursion:
                falsetuple = resolvefalse(tree, parentpath[:-1], falsetuple)
    return falsetuple

def getoptimalcost(tree, costs, probs):
    classes, paths = getsiblings(tree, [])
    sizeclasses = tuple([len(lst) for lst in classes])
    reducedtrees = getreducedtrees(sizeclasses)

    tests = {}
    expectedcost = {}
    for m in reducedtrees:
        for dtuple in reducedtrees[m]:
            expectedcost[dtuple] = np.Inf
    expectedcost[(0,)*len(sizeclasses)] = 0

    for m in range(1,sum(sizeclasses)+1):
        for dtuple in reducedtrees[m]:
            for sibnum in range(len(sizeclasses)):
                if dtuple[sibnum] > 0:
                    varindex = findhighestr(tree, costs, probs, dtuple, sibnum)
                    parentpath = paths[sibnum]
                    # TRUE ARC
                    truetuple = dtuple[:sibnum] + (dtuple[sibnum]-1,) + dtuple[sibnum+1:]
                    truetuple = resolvetrue(tree, parentpath, truetuple)

                    # FALSE ARC
                    falsetuple = dtuple[:sibnum] + (dtuple[sibnum]-1,) + dtuple[sibnum+1:]
                    falsetuple = resolvefalse(tree, parentpath, falsetuple)

                    prob = probs[sibnum][varindex]
                    cost = costs[sibnum][varindex]

                    candidate = cost + prob * expectedcost[truetuple] + (1-prob)*expectedcost[falsetuple]

                    if candidate < expectedcost[dtuple]:
                        expectedcost[dtuple] = candidate
                        tests[dtuple] = {'test': parentpath + [varindex], 'truearc':truetuple, 'falsearc':falsetuple}

    return expectedcost, tests

def toexpression(tree):
    if tree == 'var': return 'var'
    terms = [toexpression(child) for child in tree['children']]
    if tree['gate'] == 'AND': joiner = ' and '
    elif tree['gate'] == 'OR': joiner = ' or '
    return '(' + joiner.join(terms) + ')'

def numbervars(expression):
    index = expression.index('var')
    newexpression = expression[:index]
    for i in range(expression.count('var')):
        expression = expression.replace('var', 't['+str(i)+']', 1)
    return expression

# GHJM Example
tree = {'gate':'OR', 'children':['var', 'var', {'gate':'AND', 'children':[{'gate':'OR', 'children':['var', 'var']},{'gate':'OR', 'children':['var', 'var', 'var', 'var', 'var']}]}]}
costs = [[1,1], [1,1,2,2,3], [], [1,1]]
probs = [[.4,.3], [.45,.45,.9,.8,.6], [], [.7,.5]]
# Example 1 with 5 variables
tree = {'gate':'AND', 'children':[{'gate':'OR', 'children':['var', {'gate':'AND', 'children':['var', 'var']}]},{'gate':'OR', 'children':['var', 'var']}]}
costs = [[1,2], [3], [1,2], []]
probs = [[.4, .3], [.2], [.5, .7], []]
# Example 2 with 4 variables
tree = {'gate':'AND', 'children':['var', {'gate':'OR', 'children':['var', {'gate':'AND', 'children':['var', 'var']}]}]}
classes, paths = getsiblings(tree, [])
costs = [[1,2], [3], [2]]
probs = [[.4, .3], [.2], [.71]]
# Example 3 with 3 variables
tree = {'gate':'AND', 'children':['var', {'gate':'OR', 'children':['var', 'var']}]}
costs = [[3,2], [2]]
probs = [[.2, .3], [.71]]

#expectedcost, tests = getoptimalcost(tree, costs, probs)
#for dtuple in tests:
#    print(dtuple, tests[dtuple], expectedcost[dtuple])

## Exhaustive examples
#n = 3
#alltreesn = trees.generatetrees(n)
#optcosts = []
#for tree in alltreesn[n]:
#    costs, probs = getunit(tree)
#    expectedcost, tests = getoptimalcost(tree, costs, probs)
#    lastdtuple = list(tests.keys())[-1]
#    optcosts += [expectedcost[lastdtuple]]
#
#print(len(optcosts))
#print(len(list(set(optcosts))))

