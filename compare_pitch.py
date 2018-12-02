#! /usr/bin/env python

import sys
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


compare_pitch()
