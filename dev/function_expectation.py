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


def expectation(n, expression, p):
	truth_table = f(n, expression)
	print(truth_table)
	expect = 0
	for each in truth_table:
		tmp_p = 1
		for i in range(n):
			if each[i] == 0:
				tmp_p *= (1 - p[i])
			else:
				tmp_p *= p[i]
		expect += tmp_p * (truth_table[each] * 2 - 1)
	return expect


def exp(t): return (t[0] and t[1]) or ((t[2] or t[3]) and (t[4] or t[5]) and t[6])


print(expectation(7, exp, [.5] * 7))
print(0+None)
