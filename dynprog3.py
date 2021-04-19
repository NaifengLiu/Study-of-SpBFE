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

def findhighestr(tree, costs, probs, dtuple):
    highpath, r = [], -1
    classes, paths = getsiblings(tree, [])
    for sibnum in range(len(dtuple)):
        if len(classes[sibnum]) > 0 and dtuple[sibnum] > 0:
            parent = getparent(tree, paths[sibnum])
            if parent['gate'] == 'OR':
                ratios = [probs[sibnum][i]/costs[sibnum][i] for i in range(len(costs[sibnum]))]
            elif parent['gate'] == 'AND':
                ratios = [(1-probs[sibnum][i])/costs[sibnum][i] for i in range(len(costs[sibnum]))]
            if sorted(ratios)[dtuple[sibnum]-1] > r:
                r = sorted(ratios)[dtuple[sibnum]-1]
                highpath = paths[sibnum] + [np.argsort(-np.array(ratios))[-dtuple[sibnum]]]
                highsibnum = sibnum
    return highpath, highsibnum


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

#n = 5
#alltreesn = trees.generatetrees(n)
#tree = alltreesn[5][4]
# GHJM Example
tree = {'gate':'OR', 'children':['var', 'var', {'gate':'AND', 'children':[{'gate':'OR', 'children':['var', 'var']},{'gate':'OR', 'children':['var', 'var', 'var', 'var', 'var']}]}]}
costs = [[1,1], [1,1,2,2,3], [], [1,1]]
probs = [[.4,.3], [.45,.45,.9,.8,.6], [], [.7,.5]]
# Toy Example
tree = {'gate':'AND', 'children':[{'gate':'OR', 'children':['var', {'gate':'AND', 'children':['var', 'var']}]},{'gate':'OR', 'children':['var', 'var']}]}
costs = [[1,2], [3], [1,2], []]
probs = [[.4, .3], [.2], [.5, .7], []]

classes, paths = getsiblings(tree, [])
print(tree)
print(classes)
print(paths)
sizeclasses = [len(lst) for lst in classes]
reducedtrees = getreducedtrees(sizeclasses)
expectedcost = {}
for m in reducedtrees:
    for dtuple in reducedtrees[m]:
        expectedcost[dtuple] = np.Inf
expectedcost[(0,)*len(sizeclasses)] = 0

for m in range(1,sum(sizeclasses)+1):
    for dtuple in reducedtrees[m]:
        highpath, highsibnum = findhighestr(tree, costs, probs, dtuple)
        parentpath = highpath[:-1]
        # TRUE ARC
        truetuple = dtuple[:highsibnum] + (dtuple[highsibnum]-1,) + dtuple[highsibnum+1:]
        truetuple = resolvetrue(tree, parentpath, truetuple)

        # FALSE ARC
        falsetuple = dtuple[:highsibnum] + (dtuple[highsibnum]-1,) + dtuple[highsibnum+1:]
        falsetuple = resolvefalse(tree, parentpath, falsetuple)

        prob = probs[highsibnum][highpath[-1]]
        cost = costs[highsibnum][highpath[-1]]
        candidate = cost + prob * expectedcost[truetuple] + (1-prob)*expectedcost[falsetuple]
        if candidate < expectedcost[dtuple]:
            expectedcost[dtuple] = candidate

print(expectedcost)
