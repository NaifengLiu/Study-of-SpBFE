import random
import numpy as np

np.set_printoptions(precision=2)


def get_random_probabilities(num_of_variables, numerator_min=1, numerator_max=9, denominator=10):
    probabilities = []
    for _ in range(num_of_variables):
        probabilities.append(random.randint(numerator_min, numerator_max) / denominator)
    return probabilities


def get_random_probabilities_numpy(num_of_variables):
    return np.random.uniform(0, 1, num_of_variables)


def get_random_costs(num_of_variables, min_cost=1, max_cost=10):
    costs = []
    for _ in range(num_of_variables):
        costs.append(random.randint(min_cost, max_cost))
    return costs


def get_unit_costs(num_of_variables):
    costs = []
    for _ in range(num_of_variables):
        costs.append(1)
    return costs


def get_random_weights(num_of_variables, min_weight=1, max_weight=2):
    weights = []
    for _ in range(num_of_variables):
        weights.append(random.randint(min_weight, max_weight))
    return weights
