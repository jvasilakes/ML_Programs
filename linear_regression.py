#! /usr/bin/python2.7

from __future__ import division, print_function

import sys
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot

"""
Linear regression with two dependent variables.

Usage (with provided data):
    ./linear_regression.py data/regression_data.py 
"""

def main(save=False):
    # Prepare data
    try:
        data_file = sys.argv[1]
    except:
        print("Usage: linear_regression.py <path/to/data_file>")
        sys.exit(1)

    data = read_data(data_file)
    inputs = [x[:-1] for x in data]
    targets = [x[-1] for x in data]

    # Train / compute weight vector
    weights = compute_weights(inputs, targets)
    print("Weight vector: {0}" .format(weights))

    # Predict test data
    predicted = [dot_product(x, weights) for x in inputs]
    # Compute residuals (not used, but can be plotted)
#    residuals = compute_residuals(inputs, targets, weights)

    # Write out the data in CSV format.
    if save:
        with open('predicted.txt', 'w') as out:
            for inp, t in zip(inputs, predicted):
                for i in inp:
                    out.write("{0}, " .format(i))
                out.write("{0}\n" .format(t))
        with open('gold.txt', 'w') as out:
            for inp, t in zip(inputs, targets):
                for i in inp:
                    out.write("{0}, " .format(i))
                out.write("{0}\n" .format(t))
        with open('residuals.txt', 'w') as out:
            for res in residuals:
                out.write("{0}\n" .format(res))

    # Plot it!
    fig = pyplot.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.array([i[0] for i in inputs])
    y = np.array([i[1] for i in inputs])
    ax.scatter(x, y, targets, c='r', marker='o')
    ax.scatter(x, y, predicted, c='b', marker='s')
#    X,Y = np.meshgrid(sorted(x), sorted(y))
#    Z = np.array([dot_product([x,y], weights) for (x,y) in inputs])
#    ax.plot_surface(X, Y, Z)
    ax.set_xlabel('Predictor 1')
    ax.set_ylabel('Predictor 2')
    ax.set_zlabel('Output')
    pyplot.show()


def read_data(data_file):
    """
    Reads in whitespace delimited data points
    of the form:
    2.345 0.87
    3.141 6.77
    where the last column is the dependent variable
    and all columns before are indepndent variables.

    param str data_file: path to training data
    returns: list of training data instances.
    rtype: list(list(float))
    """
    data = open(data_file).readlines()
    data = [x.strip() for x in data]
    data = [x.split() for x in data]
    data = [[float(attribute) for attribute in instance]
            for instance in data]
    return data


def dot_product(vector1, vector2):
    """
    Computes the dot product.

    param list vector1, vector2: input vectors
    """
    result = sum([x*y for x, y in zip(vector1, vector2)])
    return result


def matrix_multiply(matrix1, matrix2):
    """
    Multiplies two input matrices.

    param list(list(float)) matrix1, matrix 2: input matrices
    """
    result = [[] for x in range(len(matrix1))]
    for i, row1 in enumerate(matrix1):
        for row2 in matrix2:
            result[i].append(dot_product(row1, row2))
    return result


def compute_residuals(data, targets, weights):
    """
    Squared error function.

    param list(list(float)) data: independent variable(s)
    param list targets: dependent variable
    param list weights: weight vector
    """
    assert type(weights) == list

    residuals = []
    for i, values in enumerate(data):
        target = targets[i]
        assert len(values) == len(weights)
        predicted = dot_product(values, weights)
        residual = target - predicted
        residuals.append(residual)
    return residuals


def compute_weights(data, targets):
    """
    Computes the wieght vector.

    param list(list(float)) data: independent variable(s)
    param list(float) targets: dependent variable
    """
    pseudo_inverse = np.linalg.pinv(data)
    weights = [dot_product(a, targets) for a in pseudo_inverse]
    return weights


if __name__ == '__main__':
    main()
