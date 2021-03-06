def f(n, expression):
    truth_table = dict()
    # init truth table
    for i in range(2 ** n):
        t = str(bin(i))[2:]
        while len(t) < n:
            t = "0" + t
        t = list(map(int, [t[i] for i in range(n)]))
        truth_table[tuple(t)] = 1 if expression(t) else 0

    return truth_table


def find_influences(n, expression, p):
    # print(n)
    # print(p)
    truth_table = f(n, expression)

    positive_indexes = []
    for i in range(len(truth_table.keys())):
        if truth_table[list(truth_table.keys())[i]] == 1:
            positive_indexes.append(i)
    print(','.join(map(str, positive_indexes)))

    flip = dict()
    flip_p = dict()
    influences = dict()
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
        # print(str(each) + " : " + str(flip[each]))
        for item in flip[each]:
            tmp = 1
            for i in range(n):
                if item[i] == 1:
                    tmp *= p[i]
                else:
                    tmp *= 1 - p[i]
            flip_p[each].append(tmp)

    for i in range(n):
        influences['x' + str(i)] = 4 * p[i] * (1 - p[i]) * sum(flip_p[i])

    return influences


def find_bias(n, expression, p):
    truth_table = f(n, expression)
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


def e(x): return (x[0] and x[2] and x[6]) \
                 or (x[0] and x[3] and x[7]) \
                 or (x[1] and x[4] and x[8]) \
                 or (x[1] and x[5] and x[9])


infs = find_influences(10, e, [0.5] * 10)
print(infs)
# w = [1.5,1.5,1,1.5]
# ret = [infs['x'+str(i)]/w[i] for i in range(len(infs))]
# print(ret)
