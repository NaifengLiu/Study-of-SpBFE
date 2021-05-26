from Gate import Gate
from Formula import Formula
from copy import deepcopy as copy

def OR(children: list):
    OR_gate = Gate('OR')
    for child in children:
        if type(child) is str:
            OR_gate.add_variable(child)
        elif type(child) is Gate:
            OR_gate.add_gate(child)
    return OR_gate


def AND(children: list):
    AND_gate = Gate('AND')
    for child in children:
        if type(child) is str:
            AND_gate.add_variable(child)
        elif type(child) is Gate:
            AND_gate.add_gate(child)
    return AND_gate


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


def class_type(tree):
    tmp_gate = Gate(tree['gate'])
    global index_used
    for child in tree['children']:
        if child == 'var':
            index_used += 1
            tmp_gate.add_variable('x[' + str(index_used) + ']')
    # else:
    # 	tmp_gate.add_gate(class_type(child))
    for child in tree['children']:
        if child != 'var':
            tmp_gate.add_gate(class_type(child))
    return tmp_gate


def lambda_type(tree):
    # print(type(tree))
    tmp_gate = tree['gate'].lower()
    ret = '('
    global index_used
    for child in tree['children']:
        if child == 'var':
            index_used += 1
            ret += 'x[' + str(index_used) + '] ' + tmp_gate + ' '
    # ret = tmp_gate.join(ret.split(tmp_gate)[:-1])
    # print(ret)
    for child in tree['children']:
        if child != 'var':
            ret += lambda_type(child) + ' ' + tmp_gate + ' '
    ret = ' '.join(ret.split(' ')[:-2])
    ret += ')'
    return ret


def generate_all_read_once_functions(num_of_vars):
    alltrees = {1: ['var']}
    for n in range(2, num_of_vars + 1):
        ntrees = []
        partition = [(i, n - i) for i in range(1, n // 2 + 1)]
        for num1, num2 in partition:
            for j in range(len(alltrees[num1])):
                smalltree1 = alltrees[num1][j]
                for k in range(len(alltrees[num2])):
                    smalltree2 = alltrees[num2][k]
                    if num1 != num2 or (num1 == num2 and j <= k):
                        ntrees += [simplify({'gate': 'AND', 'children': [copy(smalltree1), copy(smalltree2)]})]
                        ntrees += [simplify({'gate': 'OR', 'children': [copy(smalltree1), copy(smalltree2)]})]
        alltrees[n] = ntrees

    ret = dict()
    global index_used
    # index_used = 0
    for n in range(2, num_of_vars + 1):
        ret[n] = []
        str_ret = []
        for tree in alltrees[n]:
            index_used = -1
            f = Formula(class_type(tree))
            if f.f.to_string() not in str_ret:
                str_ret.append(f.f.to_string())
                index_used = -1
                f.lambda_type = lambda_type(tree)
                # ret[n].append([f, lambda_type(tree)])
                ret[n].append(f)
    return ret


#f = Formula(OR([AND(['x0', 'x1', 'x7']), AND(['x8', 'x9']), AND([OR(['x2', 'x3']), OR(['x4', 'x5']), 'x6'])]))
## print(f.find_gate_contains_variable('x0'))
#f.show()
#f.resolve('x0', 1)
#f.resolve('x9', 0)
#f.resolve('x5', 1)
#print(f.dnf_size)
#print(f.cnf_size)
# f.show()

# tmp = generate_all_read_once_functions(5)[5][-1]
# print(type(tmp))
# print(tmp.lambda_type)
# tmp.show()
# print(tmp.)


# for each in tmp:
# 	each[0].show()
# 	print(each[1])

# tmp = generate_all_read_once_functions(8)[8][0].show()

# print(tmp)

# def lambda_type(tree):
# 	tmp_gate = tree['gate']
# 	ret = ''
# 	global index_used
# 	for child in tree['children']:
# 		if child == 'var':
# 			index_used += 1
# 			ret += 'x[' + str(index_used) + '] '+tmp_gate
# 	for child in tree['children']:
# 		if child != 'var':
# 			tmp_gate.add_gate(class_type(child))
# 	return tmp_gate
