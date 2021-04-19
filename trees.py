# dynamically generate all trees
from copy import deepcopy as copy

def simplify(tree):
    if tree == 'var': return 'var'
    children = []
    for child in tree['children']:
        child = simplify(child)
        if child != 'var' and child['gate'] == tree['gate']:
            children += [*child['children']]
        else:
            children += [child]
    tree['children'] = children
    return tree

def generatetrees(maxvarnum):
    alltrees = {1:['var']}

    for n in range(2, maxvarnum+1):
        ntrees = []
        partition = [(i,n-i) for i in range(1,n//2+1)]
        for num1, num2 in partition:
            for j in range(len(alltrees[num1])):
                smalltree1 = alltrees[num1][j]
                for k in range(len(alltrees[num2])):
                    smalltree2 = alltrees[num2][k]
                    if num1 != num2 or (num1 == num2 and j <= k):
                        ntrees += [simplify({'gate':'AND', 'children':[copy(smalltree1), copy(smalltree2)]})]
                        ntrees += [simplify({'gate':'OR', 'children':[copy(smalltree1), copy(smalltree2)]})]
        alltrees[n] = ntrees
    return alltrees
