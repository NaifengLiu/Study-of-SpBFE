import itertools
import numpy as np
import math


class Gate:
	def __init__(self, gate_type):
		self.gate_type = gate_type
		self.variables = []
		self.types = []

	def add_variable(self, variable):
		self.variables.append(variable)
		self.types.append('variable')

	def add_gate(self, gate):
		self.variables.append(gate)
		self.types.append('gate')

	def contains(self, variable):
		if variable in self.variables:
			return True
		return False

	def to_string(self):
		s = self.gate_type
		content = []
		for i in range(len(self.variables)):
			if self.types[i] == 'variable':
				content.append(self.variables[i])
			else:
				content.append(self.variables[i].to_string())
		return s + '(' + ','.join(content) + ')'


class Formula:
	def __init__(self, gate: Gate):
		self.f = gate
		self.sibling_classes = [[], [], []]
		self.get_sibling_classes(self.f)
		self.array_type = [[], []]
		self.get_array_type(self.f)

	def get_array_type(self, gate):
		ret = [gate.gate_type]
		for each in gate.variables:
			ret.append(each)
		self.array_type[0].append(ret)
		self.array_type[1].append(gate)

		for num in range(len(gate.variables)):
			if gate.types[num] == 'gate':
				self.get_array_type(gate.variables[num])

	def get_sibling_classes(self, gate):
		# print(gate.to_string())
		ret = []
		for i in range(len(gate.variables)):
			if gate.types[i] == 'variable':
				ret.append(gate.variables[i])
			else:
				self.get_sibling_classes(gate.variables[i])
		if len(ret) > 0:
			self.sibling_classes[0].append(ret)
			self.sibling_classes[1].append(gate.gate_type)
			self.sibling_classes[2].append(gate)

	def show(self):
		print(self.f.to_string())

	def find_gate_contains_variable(self, variable):
		for num in range(len(self.array_type[0])):
			each = self.array_type[0][num]
			if variable in each:
				# return each
				return [each, self.array_type[1][num]]
		#
		#
		# for each in self.array_type[0]:
		# 	if variable in each:
		# 		return each


gate_alpha = Gate('OR')
gate_alpha.add_variable('a1')
gate_alpha.add_variable('a2')

gate_beta = Gate('OR')
gate_beta.add_variable('b1')
gate_beta.add_variable('b2')
gate_beta.add_variable('b3')
gate_beta.add_variable('b4')
gate_beta.add_variable('b5')

gate_gamma = Gate('AND')
gate_gamma.add_gate(gate_alpha)
gate_gamma.add_gate(gate_beta)

gate_delta = Gate('OR')
gate_delta.add_variable('c1')
gate_delta.add_variable('c2')
gate_delta.add_gate(gate_gamma)

f = Formula(gate_delta)

f.show()
print()
print(f.sibling_classes)
print(f.array_type)

I_max = [len(item) for item in f.sibling_classes[0]]

I_dict = dict()

for i in range(max(I_max) + 1):
	I_dict[i] = []

I_dict[0] = [[0] * len(I_max)]

for i in range(1, max(I_max) + 1):
	for item in I_dict[i - 1]:
		# print(item)
		for j in range(len(I_max)):
			if item[j] + 1 <= I_max[j]:
				I_dict[i].append(item[:j] + [item[j] + 1] + item[j + 1:])
	I_dict[i].sort()
	I_dict[i] = list(I_dict[i] for I_dict[i], _ in itertools.groupby(I_dict[i]))  # remove duplicates

print(I_dict)

cost = dict()
cost['a1'] = 1
cost['a2'] = 1
cost['b1'] = 1
cost['b2'] = 1
cost['b3'] = 2
cost['b4'] = 2
cost['b5'] = 3
cost['c1'] = 1
cost['c2'] = 1

prob = dict()
prob['a1'] = 0.4
prob['a2'] = 0.3
prob['b1'] = 0.45
prob['b2'] = 0.45
prob['b3'] = 0.9
prob['b4'] = 0.8
prob['b5'] = 0.6
prob['c1'] = 0.7
prob['c2'] = 0.5

TreeCost = dict()
FirstTest = dict()
TrueArc = dict()
FalseArc = dict()


for m in range(1, max(I_max) + 1):
	for I in I_dict[m]:
		print()
		print(I)
		L = []
		L_R_ratio = []
		for i in range(len(I_max)):
			if I[i] != 0:
				L.append(f.sibling_classes[0][i][-I[i]])
				if f.sibling_classes[1][i] == 'AND':
					L_R_ratio.append((1 - prob[f.sibling_classes[0][i][-I[i]]]) / cost[f.sibling_classes[0][i][-I[i]]])
				else:
					L_R_ratio.append(prob[f.sibling_classes[0][i][-I[i]]] / cost[f.sibling_classes[0][i][-I[i]]])
		order = np.argsort(L_R_ratio)
		print(L[order[-1]])

		# print(f.sibling_classes)

		gate_contains_first_test = f.find_gate_contains_variable(L[order[-1]])

		print(gate_contains_first_test)

		if len(gate_contains_first_test) == 2:
		# True Arc
		# resolve gate to 1
		# False Arc
		# resolve gate to 0
		elif len(gate_contains_first_test) > 2:
			if gate_contains_first_test[0] == 'AND':
				# True Arc
				# reduce sibling class
				# False Arc
				# resolve gate to 0
			elif gate_contains_first_test[0] == 'OR':
				# True Arc
				# resolve gate to 1
				# False Arc
				# reduce sibling class



