import RandomInput
import numpy as np


def f(n, expression):
	truth_table = dict()

	# init truth table
	for i in range(2 ** n):
		t = str(bin(i))[2:]
		while len(t) < n:
			t = "0" + t
		t = list(map(int, [t[i] for i in range(n)]))
		truth_table[tuple(t)] = 1 if expression(t) else 0

	# for each in truth_table:
	# 	print(str(each) + " : " + str(truth_table[each]))

	return truth_table


def find_prob_flipping_f(n, expression, p):
	truth_table = f(n, expression)
	flip = dict()
	flip_p = dict()
	for j in range(n):
		flip[j] = []
		flip_p[j] = []
		for i in range(2 ** (n - 1)):
			t = str(bin(i))[2:]
			while len(t) < n - 1:
				t = "0" + t
			t = list(map(int, [t[i] for i in range(n - 1)]))
			# print(t)
			if truth_table[tuple(t[:j] + [0] + t[j:])] != truth_table[tuple(t[:j] + [1] + t[j:])]:
				flip[j].append(t[:j] + [0] + t[j:])
				flip[j].append(t[:j] + [1] + t[j:])
	for each in flip:
		print(str(each) + " : " + str(flip[each]))
		for item in flip[each]:
			tmp = 1
			for i in range(n):
				if item[i] == 1:
					tmp *= p[i]
				else:
					tmp *= 1 - p[i]
			flip_p[each].append(tmp)

	# for each in flip_p:
	# 	# print(str(each) + " : " + str(p[each] * (1-p[each]) * sum(flip_p[each]) / c[each]))
	# 	print('x' + str(each) + " : " + str(4 * p[each] * (1 - p[each]) * sum(flip_p[each]) / c[each]))
	# print(str(each) + " : " + str(sum(flip_p[each]) / c[each]))
	# print(str(each) + " : " + str(p[each] * sum(flip_p[each]) / c[each]))
	# print()
	return [4 * p[each] * (1 - p[each]) * sum(flip_p[each]) for each in flip_p]


# inf_times_p = [p[each]*sum(flip_p[each]) for each in flip_p]
# inf_times_q = [(1-p[each])*sum(flip_p[each]) for each in flip_p]
# inf_times_pq = [p[each]*(1-p[each])*sum(flip_p[each]) for each in flip_p]
#
# if np.argsort(inf_times_p)[-1] != np.argsort(inf_times_pq)[-1]:
# 	print(p)
# 	# print(inf_times_p)
# 	# print(inf_times_q)
# 	print(inf_times_pq)
# 	print(np.argsort(inf_times_p)[-1], np.argsort(inf_times_q)[-1] , np.argsort(inf_times_pq)[-1])


# def exp(t): return ((t[0] or t[1]) and (t[2] or t[3])) or t[4]
# def exp(t): return 1 if sum(t) == len(t) or sum(t) == 0 else 0
def exp(t): return 1 if sum(t) >= 3 else 0
# def exp(t): return ((t[1] or t[2]) and t[0]) or (t[5] and (t[3] or t[4]))
# def exp(t): return (t[1] or t[2]) and t[0]


# find_prob_flipping_f(5, [0.7, 0.2, 0.2, 0.3, 0.1], [1] * 5)
# find_prob_flipping_f(5, [0.25, 0.45, 0.57, 0.73, 0.78], [1] * 5)
# find_prob_flipping_f(6, [0.5,0.5,0.5,0.5,0.5,0.5], [512, 1.1, 512.2, 8.3, 512.4, 64.5])
# find_prob_flipping_f(3, [0.4,0.9,0.3], [1,1,1])
# while True:
# 	find_prob_flipping_f(5, RandomInput.get_random_probabilities(5))
