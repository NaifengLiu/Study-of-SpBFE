import copy
import itertools

import tqdm
import numpy as np
from dev import influence, RandomInput, strategy_generation
from BinaryTree import Node as BNode

print("generating strategies ... ")
strategies = strategy_generation.generate(4)
print("start testing ... ")


class Node:
    def __init__(self, index):
        self.index = index
        self.x = None
        self.assignment = []
        self.boolean_value = None
        self.leaf = False
        self.lchild = None
        self.rchild = None
        self.probability_to_reach_this_node = None
        self.cost_to_reach_this_node = None


class Tree:
    def __init__(self, n, expression):
        self.max_level = n
        self.expression = expression
        self.root = None

    # self.root = self.build_tree(0, 0)

    def build_tree(self, level, index):
        if level == self.max_level + 1:
            return None
        root = Node(index)
        root.assignment = [None] * self.max_level
        root.lchild = self.build_tree(level + 1, index * 2 + 1)
        root.rchild = self.build_tree(level + 1, index * 2 + 2)
        return root

    def fill_strategy(self, strategy, costs, probs):
        self.root.x = strategy[0]
        self.fill_strategy_node(strategy, self.root, [None] * self.max_level, 0, 1, costs, probs)

    def fill_strategy_node(self, strategy, node: Node, assignment, cost_to_reach_this_node,
                           probability_to_reach_this_node, costs, probs):
        if node is not None:
            node.assignment = assignment
            node.cost_to_reach_this_node = cost_to_reach_this_node
            node.probability_to_reach_this_node = probability_to_reach_this_node
            right_assignment = copy.deepcopy(assignment)
            left_assignment = copy.deepcopy(assignment)
            if node.index < 2 ** self.max_level - 1:
                # print(node.index)
                # print(strategy)
                # print()
                node.x = strategy[node.index]

                right_assignment[node.x] = 1
                left_assignment[node.x] = 0
                if self.if_function_resolved(assignment):
                    node.leaf = True
                    # print(path)
                    # print(assignment)
                    for i in range(len(assignment)):
                        if assignment[i] is None:
                            assignment[i] = 0
                    node.boolean_value = self.expression(assignment)
            if node.x is not None:
                self.fill_strategy_node(strategy, node.lchild, left_assignment, cost_to_reach_this_node + costs[node.x],
                                        (1 - probs[node.x]) * probability_to_reach_this_node, costs, probs)
                self.fill_strategy_node(strategy, node.rchild, right_assignment,
                                        cost_to_reach_this_node + costs[node.x],
                                        probs[node.x] * probability_to_reach_this_node, costs, probs)
            else:
                node.boolean_value = 1 if self.expression(node.assignment) else 0
                node.leaf = True

    def build_print_tree(self, node):
        if node.index <= 30:
            if node.leaf is not True:
                root = BNode('x' + str(node.x))
                if node.rchild is not None:
                    root.right = self.build_print_tree(node.rchild)
                if node.lchild is not None:
                    root.left = self.build_print_tree(node.lchild)
                return root
            else:
                root = BNode('+' if node.boolean_value == 1 else '-')
                return root

    def print(self):
        printed_tree = self.build_print_tree(self.root)
        print(printed_tree)

    def calculate_strategy_cost(self, strategy, costs, probs, verification=None):
        self.root = self.build_tree(0, 0)
        self.fill_strategy(strategy, costs, probs)
        # self.print()
        return self.calculate_tree_cost(self.root, verification=verification)

    def calculate_tree_cost(self, node, verification=None):
        if verification is None:
            if node.leaf is True:
                return node.probability_to_reach_this_node * node.cost_to_reach_this_node
            # if node.index in [3,4,5,6]:
            # if node.index in list(range(15,31)):
            #     print(node.index)
            #     print(self.calculate_tree_cost(node.lchild) + self.calculate_tree_cost(node.rchild))
            return self.calculate_tree_cost(node.lchild) + self.calculate_tree_cost(node.rchild)
        else:
            if node.leaf is True:
                if node.boolean_value == verification:
                    return node.probability_to_reach_this_node * node.cost_to_reach_this_node
                else:
                    return 0
            return self.calculate_tree_cost(node.lchild, verification) + self.calculate_tree_cost(node.rchild,
                                                                                                  verification)

    def get_optimal_adaptive_strategy(self, costs, probs, verification=None):
        # print("generating strategies ... ")
        # strategies = strategy_generation.generate(self.max_level)
        # print("start testing ... ")
        # strategy_costs = [self.calculate_strategy_cost(item, costs, probs) for item in strategies]
        strategy_costs = []
        # for i in tqdm.tqdm(range(len(strategies))):
        for i in range(len(strategies)):
            strategy_costs.append(self.calculate_strategy_cost(strategies[i], costs, probs, verification=verification))
        min_cost = sum(costs)
        min_cost_instance = None
        for i in range(len(strategies)):
            if strategy_costs[i] < min_cost:
                min_cost = strategy_costs[i]
                min_cost_instance = strategies[i]
        return min_cost, min_cost_instance

    def if_function_resolved(self, assignment):
        # tmp_p = [0.5] * self.max_level
        # for i in range(self.max_level):
        #     if assignment[i] is not None:
        #         tmp_p[i] = assignment[i]
        #
        # total_inf = sum(influence.find_influences(self.max_level, self.expression, tmp_p))
        # if total_inf == 0:
        #     return True
        # return False
        if if_1_certificate(assignment) or if_0_certificate(assignment):
            # print(assignment)
            return True
        return False


