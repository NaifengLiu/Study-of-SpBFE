import copy
import strategy_generation
import tqdm
import RandomInput
import numpy as np


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

	def fill_strategy_node(self, strategy, node: Node, assignment, cost_to_reach_this_node, probability_to_reach_this_node, costs, probs):
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
				if self.if_function_resolved(assignment):
					node.leaf = True
					node.boolean_value = self.expression(node.assignment)
			if node.x is not None:
				self.fill_strategy_node(strategy, node.lchild, left_assignment, cost_to_reach_this_node + costs[node.x], (1 - probs[node.x]) * probability_to_reach_this_node, costs, probs)
				self.fill_strategy_node(strategy, node.rchild, right_assignment, cost_to_reach_this_node + costs[node.x], probs[node.x] * probability_to_reach_this_node, costs, probs)
			else:
				node.boolean_value = 1 if self.expression(node.assignment) else 0
				node.leaf = True

	def calculate_strategy_cost(self, strategy, costs, probs):
		self.root = self.build_tree(0, 0)
		self.fill_strategy(strategy, costs, probs)
		# for _ in range(self.max_level):
		# 	self.pruning()
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

	def if_function_resolved(self, assignment):
		assignment_0 = copy.deepcopy(assignment)
		assignment_1 = copy.deepcopy(assignment)
		for num in range(len(assignment)):
			if assignment[num] is None:
				assignment_0[num] = 0
				assignment_1[num] = 1
		if self.expression(assignment_0) == self.expression(assignment_1):
			return True
		return False


def example42(t):
	return ((t[1] and t[2]) or t[0]) and (t[3] or t[4])


T = Tree(5, example42)
c = [1, 1, 1, 1, 1]
p = [0.5, 0.5, 0.5, 0.5, 0.5]
print(T.calculate_strategy_cost([0,4,3,1,1,2,2,3,3,3,3,4,4,4,4,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1],c,p))
