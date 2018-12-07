import math
import numpy

#c - covariance matrix
def calculate_entropy(c):
    print("Before")
    for elem in c:
        print(elem)
    matrix = [x * 2 * math.pi * math.e for x in c]
    print("After")
    for elem in matrix:
        print(elem)
    entropy = (1 / 2) * math.log2(numpy.linalg.det(matrix))
    return entropy

def exp_entropy(mixtures):
    sum = 0
    for mixture in mixtures:
        sum = sum + mixture.weight

    exp_entropy = 0
    for mixture in mixtures:
        exp_entropy = exp_entropy + (mixture.weight/sum) * calculate_entropy(mixture.covar)

    print("Expected value of entropy: %.2f" % exp_entropy)