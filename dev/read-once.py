import copy
import tqdm
import numpy as np
from dev import calculate_expected_cost, calculate_influences_using_fourier_expansion, influence, RandomInput, strategy_generation, create_strategy_based_on_influences


class Node:
	def __init__(self, index):
		self.index = index
		self.x = None
		self.assignment = []
		self.boolean_value = None
		self.leaf = False
		self.lchild = None
		self.rchild = None
		self.probability_to_reach_this_node = None
		self.cost_to_reach_this_node = None


class Tree:
	def __init__(self, n, expression):
		self.max_level = n
		self.expression = expression
		self.root = None

	# self.root = self.build_tree(0, 0)

	def build_tree(self, level, index):
		if level == self.max_level + 1:
			return None
		root = Node(index)
		root.assignment = [None] * self.max_level
		root.lchild = self.build_tree(level + 1, index * 2 + 1)
		root.rchild = self.build_tree(level + 1, index * 2 + 2)
		return root

	def fill_strategy(self, strategy, costs, probs):
		self.root.x = strategy[0]
		self.fill_strategy_node(strategy, self.root, [None] * self.max_level, 0, 1, costs, probs)

	def fill_strategy_node(self, strategy, node: Node, assignment, cost_to_reach_this_node,
						   probability_to_reach_this_node, costs, probs):
		if node is not None:
			node.assignment = assignment
			node.cost_to_reach_this_node = cost_to_reach_this_node
			node.probability_to_reach_this_node = probability_to_reach_this_node
			right_assignment = copy.deepcopy(assignment)
			left_assignment = copy.deepcopy(assignment)
			if node.index < 2 ** self.max_level - 1:
				node.x = strategy[node.index]
				right_assignment[node.x] = 1
				left_assignment[node.x] = 0
			if node.x is not None:
				self.fill_strategy_node(strategy, node.lchild, left_assignment, cost_to_reach_this_node + costs[node.x],
										(1 - probs[node.x]) * probability_to_reach_this_node, costs, probs)
				self.fill_strategy_node(strategy, node.rchild, right_assignment,
										cost_to_reach_this_node + costs[node.x],
										probs[node.x] * probability_to_reach_this_node, costs, probs)
			else:
				node.boolean_value = 1 if self.expression(node.assignment) else 0
				node.leaf = True

	def pruning(self):
		self.pruning_node(self.root)

	def pruning_node(self, node):
		if node.leaf is not True:
			if node.rchild.boolean_value == node.lchild.boolean_value and node.rchild.boolean_value is not None:
				node.boolean_value = node.rchild.boolean_value
				node.leaf = True
			else:
				self.pruning_node(node.lchild)
				self.pruning_node(node.rchild)

	def calculate_strategy_cost(self, strategy, costs, probs):
		self.root = self.build_tree(0, 0)
		self.fill_strategy(strategy, costs, probs)
		for _ in range(self.max_level):
			self.pruning()
		return self.calculate_tree_cost(self.root)

	def calculate_tree_cost(self, node):
		if node.leaf is True:
			return node.probability_to_reach_this_node * node.cost_to_reach_this_node
		return self.calculate_tree_cost(node.lchild) + self.calculate_tree_cost(node.rchild)

	def get_optimal_adaptive_strategy(self, costs, probs):
		print("generating strategies ... ")
		strategies = strategy_generation.generate(self.max_level)
		print("start testing ... ")
		# strategy_costs = [self.calculate_strategy_cost(item, costs, probs) for item in strategies]
		strategy_costs = []
		for i in tqdm.tqdm(range(len(strategies))):
			strategy_costs.append(self.calculate_strategy_cost(strategies[i], costs, probs))
		min_cost = sum(costs)
		min_cost_instance = None
		for i in range(len(strategies)):
			if strategy_costs[i] < min_cost:
				min_cost = strategy_costs[i]
				min_cost_instance = strategies[i]
		return min_cost, min_cost_instance


def example42(t):
	# return ((t[0] or t[1]) and (t[2] or t[3])) or t[4]
	# return (((((t[0] or t[1]) and (t[2] or t[3])) or t[4]) and t[5]) or t[6]) and (t[7] or (t[8] and t[9]))
	return (t[0] and t[1]) or (t[2] and t[3])

def example0(t):
	return (1 and t[1]) or (t[2] and t[3])

def example1(t):
	return (t[0] and 1) or (t[2] and t[3])

def example2(t):
	return (t[0] and t[1]) or (1 and t[3])

def example3(t):
	return (t[0] and t[1]) or (t[2] and 1)

def example4(t):
	return (0 and t[1]) or (t[2] and t[3])

def example5(t):
	return (t[0] and 0) or (t[2] and t[3])

def example6(t):
	return (t[0] and t[1]) or (0 and t[3])

def example7(t):
	return (t[0] and t[1]) or (t[2] and 0)


# return ((0 or t[1]) and t[0]) or (t[4] and (t[2] or t[3]))
# return ((t[1] or t[2]) and t[0]) or (t[5] and (t[3] or t[4]))
# return ((t[1] and t[2]) or t[0]) and (t[3] or t[4])


for _ in range(10000):
	T = Tree(4, example42)
	c = [1] * 4
	# p = [0.5]*4
	p = [0.8, 0.7, 0.9, 0.5]
	# p = RandomInput.get_random_probabilities(4)
	opt = T.get_optimal_adaptive_strategy(c, p)
	greedy_influence_S = create_strategy_based_on_influences.get_strategy(4, p, example42)
	greedy_influence = T.calculate_strategy_cost(greedy_influence_S, c, p)

	# print(calculate_influences_using_fourier_expansion.exp())
	# print(opt)
	# print(greedy_influence)
	if opt[0] != greedy_influence:
		print(p)
		print(opt)
		print(greedy_influence, end=",")
		print(greedy_influence_S)
		print()
		print(influence.find_influences(4, example42, p))
		print(calculate_influences_using_fourier_expansion.f(4, example42, p))
		print(calculate_influences_using_fourier_expansion.f(4, example0, p))
		print(calculate_influences_using_fourier_expansion.f(4, example4, p))
		print(calculate_influences_using_fourier_expansion.f(4, example1, p))
		print(calculate_influences_using_fourier_expansion.f(4, example5, p))
		print(calculate_influences_using_fourier_expansion.f(4, example2, p))
		print(calculate_influences_using_fourier_expansion.f(4, example6, p))
		print(calculate_influences_using_fourier_expansion.f(4, example3, p))
		print(calculate_influences_using_fourier_expansion.f(4, example7, p))
		break
