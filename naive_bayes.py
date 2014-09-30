#! /usr/bin/python2

from __future__ import division
import numpy as np

from sys import exit
from collections import OrderedDict

# ------Training data-------------

# Politics
xP = [
     [1, 0, 1, 1, 1, 0, 1, 1],
     [0, 0, 0, 1, 0, 0, 1, 1],
     [1, 0, 0, 1, 1, 0, 1, 0],
     [0, 1, 0, 0, 1, 1, 0, 1],
     [0, 0, 0, 1, 1, 0, 1, 1],
     [0, 0, 0, 1, 1, 0, 0, 1]
]

# Sport
xS = [
     [1, 1, 0, 0, 0, 0, 0, 0],
     [0, 0, 1, 0, 0, 0, 0, 0],
     [1, 1, 0, 1, 0, 0, 0, 0],
     [1, 1, 0, 1, 0, 0, 0, 0],
     [1, 1, 0, 1, 1, 0, 0, 0],
     [0, 0, 0, 1, 0, 1, 0, 0],
     [1, 1, 1, 1, 1, 0, 1, 0]
]

# ---------------------------------

# --------Test data----------------
test_data = [1, 1, 1, 0, 1, 1, 0, 0]
# ---------------------------------


def main(xP, xS, test_data):

    # Create attribute counts table for each class in training data
    xP_attribute_counts = count_values(xP)
    xS_attribute_counts = count_values(xS)

    total_num_instances = len(xP) + len(xS)
    xP_prior_prob = calc_prior_probability(xP, total_num_instances)
    xS_prior_prob = calc_prior_probability(xS, total_num_instances)

    likelihood_xP = calc_likelihood(xP, xP_attribute_counts, test_data)
    likelihood_xS = calc_likelihood(xS, xS_attribute_counts, test_data)

    total_attribute_probability = calc_attrib_prob(xP_attribute_counts,
                                                   xS_attribute_counts,
                                                   total_num_instances,
                                                   test_data)

    xP_prob = calc_bayes_prob(xP_prior_prob,
                                    likelihood_xP,
                                    total_attribute_probability)

    xS_prob = calc_bayes_prob(xS_prior_prob,
                                    likelihood_xS,
                                    total_attribute_probability)

    if max(xP_prob, xS_prob) == xP_prob:
        return 'Politics'
    else:
        return 'Sport'



def calc_prior_probability(clazz, total_num_instances):
    '''
    # Calculates the prior probability for clazz
    '''

    num_instances = len(clazz)
    prior_probability = (num_instances/total_num_instances)

    return prior_probability


def calc_likelihood(clazz, attribute_counts, test_data):
    '''
    # Calculates total likelihood for all attributes in
    # test data according to attribute_count
    '''

    likelihoods = []
    for idx in range(len(test_data)):
        likelihoods.append(attribute_counts[idx][test_data[idx]] / len(clazz))

    return np.prod(likelihoods)


def calc_attrib_prob(xP_counts, xS_counts, total_instances, test_data):
    '''
    # Calculates total probability for all attributes in test_data.
    '''

    attribute_probs = []
    for idx in range(len(xP_counts)):
        attribute_probs.append((xP_counts[idx][test_data[idx]] \
                                + xS_counts[idx][test_data[idx]]) \
                                / total_instances)

    return np.prod(attribute_probs)


def calc_bayes_prob(prior_prob, likelihood, total_attrib_prob):

    return (prior_prob * likelihood) / total_attrib_prob


def count_values(attribute_vector):
    '''
    # Creates an OrderedDict from each attribute vector
    # in clazz, totaling up the counts for each value
    # of each attribute in the attribute vector.

    # p = model_data(xP)
    # p.[3][1] gives the total count of 1's for the attribute
        at index 3 of all sets of xP
    '''

    # Initialize dict to hold counts for each variable value
    # in each set of attribute_vector.
    counts = OrderedDict.fromkeys([x for x in range(len(attribute_vector[0]))])
    for key in counts.keys():
        counts[key] = [0, 0]

    # Count values
    for set in attribute_vector:
        for i in range(len(set)):
            if set[i] == 0:
                counts[i][0] += 1
            elif set[i] == 1:
                counts[i][1] += 1
            else:
                print "ERROR: INVALID VARIABLE VALUE"
                exit(1)

    return counts


if __name__ == '__main__':
    print main(xP, xS, test_data)
