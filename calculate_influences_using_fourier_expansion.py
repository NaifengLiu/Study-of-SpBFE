import sympy
import math


def exp(t): return (t[1] or t[2]) and t[0]


def squared_sum(x):
	ret = 0
	for item in x:
		ret += item**2
	return ret


def f(n, expression, probabilities):
	truth_table = dict()

	formula = 0
	x = []
	for i in range(n):
		x.append(0)
		x[i] = sympy.Symbol('x' + str(i))

	# init truth table
	for i in range(2 ** n):
		t = str(bin(i))[2:]
		while len(t) < n:
			t = "0" + t
		t = list(map(int, [t[i] for i in range(n)]))
		truth_table[tuple(t)] = 1 if expression(t) else 0

	for each in truth_table:
		# print(str(each) + " : " + str(truth_table[each]))
		tmp = 1
		for i in range(n):
			item = each[i]
			if item == 0:
				tmp *= (1+((1-2*probabilities[i])+(math.sqrt(4*probabilities[i]*(1-probabilities[i])))*x[i])) /2
			else:
				tmp *= (1-((1-2*probabilities[i])+(math.sqrt(4*probabilities[i]*(1-probabilities[i])))*x[i])) /2
		if truth_table[each] == 0:
			tmp *= 1
		else:
			tmp *= -1
		formula += tmp

	# print()

	# print(formula)
	formula = sympy.simplify(formula)
	# print(formula)

	# mu = sympy.Symbol('m')
	# sigma = sympy.Symbol('s')
	# y = []
	# for i in range(n):
	# 	y.append(0)
	# 	y[i] = sympy.Symbol('y' + str(i))
	#
	# formula = formula.subs({x[0]:mu+sigma*y[0],x[1]:mu+sigma*y[1],x[2]:mu+sigma*y[2]})
	# # formula = formula.subs({mu:0.5, y[0]:0, y[2]:0})
	# print(formula)

	# lambdified_formula = sympy.lambdify([x], formula, 'numpy')
	# print()

	for i in x:
		print(i, end=' : ')
		tmp = str(formula.coeff(i))
		for j in range(n):
			tmp = tmp.replace('x'+str(j), '1')

		tmp = tmp.replace(' ', '')
		tmp = tmp.replace('-', ',')
		tmp = tmp.replace('+', ',')
		if not tmp[0].isdigit():
			tmp = tmp[1:]
		# print(tmp)
		tmp_list = tmp.split(',')
		tmp_list = map(eval, tmp_list)
		print(squared_sum(tmp_list))
		# print(formula.coeff(i))

	print()
	return truth_table


f(3, exp, [0.4,0.9,0.3])

# print((0.348**2+0.372**2+0.828**2+0.972**2)/0.2/0.8)
# print((0.348**2+0.372**2+0.164**2+0.268**2)/0.3/0.7)
# print((0.348**2+0.828**2+0.164**2+0.452**2)/0.1/0.9)
