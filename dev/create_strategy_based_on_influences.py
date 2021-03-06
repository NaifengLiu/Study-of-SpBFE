import numpy as np
from dev.influence import find_influences as inf
from copy import deepcopy as copy


def get_strategy(n, p, expression):
	print("creating strategies")
	assignment = [None] * n
	strategy = []
	for i in range(2 ** n - 1):
		if i == 0:
			strategy.append([np.argmax(inf(n, expression, p)), assignment])
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

	print("finished creating strategies")
	print(len(strategy_output))
	return strategy_output
