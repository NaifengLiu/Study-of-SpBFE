import influence
import calculate_influences_using_fourier_expansion
import RandomInput
import numpy as np


def exp(t): return 1 if sum(t) >= 3 else 0


while True:
	# p = RandomInput.get_random_probabilities(5)
	# p.sort()
	p = [0.1, 0.2, 0.3, 0.4, 0.8]

	# calculate_influences_using_fourier_expansion.f(5, exp, p)

	print(influence.find_prob_flipping_f(5, exp, p))
	max_inf = np.argsort(influence.find_prob_flipping_f(5, exp, p))[-1]
	print(max_inf)
	if max_inf != 2:
		if len(set(p)) == 5:
			print(p)
			break
	print()