import influence
import calculate_influences_using_fourier_expansion
import RandomInput
import numpy as np
import tqdm


# def exp(t): return 1 if sum(t) >= 3 else 0
def exp(t): return ((t[0] or t[1]) and (t[2] or t[3])) or 0
def exp1(t): return ((t[0] or t[1]) and (t[2] or t[3])) or t[4]


while True:
	# p = RandomInput.get_random_probabilities(5)
	# p.sort()
	p = [0.1, 0.2, 0.3, 0.4, 0.8]
	p_2 = [0.1, 0.2, 0.3, 0.4, 0]

	# for _ in tqdm.tqdm(range(100)):
	# 	print(calculate_influences_using_fourier_expansion.f(10, exp, p))

	# for _ in tqdm.tqdm(range(100)):
	print(influence.find_influences(5, exp, p))
	print(influence.find_influences(5, exp1, p_2))
	# print(exp)
	break

	# max_inf = np.argsort(influence.find_influences(5, exp, p))[-1]
	# print(max_inf)
	# if max_inf != 2:
	# 	if len(set(p)) == 5:
	# 		print(p)
	# 		break
	# print()