def if_1_certificate(assignment):
    tmp = []
    for each in assignment:
        if each is not None:
            tmp.append(each)
        else:
            tmp.append(0.5)

    if (tmp[0] + tmp[2] + tmp[6] == 3) \
            or (tmp[0] + tmp[2] + tmp[7] == 3) \
            or (tmp[0] + tmp[3] + tmp[8] == 3) \
            or (tmp[0] + tmp[3] + tmp[9] == 3) \
            or (tmp[1] + tmp[4] + tmp[10] == 3) \
            or (tmp[1] + tmp[4] + tmp[11] == 3) \
            or (tmp[1] + tmp[5] + tmp[12] == 3) \
            or (tmp[1] + tmp[5] + tmp[13] == 3):
        return True
    return False


def if_0_certificate(assignment):
    tmp = []
    for each in assignment:
        if each is not None:
            tmp.append(each)
        else:
            tmp.append(0.5)

    t = 0
    t += (tmp[0] * tmp[2] * tmp[6])
    t += (tmp[0] * tmp[2] * tmp[7])
    t += (tmp[0] * tmp[3] * tmp[8])
    t += (tmp[0] * tmp[3] * tmp[9])
    t += (tmp[1] * tmp[4] * tmp[10])
    t += (tmp[1] * tmp[4] * tmp[11])
    t += (tmp[1] * tmp[5] * tmp[12])
    t += (tmp[1] * tmp[5] * tmp[13])

    # print(t)

    if t == 0.0 or t == 0:
        return True
    return False

    # if (tmp[0] * tmp[2] * tmp[6] ) \
    #         + (tmp[0] * tmp[2] * tmp[7] ) \
    #         + (tmp[0] * tmp[3] * tmp[8] ) \
    #         + (tmp[0] * tmp[3] * tmp[9] ) \
    #         + (tmp[1] * tmp[4] * tmp[10] ) \
    #         + (tmp[1] * tmp[4] * tmp[11] ) \
    #         + (tmp[1] * tmp[5] * tmp[12] ) \
    #         + (tmp[1] * tmp[5] + tmp[13] ) == 0.0:
    #     return True
    #
    # return False


