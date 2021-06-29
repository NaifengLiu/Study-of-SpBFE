import copy
import itertools


def generate(n, candidate=None):
    if candidate is None:
        candidate = list(range(n))
    if n == 2:
        output = [[candidate[0], candidate[1], candidate[1]], [candidate[1], candidate[0], candidate[0]]]
        return output
    elif n > 2:
        output = []
        for i in range(n):
            tmp_head = candidate[i]
            tmp_candidate = copy.deepcopy(candidate)
            tmp_candidate.remove(tmp_head)
            previous = generate(n - 1, candidate=tmp_candidate)
            for a in previous:
                for b in previous:
                    tmp_output = [tmp_head]
                    for j in range(n - 1):
                        tmp_output += a[2 ** j - 1:2 ** (j + 1) - 1] + b[2 ** j - 1:2 ** (j + 1) - 1]
                    output.append(tmp_output)
        return output


def generate_non_adaptive(n):
    all_path = list(itertools.permutations(list(range(n))))
    all_strategies = []
    for each in all_path:
        ret = []
        for i in range(n):
            for _ in range(2**i):
                ret.append(each[i])
        all_strategies.append(ret)
    return all_strategies


# print(len(generate(3)))
# print(len(generate(4)))
# print(len(generate(5)))
# # print((generate(5)[50000]))
