import numpy as np
from influence import find_influences as inf
from fourier import influencesfromexpression
from copy import deepcopy as copy


def get_strategy(n, p, expression):
	assignment = [None] * n
	strategy = []
	for i in range(2 ** n - 1):
		if i == 0:
			influences1 = inf(n, expression, p)
			print(expression([[0,0,0,0,1,0,1], [0,0,0,0,1,0,0]]))
			print(n)
			influences2 = influencesfromexpression(n, expression, [1/2**n]*2**n)
			print(influences1)
			print(influences2)
			strategy.append([np.argmax(influences1), assignment])
		else:
			tmp_p = copy(p)
			parent_strategy = strategy[(i - 1) // 2]
			previous_assignment = parent_strategy[1]
			new_assignment = previous_assignment[:parent_strategy[0]] + [(i - 1) % 2] + previous_assignment[parent_strategy[0] + 1:]
			for j in range(n):
				if new_assignment[j] is not None:
					tmp_p[j] = new_assignment[j]
			influences = inf(n, expression, tmp_p)
			if sum(influences) == 0:
				first_not_tested = 0
				for j in range(n):
					if new_assignment[j] is None:
						first_not_tested = j
						break
				strategy.append([first_not_tested, new_assignment])
			else:
				strategy.append([np.argmax(inf(n, expression, tmp_p)), new_assignment])
	strategy_output = []
	for each in strategy:
		strategy_output.append(each[0])

	return strategy_output

if __name__ == "__main__": # file is imported as library to dynprog3
	def exp22(t): return (t[0] or t[1]) and (t[2] or t[3])


	#print(inf(4, exp22, [0.3, 0.6, 0.4, 0.4]))

	#print(get_strategy(4, [0.3, 0.6, 0.4, 0.4], exp22))
