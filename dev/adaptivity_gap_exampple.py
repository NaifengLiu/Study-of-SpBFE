p = 0.5

def get_all(n):
    ret = []
    total = 0
    for num in range(2 ** n):
        ret.append(bin(num)[2:].zfill(n))
    for each in ret:
        # print(each)
        if get_step(each) is None:
            # print(n+get_rest(each)+1)
            total += (n+get_rest(each)+1)*0.5**n
        else:
            # print(get_step(each))
            total += get_step(each)*.5**n
    print(total)


def get_step(s):
    n = int(len(s) / 2)
    for c in range(n):
        if s[2 * c] == s[2 * c + 1] == '0':
            return 2 * (c + 1)


def get_rest(s):
    n = int(len(s) / 2)
    tmp = []
    for c in range(n):
        if s[2*c] == '1':
            tmp.append(0)
        else:
            tmp.append(1)
    tmp = ''.join(map(str, tmp))
    return int(tmp, 2)


# get_all(20)

current = 1
for i in range(1, 15):
    current = current * p + (1 - p) * (1 + p * current + 1 - p) + 1
    print(i, end=",")
    print(current, end=",")
    get_all(i*2)

