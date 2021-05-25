from copy import deepcopy as copy


def to_expression(e):
	return lambda x: eval(e)


class Gate:
	def __init__(self, gate_type):
		self.gate_type = gate_type
		self.variables = []
		self.types = []
		self.resolved = False
		self.value = None

	def add_variable(self, variable):
		self.variables.append(variable)
		self.types.append('variable')

	def add_gate(self, gate):
		self.variables.append(gate)
		self.types.append('gate')

	def remove(self, variable):
		tmp_variables = []
		tmp_types = []
		for i in range(len(self.variables)):
			if self.variables[i] != variable:
				tmp_variables.append(self.variables[i])
				tmp_types.append(self.types[i])
		self.variables = tmp_variables
		self.types = tmp_types

	def contains(self, variable):
		if variable in self.variables:
			return True
		return False

	def to_string(self):
		if self.resolved is False:
			s = self.gate_type
			content = []
			for i in range(len(self.variables)):
				if self.types[i] == 'variable':
					content.append(self.variables[i])
				else:
					content.append(self.variables[i].to_string())
			return s + '(' + ','.join(content) + ')'
		else:
			return ''


class Formula:
	def __init__(self, gate: Gate):
		self.f = gate
		self.sibling_classes = [[], [], []]
		self.get_sibling_classes(self.f)
		self.array_type = [[], []]
		self.get_array_type(self.f)
		self.lambda_type = self.get_lambda_type()

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
		# print('Done')
		return self.f.to_string()

	def find_gate_contains_variable(self, variable):
		for num in range(len(self.array_type[0])):
			each = self.array_type[0][num]
			if variable in each:
				# return each
				return [each, self.array_type[1][num]]

	def get_lambda_type(self):
		return lambda x: eval(str(self.to_lambda(self.f))[1:-1])

	def to_lambda(self, gate):
		ret = '('
		g_type = ' ' + gate.gate_type.lower() + ' '
		for i in range(len(gate.variables)):
			if gate.types[i] == 'variable':
				ret += gate.variables[i][0] + '[' + gate.variables[i][1:] + ']' + g_type
			else:
				ret += self.to_lambda(gate.variables[i]) + g_type
		ret = ' '.join(ret.split(' ')[:-2])
		ret += ')'
		return ret

	def resolve(self, variable, value):
		# print(variable)
		parent = self.find_gate_contains_variable(variable)[1]
		parent.remove(variable)
		parent.add_variable(str(value))
		# self.show()
		self.if_resolved(f.f)
		# self.show()
		# self.simplify_tree(f.f)
		self.show()

	def if_resolved(self, gate):
		# count_resolved = []
		child_unresolved = False
		for i in range(len(gate.variables)):
			each = gate.variables[i]
			if type(each) is Gate:
				if self.if_resolved(each) is True:
					if (gate.gate_type == 'AND' and each.value == '0') or (gate.gate_type == 'OR' and each.value == '1'):
						gate.value = each.value
						gate.resolved = True
						return True
					elif not each.resolved:
						child_unresolved = True

			elif type(each) is str:
				if (gate.gate_type == 'AND' and each == '0') or (gate.gate_type == 'OR' and each == '1'):
					gate.value = each
					gate.resolved = True
					return True
				elif not str(each[0]).isdigit():
					child_unresolved = True
		# if sum(count_resolved) == 0:
		# 	gate.resolved = False
		# 	return False

		if child_unresolved:
			gate.resolved = False
			return False
		gate.value = '0' if gate.gate_type == 'OR' else '1'
		return True

	# def simplify_tree(self, gate):
	# 	resolved_class_parent = None
	# 	resolved_class = None
	# 	resolved_variable = None
	# 	resolved_variable_parent = None
	# 	for i in range(len(gate.variables)):
	# 		each = gate.variables[i]
	# 		if type(each) is Gate:
	# 			if each.resolved is True:
	# 				resolved_class = each
	# 				resolved_class_parent = self.find_gate_contains_variable(each)[1]
	# 			else:
	# 				self.simplify_tree(each)
	# 		# elif type(each) is str:
	# 		# 	if str(each[0]).isdigit():
	# 		# 		resolved_variable = each
	# 		# 		resolved_variable_parent =
	#
	# 	if resolved_class is not None:
	# 		resolved_class_parent.remove(resolved_class)


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


f = Formula(OR([AND(['x0', 'x1', 'x7']), AND([OR(['x2', 'x3']), OR(['x4', 'x5']), 'x6'])]))
# print(f.find_gate_contains_variable('x0'))
f.show()
f.resolve('x0', 1)
f.resolve('x1', 1)
f.resolve('x7', 1)
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
