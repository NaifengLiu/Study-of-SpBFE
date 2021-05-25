import itertools
import numpy as np


class Gate:
	def __init__(self, gate_type):
		self.gate_type = gate_type
		self.variables = []
		self.types = []
		self.p = None
		self.c = None

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
		self.dfa = []

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

	def get_prob_cost_for_each_gate(self, probabilities, costs):
		formula = self
		for _ in range(len(formula.array_type[0])):
			for i in range(len(formula.array_type[0])):
				# print(formula.array_type[0][i])
				# print(formula.array_type[1][i])
				flag = 0
				for each in formula.array_type[0][i]:
					if type(each) is Gate:
						if each.c is None:
							flag += 1
				if flag == 0:
					tmp_costs = []
					tmp_probabilities = []
					for each in formula.array_type[0][i][1:]:
						if type(each) is str:
							tmp_costs.append(costs[each])
							tmp_probabilities.append(probabilities[each])
						elif type(each) is Gate:
							tmp_costs.append(each.c)
							tmp_probabilities.append(each.p)
					if formula.array_type[0][i][0] == 'OR':
						tmp_p = 1
						for item in tmp_probabilities:
							tmp_p *= 1 - item
						formula.array_type[1][i].p = 1 - tmp_p
						formula.array_type[1][i].c = get_or_expected_cost(tmp_costs, tmp_probabilities)
					elif formula.array_type[0][i][0] == 'AND':
						formula.array_type[1][i].p = np.prod(tmp_probabilities)
						formula.array_type[1][i].c = get_and_expected_cost(tmp_costs, tmp_probabilities)

	def get_dfa(self, probabilities, costs):
		self.get_prob_cost_for_each_gate(probabilities, costs)
		self.dfs(self.f, probabilities, costs)
		return self.dfa

	def dfs(self, gate, probabilities, costs):
		# print(gate)
		tmp_costs = []
		tmp_probs = []

		for each in gate.variables:
			if type(each) is str:
				tmp_costs.append(costs[each])
				tmp_probs.append(probabilities[each])
			elif type(each) is Gate:
				tmp_costs.append(each.c)
				tmp_probs.append(each.p)

		if gate.gate_type == "OR":
			c_over_p = [tmp_costs[i] / tmp_probs[i] for i in range(len(gate.variables))]
			order = np.argsort(c_over_p)
		else:
			c_over_q = [tmp_costs[i] / (1 - tmp_probs[i]) for i in range(len(gate.variables))]
			order = np.argsort(c_over_q)

		for i in order:
			if type(gate.variables[i]) is str:
				# print(gate.variables[i])
				self.dfa.append(gate.variables[i])
			elif type(gate.variables[i]) is Gate:
				self.dfs(gate.variables[i], probabilities, costs)


def get_and_expected_cost(costs, probabilities):
	c_over_q = []
	for i in range(len(costs)):
		c_over_q.append(costs[i] / (1 - probabilities[i]))
	order = np.argsort(c_over_q)
	total_cost = 0
	c = 0
	p = 1
	for each in order:
		c += costs[each]
		total_cost += c * p * (1 - probabilities[each])
		p *= probabilities[each]
	total_cost += p * sum(costs)
	return total_cost


def get_or_expected_cost(costs, probabilities):
	c_over_p = []
	for i in range(len(costs)):
		c_over_p.append(costs[i] / probabilities[i])
	order = np.argsort(c_over_p)
	total_cost = 0
	c = 0
	p = 1
	for each in order:
		c += costs[each]
		total_cost += c * p * probabilities[each]
		p *= (1 - probabilities[each])
	total_cost += p * sum(costs)
	return total_cost


# def get_strategy(formula: Formula, probabilities, costs):
# 	for _ in range(len(formula.array_type[0])):
# 		for i in range(len(formula.array_type[0])):
# 			# print(formula.array_type[0][i])
# 			# print(formula.array_type[1][i])
# 			flag = 0
# 			for each in formula.array_type[0][i]:
# 				if type(each) is Gate:
# 					if each.c is None:
# 						flag += 1
# 			if flag == 0:
# 				tmp_costs = []
# 				tmp_probabilities = []
# 				for each in formula.array_type[0][i][1:]:
# 					if type(each) is str:
# 						tmp_costs.append(costs[each])
# 						tmp_probabilities.append(probabilities[each])
# 					elif type(each) is Gate:
# 						tmp_costs.append(each.c)
# 						tmp_probabilities.append(each.p)
# 				if formula.array_type[0][i][0] == 'OR':
# 					tmp_p = 1
# 					for item in tmp_probabilities:
# 						tmp_p *= 1 - item
# 					formula.array_type[1][i].p = 1 - tmp_p
# 					formula.array_type[1][i].c = get_or_expected_cost(tmp_costs, tmp_probabilities)
# 				elif formula.array_type[0][i][0] == 'AND':
# 					formula.array_type[1][i].p = np.prod(tmp_probabilities)
# 					formula.array_type[1][i].c = get_and_expected_cost(tmp_costs, tmp_probabilities)
#
# 	for


# gate_alpha = Gate('OR')
# gate_alpha.add_variable('a1')
# gate_alpha.add_variable('a2')
#
# gate_beta = Gate('OR')
# gate_beta.add_variable('b1')
# gate_beta.add_variable('b2')
# gate_beta.add_variable('b3')
# gate_beta.add_variable('b4')
# gate_beta.add_variable('b5')
#
# gate_gamma = Gate('AND')
# gate_gamma.add_gate(gate_alpha)
# gate_gamma.add_gate(gate_beta)
#
# gate_delta = Gate('OR')
# gate_delta.add_variable('c1')
# gate_delta.add_variable('c2')
# gate_delta.add_gate(gate_gamma)
#
# f = Formula(gate_delta)
#
# cost = dict()
# cost['a1'] = 1
# cost['a2'] = 1
# cost['b1'] = 1
# cost['b2'] = 1
# cost['b3'] = 2
# cost['b4'] = 2
# cost['b5'] = 3
# cost['c1'] = 1
# cost['c2'] = 1
#
# prob = dict()
# prob['a1'] = 0.4
# prob['a2'] = 0.3
# prob['b1'] = 0.45
# prob['b2'] = 0.45
# prob['b3'] = 0.9
# prob['b4'] = 0.8
# prob['b5'] = 0.6
# prob['c1'] = 0.7
# prob['c2'] = 0.5
#
# f.get_prob_cost_for_each_gate(prob, cost)
# print(f.get_dfa(prob, cost))


