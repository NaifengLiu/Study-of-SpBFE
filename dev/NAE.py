import math
import itertools
from tqdm import tqdm
import copy
from dev import RandomInput
import platform


def get_adaptive_cost_with_root(p, root_index):
	p = [0] + p
	# p = sympy.symbols('b_0:{}'.format(len(p)+1))
	cost = 0
	remaining_order = list(filter(lambda x: x != root_index, range(1, len(p))))

	right_order = [root_index] + remaining_order
	remaining_order.reverse()
	left_order = [root_index] + remaining_order

	# print(left_order)
	# print(right_order)

	right_tmp_stack = 1
	left_tmp_stack = 1
	for i in range(len(remaining_order) + 1):
		if i != 0:
			# print(right_order[i])
			# print(left_order[i])
			cost += (i + 1) * right_tmp_stack * (1 - p[right_order[i]])
			cost += (i + 1) * left_tmp_stack * p[left_order[i]]

			# print(cost)

		right_tmp_stack *= p[right_order[i]]
		left_tmp_stack *= (1 - p[left_order[i]])

	# cost += (len(p) - 1) * (right_tmp_stack + left_tmp_stack)

	return cost


def get_adaptive_cost(p):
	min_cost = math.inf
	true_root = None
	for i in range(len(p)):
		tmp_cost = get_adaptive_cost_with_root(p, i + 1)
		if tmp_cost < min_cost:
			min_cost = tmp_cost
			true_root = i
	return min_cost, true_root


def get_non_adaptive_cost_with_order(p, order):
	cost = 0
	right_tmp_stack = p[order[0]]
	left_tmp_stack = (1 - p[order[0]])

	# right_tmp_stack = 1
	# left_tmp_stack = 1
	for i in range(1, len(order)):
		cost += (i + 1) * right_tmp_stack * (1 - p[order[i]])
		cost += (i + 1) * left_tmp_stack * p[order[i]]
		right_tmp_stack *= p[order[i]]
		left_tmp_stack *= (1 - p[order[i]])

	# cost += len(p) * (right_tmp_stack + left_tmp_stack)

	return cost


# def get_optimal_non_adaptive_cost(p):
#     min_cost = math.inf
#     min_order = None
#     for order in list(itertools.permutations(range(len(p)))):
#         tmp_cost = get_non_adaptive_cost_with_order(p, order)
#         # print(tmp_cost, order)
#         if tmp_cost < min_cost:
#             min_cost = tmp_cost
#             min_order = order
#             # print("?")
#             # print(tmp_cost, order)
#     return min_cost, min_order

n = 5
max_ratio = 0
while True:
	probs = RandomInput.get_random_probabilities(n, numerator_min=0, numerator_max=100, denominator=100)
	probs.sort()
	# probs=[0,.5,.5,.5,.5]
	# probs = [0.5,0.6,0.8]
	# probs = [0,1,1,1,1]
	# # probs = RandomInput.get_random_probabilities(n)
	# probs.sort()
	# # print([0]+list(reversed(list(range(1,n)))))
	tmp_0 = get_non_adaptive_cost_with_order(probs,[0]+list(reversed(list(range(1,n)))))
	tmp_1 = get_non_adaptive_cost_with_order(probs,[n-1]+list(range(n-1)))
	tmp_2 = get_non_adaptive_cost_with_order(probs,list(range(n)))
	tmp_3 = get_non_adaptive_cost_with_order(probs,list(reversed(range(n))))
	# tmp = min([tmp_0])
	# tmp = min([tmp_0, tmp_1])
	tmp = min([tmp_0, tmp_1, tmp_2, tmp_3])
	adapt = get_adaptive_cost(probs)
	ratio = tmp/adapt[0]
	if ratio > max_ratio:
		max_ratio = ratio
		print(ratio)
		print(probs)
	# if adapt[1]==1:
	# 	print(adapt)
	# 	print(probs)
	# if probs[0]*(1-probs[2])+probs[2]*(1-probs[0]) < probs[1]*(1-probs[2])+(1-probs[1])*probs[0]:
	# 	print(probs)
	# 	break







