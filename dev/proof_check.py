from dev import RandomInput
import numpy as np
import math

def prod(a: list):
	ret = 1
	for each in a:
		ret *= each
	return ret

n = 3
max_f = 0

while True:
	int_list = RandomInput.get_random_costs(n, 1, 100)
	double_list = [i / sum(int_list) for i in int_list]

	double_list = [math.sqrt(1/8),math.sqrt(1/8),(1-2*math.sqrt(1/8))]

	int_list_2 = RandomInput.get_random_costs(n, 1, 100)
	double_list_2 = [i / sum(int_list_2) for i in int_list_2]
	double_list_2 = [math.sqrt(1/8),math.sqrt(1/8),(1-2*math.sqrt(1/8))]

	new_list = [(double_list[i] * double_list_2[i]) for i in range(n)]
	new_list_2 = [(double_list[i] * double_list_2[i])**2 for i in range(n)]
	# new_list_0 = [(1.5*(1-double_list[i])*double_list_2[i]+1-double_list_2[i]) for i in range(n)]
	new_list_0 = [(1+0.5*double_list_2[i]-1.5*new_list[i]) for i in range(n)]
	print(double_list)
	print(double_list_2)
	print(new_list)
	print(new_list_0)
	# new_list_3 = [(1.5*(1-double_list[i])*double_list_2[i]) for i in range(n)]
	new_list_3 = [(1-double_list_2[i]) for i in range(n)]
	# print(new_list)

	# new_list = RandomInput.get_random_probabilities(n)
	# new_list_2 = [item**2 for item in new_list]
	# new_list

	# print(sum(new_list), sum(new_list_2))

	max_term = int(np.argmax(new_list))

	# print(double_list[max_term]*double_list_2[max_term]-(1-double_list[max_term])*(1-double_list_2[max_term]))

	tmp_f = (min(new_list_0))/(1-sum(new_list))
	print((min(new_list_0)),(1-sum(new_list)))
	break
	# print(tmp_f)

	if tmp_f > max_f:
		max_f = tmp_f
		print(new_list)
		print(double_list)
		print(double_list_2)
		print(tmp_f)
		print(min(new_list_0) / (1 - sum(new_list)))
		print()
