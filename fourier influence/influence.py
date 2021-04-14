#From Naifeng

def f(n, expression):
	truth_table = dict()

	# init truth table
	for i in range(2 ** n):
		t = str(bin(i))[2:]
		while len(t) < n:
			t = "0" + t
		t = list(map(int, [t[i] for i in range(n)]))
		truth_table[tuple(t)] = 1 if expression(t) else 0

	#for each in truth_table:
	#	print(str(each) + " : " + str(truth_table[each]))
	return truth_table


def find_prob_flipping_f(n, p, expression, c=False):
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
			if truth_table[tuple(t[:j] + [0] + t[j:])] != truth_table[tuple(t[:j] + [1] + t[j:])]:
				flip[j].append(t[:j] + [0] + t[j:])
				flip[j].append(t[:j] + [1] + t[j:])
	for each in flip:
		#print(str(each) + " : " + str(flip[each]))
		for item in flip[each]:
			tmp = 1
			for i in range(n):
				if item[i] == 1:
					tmp *= p[i]
				else:
					tmp *= 1 - p[i]
			flip_p[each].append(tmp)

	if c == False:
		for each in flip_p:
			print(str(each) + " : " + str(sum(flip_p[each])))
	if c != False:
		for each in flip_p:
			print(str(each) + " : " + str(sum(flip_p[each])/c[each]))

# Page 42 a
#def example42(t): return ((t[0] or t[1]) and (t[2] or t[3])) or t[4]
#find_prob_flipping_f(5, [0.41, 0.34, 0.61, 0.13, 0.05], example42)

# Page 43
#                        ((t[1] or t[2]) and t[0]) or (t[5] and (t[3] or t[4])) 
def example43(t): return ((t[1] or t[2]) and t[0]) or (t[5] and (t[3] or t[4]))
find_prob_flipping_f(6, [.5]*6, example43, c=[1]*6)

