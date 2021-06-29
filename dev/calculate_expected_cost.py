import copy
import tqdm
import numpy as np
from dev import influence, RandomInput, strategy_generation

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

    def calculate_strategy_cost(self, strategy, costs, probs, verification=None):
        self.root = self.build_tree(0, 0)
        self.fill_strategy(strategy, costs, probs)
        # for _ in range(self.max_level):
        # 	self.pruning()
        return self.calculate_tree_cost(self.root, verification=verification)

    def calculate_tree_cost(self, node, verification=None):
        if verification is None:
            if node.leaf is True:
                return node.probability_to_reach_this_node * node.cost_to_reach_this_node
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
        tmp_p = [0.5] * self.max_level
        for i in range(self.max_level):
            if assignment[i] is not None:
                tmp_p[i] = assignment[i]

        total_inf = sum(influence.find_influences(self.max_level, self.expression, tmp_p))
        if total_inf == 0:
            return True
        return False


if __name__ == "__main__":  # file is imported as library to dynprog3

    def example(x):
        return (x[0] and x[1] and x[2] and x[6]) \
               or (x[0] and x[1] and x[5] and x[7]) \
               or (x[0] and x[4] and x[2] and x[8]) \
               or (x[0] and x[4] and x[5] and x[9]) \
               or (x[3] and x[1] and x[2] and x[10]) \
               or (x[3] and x[1] and x[5] and x[11]) \
               or (x[3] and x[4] and x[2] and x[12]) \
               or (x[3] and x[4] and x[5] and x[13])


    T = Tree(14, example)
    c = [1]*14
    p = [0.5]*14

    # na_s = strategy_generation.generate_non_adaptive(6)
    #
    # res = []
    # for i in tqdm.tqdm(range(len(na_s))):
    #     res.append(T.calculate_strategy_cost(na_s[i], c, p))

    # print(min(res))
    print(T.calculate_strategy_cost([0]+[3]*2+[1]*4+[4]*8+[2]*16+[5]*32+[6]*64+[7]*128+[8]*256+[9]*512+[10]*1024+[11]*2048+[12]*4096+[13]*8192, c, p))
