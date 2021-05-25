from dev.DFA import Gate, Formula
import numpy as np
from dev.influence import find_influences as inf
from copy import deepcopy as copy

gate_1 = Gate('OR')
gate_1.add_variable('a0')
gate_1.add_variable('a1')

gate_2 = Gate('OR')
gate_2.add_variable('b2')
gate_2.add_variable('b3')

gate_3 = Gate('AND')
gate_3.add_gate(gate_1)
gate_3.add_gate(gate_2)

gate_4 = Gate('OR')
gate_4.add_gate(gate_3)
gate_4.add_variable('c4')

gate_5 = Gate('AND')
gate_5.add_gate(gate_4)
gate_5.add_variable('d5')

gate_6 = Gate('OR')
gate_6.add_gate(gate_5)
gate_6.add_variable('e6')

gate_7 = Gate('AND')
gate_7.add_variable('f8')
gate_7.add_variable('f9')

gate_8 = Gate('OR')
gate_8.add_gate(gate_7)
gate_8.add_variable('g7')

gate_9 = Gate('AND')
gate_9.add_gate(gate_6)
gate_9.add_gate(gate_8)

gate = {'a': 'OR', 'b': 'OR', 'c': 'OR', 'd': 'AND', 'e': 'OR', 'f': 'AND', 'g': 'OR'}

f = Formula(gate_9)

# prob = {'a0': 0.2, 'a1': 0.3, 'b2': 0.1, 'b3': 0.5, 'c4': 0.7, 'd5': .9, 'e6': .4, 'g7': .3, 'f8': .1, 'f9': .8}
prob = {'a0': 0.5, 'a1': 0.5, 'b2': 0.5, 'b3': 0.5, 'c4': 0.5, 'd5': .5, 'e6': .5, 'g7': .5, 'f8': .5, 'f9': .5}
cost = {'a0': 1, 'a1': 1, 'b2': 1, 'b3': 1, 'c4': 1, 'd5': 1, 'e6': 1, 'g7': 1, 'f8': 1, 'f9': 1}

skip_strategy = f.get_dfa(prob, cost)

f.show()

print(skip_strategy)
unflatten_strategy = []
initial = ''
tmp = []
for each in skip_strategy:
	if each[0] != initial:
		if tmp:
			unflatten_strategy.append([gate[initial]] + tmp)
		tmp = [int(each[1:])]
		initial = each[0]
	else:
		tmp.append(int(each[1:]))
if tmp:
	unflatten_strategy.append([gate[initial]] + tmp)

print(unflatten_strategy)


class Node:
	def __init__(self, index):
		self.index = index
		self.val = None
		self.lchild = None
		self.rchild = None


class Tree:
	def __init__(self, n, s):
		self.max_level = n
		self.root = None
		self.dfa_modified = [None] * (2 ** n - 1)
		self.build_tree(0, 0, s)

	def build_tree(self, level, index, s):
		# print(index)
		# print(s)
		if not s:
			return None
		if level == self.max_level:
			return None
		root = Node(index)
		root.val = s[0][1]
		# print(root.val)
		self.dfa_modified[index] = root.val
		if s[0][0] == 'OR':
			rs = copy(s)
			rs = rs[1:]
			ls = copy(s)
			ls[0].remove(root.val)
			if len(ls[0]) == 1:
				ls = ls[1:]
			root.lchild = self.build_tree(level + 1, index * 2 + 1, ls)
			root.rchild = self.build_tree(level + 1, index * 2 + 2, rs)
		elif s[0][0] == 'AND':
			rs = copy(s)
			ls = copy(s)
			rs[0].remove(root.val)
			if len(rs[0]) == 1:
				rs = rs[1:]
			ls = ls[1:]
			root.lchild = self.build_tree(level + 1, index * 2 + 1, ls)
			root.rchild = self.build_tree(level + 1, index * 2 + 2, rs)
		return root

	def get_modified_dfa(self):
		return self.dfa_modified


n = 10

T = Tree(n, unflatten_strategy)
dfa = T.get_modified_dfa()
print(dfa)

complete_list = []
for i in range(2 ** n - 1):
	# print()
	# print(i)
	if i == 0:
		complete_list.append([dfa[0], [i for i in range(n) if i != dfa[0]]])
	else:
		if dfa[i] is not None:
			complete_list.append([dfa[i], [j for j in complete_list[(i - 1) // 2][1] if j != dfa[i]]])
			# print(i, dfa[i], (i - 1) // 2)
			# print(complete_list[(i - 1) // 2][1])
			# print([i for i in complete_list[(i - 1) // 2][1] if i != dfa[i]])
		else:
			complete_list.append([complete_list[(i - 1) // 2][1][0], [i for i in complete_list[(i - 1) // 2][1][1:]]])

# print(complete_list)
print([i[0] for i in complete_list])

# print(len([7, 8, 8, 6, 9, 6, 9, 0, 0, 6, 6, 0, 0, 6, 6, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
# ))