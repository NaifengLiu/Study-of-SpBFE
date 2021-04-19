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
                highi = sibnum
    return highpath, highi

            
            



#n = 5
#alltreesn = trees.generatetrees(n)
#tree = alltreesn[5][4]
tree = {'gate':'OR', 'children':['var', 'var', {'gate':'AND', 'children':[{'gate':'OR', 'children':['var', 'var']},{'gate':'OR', 'children':['var', 'var', 'var', 'var', 'var']}]}]}
costs = [[1,1], [1,1,2,2,3], [], [1,1]]
probs = [[.4,.3], [.45,.45,.9,.8,.6], [], [.7,.5]]

classes, paths = getsiblings(tree, [])
print(tree)
print(classes)
sizeclasses = [len(lst) for lst in classes]
reducedtrees = getreducedtrees(sizeclasses)
cost = {}
for dtuple in reducedtrees:
    cost[dtuple] = np.Inf
cost = {(0,)*len(sizeclasses):0}


#for m in range(1,sum(sizeclasses)+1):
#    for dtuple in reducedtrees[m]:
#        print(dtuple)

dtuple = (2,3,0,0)
highpath, highi = findhighestr(tree, costs, probs, dtuple)
# TRUE ARC
truetuple = copy(dtuple)
#parent = highpath[:-1]
#if parent['gate'] == 'OR':
#    truetuple[highi] = 0
#    for sibnum in range(len(dtuple)):
#        if paths[sibnum][:len(parent)] == parent:
#            truetuple[sibnum] = 0
    

# parent and, false arc
#dtuple2tree(tree, dtuple)



#I_max = [len(item) for item in f.sibling_classes[0]]
#I_dict = dict()
#
#for i in range(max(I_max) + 1):
#	I_dict[i] = []
#
#I_dict[0] = [[0] * len(I_max)]
#
#for i in range(1, max(I_max) + 1): #I_max = [1,3,5]
#	for item in I_dict[i - 1]:
#		# print(item)
#		for j in range(len(I_max)):
#			if item[j] + 1 <= I_max[j]:
#				I_dict[i].append(item[:j] + [item[j] + 1] + item[j + 1:])
#	I_dict[i].sort()
#	I_dict[i] = list(I_dict[i] for I_dict[i], _ in itertools.groupby(I_dict[i]))  # remove duplicates
#
#print(I_dict)
