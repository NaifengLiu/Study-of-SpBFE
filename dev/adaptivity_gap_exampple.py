import math
from copy import deepcopy as copy
import itertools

p = 0.5


def from_sequence_to_dict(sequence):
    ret = dict()
    for n in range(len(sequence)):
        ret[bin(n)[2:].zfill(int(math.log2(len(sequence))))] = sequence[n]
    return ret


def find_possible_subset(s):
    ret = []
    if s[0] == '1' and s[1] == '0':
        ret = [[0]]
    elif s[0] == '0' and s[1] == '1':
        ret = [[1]]
    elif s[0] == '1' and s[1] == '1':
        ret = [[0], [1]]
    n = int(len(s) / 2)
    for c in range(1, n):
        if s[2 * c] == '0':
            for j in range(len(ret)):
                ret[j].append(1)
        elif s[2 * c + 1] == '0':
            for j in range(len(ret)):
                ret[j].append(0)
        else:
            ret_cp = copy(ret)
            for j in range(len(ret)):
                ret[j].append(1)
            for j in range(len(ret_cp)):
                ret_cp[j].append(0)
            ret = ret + ret_cp
    return ret


def find_possible_subset2(s):
    # print(s)
    if s[:2] != '11':
        ret = [s[:2]]
    else:
        ret = ['01','10']
    n = int(len(s) / 2)
    for c in range(1, n):
        # print(s[2*c:2*c+2])
        if s[2*c:2*c+2] == '11':
            ret_cp = copy(ret)
            for j in range(len(ret)):
                ret[j] += '01'
            for j in range(len(ret_cp)):
                ret_cp[j] += '10'
            ret = ret + ret_cp
        else:
            for j in range(len(ret)):
                ret[j] += s[2*c:2*c+2]
    return ret



def get_all(n):
    ret = []
    total = 0
    for num in range(2 ** n):
        ret.append(bin(num)[2:].zfill(n))
    for each in ret:
        # print(each)
        if get_step(each) is None:
            # print(n+get_rest(each)+1)
            total += (n + get_rest(each) + 1) * 0.5 ** n
        else:
            # print(get_step(each))
            total += get_step(each) * .5 ** n
    print(total)


def cal_cost_with_sequence(n, sequence):
    ret = []
    total = 0
    d = from_sequence_to_dict(sequence)

    for num in range(2 ** n):
        ret.append(bin(num)[2:].zfill(n))
    for each in ret:
        if get_step(each) is None:
            # total += (n + get_rest(each) + 1) * 0.5 ** n
            res = []
            for j in find_possible_subset(each):
                res.append(d[''.join(map(str,j))])
            total += (n + min(res)+1)*0.5**n
        else:
            # print(get_step(each))
            total += get_step(each) * .5 ** n
    return total


def get_step(s):
    n = int(len(s) / 2)
    for c in range(n):
        if s[2 * c] == s[2 * c + 1] == '0':
            return 2 * (c + 1)


def get_rest(s):
    n = int(len(s) / 2)
    tmp = []
    for c in range(n):
        if s[2 * c] == '1':
            tmp.append(0)
        else:
            tmp.append(1)
    tmp = ''.join(map(str, tmp))
    return int(tmp, 2)


def cal_cost(n):
    ret = []
    total = 0
    d = generate_pretty_dict(int(n/2))
    # print(d)
    # d = tmp_dict
    for num in range(2 ** n):
        ret.append(bin(num)[2:].zfill(n))
    for each in ret:
        if get_step(each) is None:
            # total += (n + get_rest(each) + 1) * 0.5 ** n
            # print(each)
            total += (n + d[each])*0.5**n
        else:
            # print(get_step(each))
            total += get_step(each) * .5 ** n
    return total


def generate_pretty_dict(n):
    tmp = []
    d = {}
    for num in range(2 ** n):
        tmp.append(bin(num)[2:].zfill(n))
    for k in range(len(tmp)):
        each = tmp[k]
        s = ''
        for j in range(n):
            if each[j] == '0':
                s += '01'
            else:
                s += '10'
        if s[-1] == '1':
            d[s] = (k+2)/2
        else:
            d[s] = 2**n+1-(k+1)/2
    tmp = []
    for num in range(2 ** (2*n)):
        t = bin(num)[2:].zfill(2*n)
        if get_step(t) is None:
            tmp.append(t)
    for kk in range(n+1,2*n+1):
        for each in tmp:
            if each.count('1')==kk:
                res = []
                # print(find_possible_subset2(each))
                for j in find_possible_subset2(each):
                    res.append(d[j])
                d[each] = min(res)
    return d

# generate_pretty_dict(4)
# get_all(20)

# current = 1
# for i in range(1, 10):
#     current = current * p + (1 - p) * (1 + p * current + 1 - p) + 1
#     print(i, end=",")
#     print(current, end=",")
#     get_all(2*i)

# list(itertools.permutations(list(range(n))))


tmp_dict = {}

tmp_dict['010101'] = 1
tmp_dict['010110'] = 8
tmp_dict['011001'] = 2
tmp_dict['011010'] = 7
tmp_dict['100101'] = 3
tmp_dict['100110'] = 6
tmp_dict['101001'] = 4
tmp_dict['101010'] = 5
tmp_dict['110101'] = 1
tmp_dict['111010'] = 5
tmp_dict['111001'] = 2
tmp_dict['110110'] = 6
tmp_dict['011101'] = 1
tmp_dict['011110'] = 7
tmp_dict['101101'] = 3
tmp_dict['101110'] = 5
tmp_dict['010111'] = 1
tmp_dict['011011'] = 2
tmp_dict['100111'] = 3
tmp_dict['101011'] = 4
tmp_dict['111101'] = 1
tmp_dict['110111'] = 1
tmp_dict['011111'] = 1
tmp_dict['111110'] = 5
tmp_dict['111011'] = 2
tmp_dict['101111'] = 3
tmp_dict['111111'] = 1

current = 1
for i in range(2, 100):
    current = current * p + (1 - p) * (1 + p * current) + 1
    print(current)
    # get_all(2*i)

    costs = []

    # print(cal_cost(2*i))


    # for seq in list(itertools.permutations(list(range(2**i)))):
    #     costs.append([cal_cost_with_sequence(2*i, seq), seq])

    # print(sorted(costs, key=lambda x: x[0])[0])
    # ss = []
    # flag = 0
    # for k in range(int(2**i/4)):
    #     if k%2==0:
    #         ss.append(2*k)
    #         ss.append(2*k+2**(i-1))
    #         ss.append(2*k+2**(i-1)+1)
    #         ss.append(2*k+1)
    #     if k%2==1:
    #         ss.append(2 * k + 2 ** (i - 1))
    #         ss.append(2 * k)
    #         ss.append(2 * k + 1)
    #         ss.append(2 * k + 2 ** (i - 1) + 1)
    # # print(ss)
    # # print(ss)
    # # ss = [0,8,9,1,10,2,3,11,4,12,13,5,14,6,7,15]
    # print(cal_cost_with_sequence(2*i, ss))
    #
    # print()


# print(find_possible_subset('111111111111011111'))