if __name__ == "__main__":  # file is imported as library to dynprog3

    # tmp = [None]*14
    # tmp[1] = 1
    # tmp[5] = 0
    # tmp[13] = 0
    # tmp[0] = 0
    # print(if_0_certificate(tmp))
    # def example(x):
    #     return (x[0] and x[2] and x[6]) \
    #            or (x[0] and x[3] and x[7]) \
    #            or (x[1] and x[4] and x[8]) \
    #            or (x[1] and x[5] and x[9])
    #
    #
    # # [0, 1, 8, 4, 3, 9, 2, 7, 6, 5]
    #
    # T = Tree(10, example)
    # c = [1]*10
    # p = [0.5]*10
    #
    # # print(min(res))
    # mincost = T.calculate_strategy_cost([0]+[1]*2+[2]*4+[3]*8+[4]*16+[5]*32+[6]*64+[7]*128+[8]*256+[9]*512, c, p) # 6.369140625
    # print(mincost)
    # mincost = T.calculate_strategy_cost([0]+[1]*2+[2]*4+[3]*8+[4]*16+[5]*32+[6]*64+[7]*128+[8]*256+[9]*512, c, p, verification=1) # 3.236328125
    # print(mincost)
    # mincost = T.calculate_strategy_cost([0]+[1]*2+[2]*4+[3]*8+[4]*16+[5]*32+[6]*64+[7]*128+[8]*256+[9]*512, c, p, verification=0) # 3.1328125
    # # mincost = 6.369140625
    # print(mincost)
    #
    # def make_strategy(order):
    #     return [order[0]]*1+[order[1]]*2+[order[2]]*4+[order[3]]*8+[order[4]]*16+[order[5]]*32+[order[6]]*64+[order[7]]*128+[order[8]]*256+[order[9]]*512
    #
    # print(T.calculate_strategy_cost(make_strategy([0, 1, 8, 4, 3, 9, 2, 7, 6, 5]), c, p)) # 6.166015625
    # print(T.calculate_strategy_cost(make_strategy([0, 1, 8, 4, 3, 9, 2, 7, 6, 5]), c, p, verification=1)) # 2.845703125
    # print(T.calculate_strategy_cost(make_strategy([0, 1, 8, 4, 3, 9, 2, 7, 6, 5]), c, p, verification=0)) # 3.3203125

    ##############################################

    def example(x):
        return (x[0] and x[2] and x[6]) \
               or (x[0] and x[2] and x[7]) \
               or (x[0] and x[3] and x[8]) \
               or (x[0] and x[3] and x[9]) \
               or (x[1] and x[4] and x[10]) \
               or (x[1] and x[4] and x[11]) \
               or (x[1] and x[5] and x[12]) \
               or (x[1] and x[5] and x[13])


    # [11, 0, 8, 6, 3, 10, 13, 4, 1, 12, 9, 5, 2, 7] =
    # [0, 1, 2, 6, 7, 3, 8, 9, 4, 10, 11, 5, 12, 13] = 10.8739013671875
    # [0, 2, 6, 7, 3, 8, 9, 1, 4, 10, 11, 5, 12, 13] = 10.7230224609375
    # [8,  1, 10,  3, 11,  4,  0,  9, 13,  6,  2,  7,  5, 12] = 10.4683837890625
    # [1,  8, 10,  3, 11,  4,  0,  9, 13,  6,  2,  7,  5, 12] = 11.361328125
    # [0, 1, 10, 3, 11, 4, 8, 9, 13, 6, 2, 7, 5, 12] = 10.242919921875  ****
    # [0, 1, 4, 3, 11, 10, 8, 9, 13, 6, 2, 7, 5, 12] = 10.321044921875
    # [13,  1,  8,  4,  9,  0,  3, 10,  5, 12,  2,  7, 11,  6] = 10.157470703125
    # [1,  13,  8,  4,  9,  0,  3, 10,  5, 12,  2,  7, 11,  6] = 10.2369384765625
    T = Tree(14, example)
    c = [1] * 14
    p = [0.5] * 14

    mincost = T.calculate_strategy_cost(
        [0] + [1] * 2 + [2] * 4 + [3] * 8 + [4] * 16 + [5] * 32 + [6] * 64 + [7] * 128 + [8] * 256 + [9] * 512 + [
            10] * 1024 + [11] * 2048 + [12] * 4096 + [13] * 8192, c, p)
    print(mincost)

    # mincost1 = T.calculate_strategy_cost(
    #     [0] + [1] * 2 + [2] * 4 + [3] * 8 + [4] * 16 + [5] * 32 + [6] * 64 + [7] * 128 + [8] * 256 + [9] * 512 + [
    #         10] * 1024 + [11] * 2048 + [12] * 4096 + [13] * 8192, c, p, verification=1)
    # print(mincost1)
    # mincost2 = T.calculate_strategy_cost(
    #     [0] + [1] * 2 + [2] * 4 + [3] * 8 + [4] * 16 + [5] * 32 + [6] * 64 + [7] * 128 + [8] * 256 + [9] * 512 + [
    #         10] * 1024 + [11] * 2048 + [12] * 4096 + [13] * 8192, c, p, verification=0)
    # print(mincost2)

    print("############")


    # mincost = T.calculate_strategy_cost([0]+[1]*2+[2]*4+[3]*8+[4]*16+[5]*32, c, p, verification=1)
    # print(mincost)
    # mincost = T.calculate_strategy_cost([0]+[1]*2+[2]*4+[3]*8+[4]*16+[5]*32, c, p, verification=0)
    # # mincost = 6.369140625
    # print(mincost)

    def make_strategy(order):
        return [order[0]] * 1 + [order[1]] * 2 + [order[2]] * 4 + [order[3]] * 8 + [order[4]] * 16 + [
            order[5]] * 32 + [order[6]] * 64 + [order[7]] * 128 + [order[8]] * 256 + [order[9]] * 512 + [
                   order[10]] * 1024 + [order[11]] * 2048 + [order[12]] * 4096 + [order[13]] * 8192


    #
    # # print(T.calculate_strategy_cost(make_strategy([0, 1, 8, 4, 3, 9, 2, 7, 6, 5]), c, p))
    # # print(T.calculate_strategy_cost(make_strategy([0, 1, 8, 4, 3, 9, 2, 7, 6, 5]), c, p, verification=1))
    # # print(T.calculate_strategy_cost(make_strategy([0, 1, 8, 4, 3, 9, 2, 7, 6, 5]), c, p, verification=0))

    o = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    print(o)
    print(T.calculate_strategy_cost(make_strategy(o), c, p))

    o = [1, 5, 13, 0, 2, 6, 7, 3, 8, 4, 11, 10, 9, 12]
    print(o)
    print(T.calculate_strategy_cost(make_strategy(o), c, p))

    o = [0, 1, 5, 13, 2, 6, 7, 3, 8, 4, 11, 10, 9, 12]
    print(o)
    print(T.calculate_strategy_cost(make_strategy(o), c, p))

    o = [1, 5, 13, 0, 2, 6, 3, 8, 4, 11, 10, 7, 9, 12]
    print(o)
    print(T.calculate_strategy_cost(make_strategy(o), c, p))

    while True:
        #     # current_best = 10.4683837890625
        o = np.random.permutation(14)
        res = T.calculate_strategy_cost(make_strategy(o), c, p)
        #     # print(res)
        #     # break
        #     # res = T.calculate_strategy_cost(make_strategy(o), c, p, verification=1)
        #     # print(res)
        #     # res = T.calculate_strategy_cost(make_strategy(o), c, p, verification=0)
        #     # print(res)
        #     # break
        #     mincost = 9.03955078125
        if res < mincost:
            print("###############")
            print(list(o))
            print(res)
            print(T.calculate_strategy_cost(make_strategy(o), c, p, verification=1))
            print(T.calculate_strategy_cost(make_strategy(o), c, p, verification=0))
            mincost = res
