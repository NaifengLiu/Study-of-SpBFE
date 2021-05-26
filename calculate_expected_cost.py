# import strategy_generation
# import RandomInput

import influence
import operator
from BinaryTree import Node as BNode
from BooleanFunctions import *
from ppbtree import Node as PPNode
from ppbtree import print_tree
# from ppbtree import print_tree_vertically


# print("generating strategies ... ")
# strategies = strategy_generation.generate(4)
# print("start testing ... ")


class Node:
    def __init__(self):
        # self.index = index
        self.x = None
        self.assignment = []
        self.boolean_value = None
        self.leaf = False
        self.lchild = None
        self.rchild = None
        self.probability_to_reach_this_node = None
        self.cost_to_reach_this_node = None


class Tree:
    def __init__(self, n, formula, func, probabilities):
        self.max_level = n
        self.expression = formula.lambda_type
        self.formula = formula
        self.probabilities = probabilities
        self.func = func
        self.root = self.build_tree()
        self.ppprint_tree = None

    def build_tree(self):
        root = Node()
        root.assignment = [None] * self.max_level
        root.cost_to_reach_this_node = 0
        root.probability_to_reach_this_node = 1
        self.build_tree_node(root, self.func)
        return root

    def build_tree_node(self, node, func):
        tmp_prob = [self.probabilities[i] if node.assignment[i] is None else node.assignment[i] for i in range(self.max_level)]
        if sum(influence.find_influences(self.max_level, self.expression, tmp_prob).values()) == 0:
            node.leaf = True
            node.boolean_value = self.expression(node.assignment)
        if node.leaf is not True:
            node.x = func(node, self)
            l_node = Node()
            r_node = Node()
            l_node.cost_to_reach_this_node = node.cost_to_reach_this_node + 1
            r_node.cost_to_reach_this_node = node.cost_to_reach_this_node + 1
            l_node.probability_to_reach_this_node = node.probability_to_reach_this_node * (1 - self.probabilities[node.x])
            r_node.probability_to_reach_this_node = node.probability_to_reach_this_node * self.probabilities[node.x]
            l_node.assignment = [node.assignment[i] if i != node.x else 0 for i in range(self.max_level)]
            r_node.assignment = [node.assignment[i] if i != node.x else 1 for i in range(self.max_level)]
            node.lchild = self.build_tree_node(l_node, func)
            node.rchild = self.build_tree_node(r_node, func)
        return node

    def calculate_expected_cost(self, verification=None):
        return self.calculate_tree_cost(self.root, verification)

    def calculate_tree_cost(self, node, verification):
        if verification is None:
            if node.leaf is True:
                return node.probability_to_reach_this_node * node.cost_to_reach_this_node
            return self.calculate_tree_cost(node.lchild, verification) + self.calculate_tree_cost(node.rchild, verification)

    def build_print_tree(self, node):
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

    def ppprint(self):
        ppprint_tree = self.build_pptree(self.root)
        print_tree(ppprint_tree)

    def build_pptree(self, node, parent=None):
        if node.leaf is not True:
            root = PPNode('x' + str(node.x))
            # print(node.x)
            # print(node.lchild.x)
            # print(node.rchild.x)
            # print()
            if node.rchild is not None:
                root.left = self.build_pptree(node.rchild)
            if node.lchild is not None:
                root.right = self.build_pptree(node.lchild)
            return root
        else:
            root = PPNode('[+]' if node.boolean_value == 1 else '[-]')
            return root


def greedy_influence(node: Node, tree: Tree):
    n = tree.max_level
    prob = tree.probabilities
    e = tree.expression
    assignment = node.assignment
    modified_prob = [prob[i] if assignment[i] is None else assignment[i] for i in range(n)]
    influences = influence.find_influences(n, e, modified_prob)
    result = int(max(influences.items(), key=operator.itemgetter(1))[0][1:])
    return result


def greedy_goal_value(node: Node, tree: Tree):
    n = tree.max_level
    prob = tree.probabilities
    formula = copy(tree.formula)
    assignment = node.assignment

    for i in range(len(assignment)):
        if assignment[i] is not None:
            formula.resolve('x'+str(i), str(assignment[i]))

    min_goal, best_test = 2*2**n, None
    for i in range(len(assignment)):
        if assignment[i] is None:
            tmp_pos = copy(formula)
            tmp_pos.resolve('x'+str(i), '1')
            tmp_neg = copy(formula)
            tmp_neg.resolve('x'+str(i), '0')
            candidate_goal = prob[i] * tmp_pos.goal_value + (1-prob[i])*tmp_neg.goal_value
            if candidate_goal < min_goal:
                min_goal = candidate_goal
                best_test = i
    return best_test

## you can either
f = Formula(OR([AND(['x0', 'x1']), AND([OR(['x2', 'x3']), OR(['x4', 'x5']), 'x6'])]))
example = Tree(7, f, greedy_influence, [.5] * 7)
print(example.calculate_expected_cost())
example.print()
#
## or
f = Formula(OR([AND(['x0', 'x1']), AND([OR(['x2', 'x3']), OR(['x4', 'x5']), 'x6'])]))
example = Tree(7, f, greedy_goal_value, [.5] * 7)
print(example.calculate_expected_cost())
example.print()
