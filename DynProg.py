import itertools
from copy import deepcopy as copy
import numpy as np

from dev import greedy_influence, calculate_expected_cost, trees
from BinaryTree import Node as BNode
from ppbtree import print_tree

import BooleanFunctions

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

def getunit(tree, p=.5):
    classes, paths = getsiblings(tree, [])
    unitcosts, unitprobs = [], []    
    for sibclass in classes:
        unitcosts += [[1]*len(sibclass)]
        unitprobs += [[p]*len(sibclass)]
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

def topartial(tree):
    if tree == 'var': return 'var'
    terms = [topartial(child) for child in tree['children']]
    if tree['gate'] == 'AND': joiner = ' and '
    elif tree['gate'] == 'OR': joiner = ' or '
    return '(' + joiner.join(terms) + ')'

def numbervars(partial):
    index = partial.index('var')
    for i in range(partial.count('var')):
        partial = partial.replace('var', 't['+str(i)+']', 1)
    return partial

def toexpression(tree):
    partial = topartial(tree)
    expression = numbervars(partial)
    return lambda t : eval(expression)

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

def getgreedyinfluencecost(n, tree, p=.5):
    exp = toexpression(tree)
    c, p = [1]*n, [p]*n
    strategy = greedy_influence.get_strategy(n, p, exp)
    #print(strategy)
    T = calculate_expected_cost.Tree(n, exp)
    return T.calculate_strategy_cost(strategy, c, p)

def buildstrategy(tree, expectedcost, tests):
    reducedtree = list(tests.keys())[-1]
    tree = renametree(tree)
    strategy = recursivestrategy(reducedtree, tests=tests, tree=tree)
    return strategy


def recursivestrategy(reducedtree, tests, tree):
    path = tests[reducedtree]['test']
    current = copy(tree)
    for i in path:
        current = current['children'][i]
    root = BNode(current)
    if tests[reducedtree]['falsearc'] != (0,)*len(reducedtree):
        root.left = recursivestrategy(tests[reducedtree]['falsearc'], tests, tree)
    else:
        root.left = BNode('-')
    if tests[reducedtree]['truearc'] != (0,)*len(reducedtree):
        root.right = recursivestrategy(tests[reducedtree]['truearc'], tests, tree)
    else:
        root.right = BNode('+')
    return root

def fixtree(tree):
    variables, gates = [], []
    for i in range(len(tree['children'])):
        if tree['children'][i] == 'var':
            variables += ['var']
        else:
            gates += [fixtree(tree['children'][i])]
    return {'gate':tree['gate'], 'children':variables+gates}

def renametree(tree):
    children = []
    for i in range(len(tree['children'])):
        if tree['children'][i] == 'var':
            global currentnum
            children += ['x'+str(currentnum)]
            currentnum += 1
        else:
            children += [renametree(tree['children'][i])]
    return {'gate':tree['gate'], 'children':children}

def checkincreasing(strategy):
    if strategy.right.value not in ['+', '-']:
        if int(strategy.right.value[1]) < int(strategy.value[1]):
            return True
        if checkincreasing(strategy.right):
            return True
    if strategy.left.value not in ['+', '-']:
        if int(strategy.left.value[1]) < int(strategy.value[1]):
            return True
        if checkincreasing(strategy.left):
            return True
    return False


if __name__ == "__main__":
    n, p = 8, .5
    alltreesn = trees.generatetrees(n)

    for treenum in range(len(alltreesn[n])):
        currentnum = 1 # VERY sketch
        tree = fixtree(alltreesn[n][treenum])
        costs, probs = getunit(tree, p)
        expectedcost, tests = getoptimalcost(tree, costs, probs)
        strategy = buildstrategy(tree, expectedcost, tests)
        outoforder = checkincreasing(strategy)
        if outoforder:
            BooleanFunctions.index_used = 0
            f = BooleanFunctions.Formula(BooleanFunctions.class_type(tree))
            print(treenum)
            f.show()
            strategy.pprint()
            classes, paths = getsiblings(tree, [])
            print(classes)


#    # Exhaustive examples
#    n, p = 7, .5
#    alltreesn = trees.generatetrees(n)
#    optcosts = []
#    #for numvar in range(2,n+1):
#    #    print(numvar)
#    #    for i in range(len(alltreesn[numvar])):
#    #        tree = alltreesn[numvar][i]
#    #        print(i)
#    tree = alltreesn[7][377]
#    numvar = 7
#    #print(tree)
#    costs, probs = getunit(tree, p)
#    expectedcost, tests = getoptimalcost(tree, costs, probs)
#    print(tests)
#    for key in tests:
#        print(key, tests[key])
#    optcost = expectedcost[list(tests.keys())[-1]]
#    greedycost = getgreedyinfluencecost(numvar, tree, p)
#    optcosts += [optcost]
#    print(optcost, greedycost)
#    #assert np.allclose(optcost, greedycost)
#
#    #print(len(optcosts))
#    #print(len(list(set(optcosts))))

