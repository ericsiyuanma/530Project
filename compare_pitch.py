# ! /usr/bin/env python

import sys
import math
from scipy import stats
from readpitch import read_pitch


def compare_pitch():
    file1, file2, tolerance = sys.argv[1], sys.argv[2], sys.argv[3]
    print(file1, file2)
    data1, data2 = read_pitch(file1), read_pitch(file2)

    slope, intercept, r_value, p_value, std_err = stats.linregress(data1, data2)
    print("REGRESSION ANALYSIS")
    print("SLOPE = %f" % slope)
    print("INTERCEPT = %f" % intercept)
    print("R-VALUE = %f" % r_value)
    print("P-VALUE = %f" % p_value)
    print("STD-ERROR = %f" % std_err)

    print("-----VERDICT-----")
    if float(p_value) >= float(tolerance):
        print("p-value: %f is higher than tolerance: %s" % (p_value, tolerance))
    else:
        print("p-value: %f is lower than tolerance: %s" % (p_value, tolerance))

    password_length = 5
    password_prob = 1/(26**password_length)
    pitch_prob = 0.05
    joint_prob = password_prob * pitch_prob
    joint_entropy = joint_prob * -math.log2(joint_prob)
    print("Joint entropy: %.2E" % joint_entropy)



def compare_pitch_function(file1, file2, tolerance):
    print(file1, file2)
    data1, data2 = read_pitch(file1), read_pitch(file2)
    print(len(data1),len(data2))

    slope, intercept, r_value, p_value, std_err = stats.linregress(data1, data2)
    print("REGRESSION ANALYSIS")
    print("SLOPE = %f" % slope)
    print("INTERCEPT = %f" % intercept)
    print("R-VALUE = %f" % r_value)
    print("P-VALUE = %f" % p_value)
    print("STD-ERROR = %f" % std_err)

    print("-----VERDICT-----")
    if float(p_value) >= float(tolerance):
        print("p-value: %f is higher than tolerance: %s" % (p_value, tolerance))
    else:
        print("p-value: %f is lower than tolerance: %s" % (p_value, tolerance))
