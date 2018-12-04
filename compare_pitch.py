# ! /usr/bin/env python

import sys
import math
from scipy import stats
from readpitch import read_pitch


def calculate_entropy(password_length):
    password_entropy = password_length * math.log(26, 2)
    pitch_entropy = 50 * math.log(14, 2)
    joint_entropy = password_entropy + pitch_entropy
    print("Joint entropy: %.2E" % joint_entropy)


def compare_pitch():
    file1, file2, tolerance = sys.argv[1], sys.argv[2], sys.argv[3]

    data1_raw, data1_curve = read_pitch(file1)
    data2_raw, data2_curve = read_pitch(file2)

    if len(data1_raw) < len(data2_raw):
        data2_raw = data2_raw[0:len(data1_raw)]
    else:
        data1_raw = data1_raw[0:len(data2_raw)]

    if len(data1_curve) < len(data2_curve):
        data2_curve = data2_curve[0:len(data1_curve)]
    else:
        data1_curve = data1_curve[0:len(data2_curve)]

    slope, intercept, r_value, p_value, std_err = stats.linregress(data1_raw,
                                                                   data2_raw)
    print("REGRESSION ANALYSIS FROM RAW DATA")
    print("SLOPE = %f" % slope)
    print("INTERCEPT = %f" % intercept)
    print("R-VALUE = %f" % r_value)
    print("P-VALUE = %f" % p_value)
    print("STD-ERROR = %f" % std_err)

    print("-----VERDICT-----")
    if float(p_value) >= float(tolerance):
        print(
            "p-value: %f is higher than tolerance: %s" % (p_value, tolerance))
    else:
        print("p-value: %f is lower than tolerance: %s" % (p_value, tolerance))

    slope, intercept, r_value, p_value, std_err = stats.linregress(data1_curve,
                                                                   data2_curve)
    print("REGRESSION ANALYSIS FROM CURVED APPROXIMATION FUNCTION")
    print("SLOPE = %f" % slope)
    print("INTERCEPT = %f" % intercept)
    print("R-VALUE = %f" % r_value)
    print("P-VALUE = %f" % p_value)
    print("STD-ERROR = %f" % std_err)

    print("-----VERDICT-----")
    if float(p_value) >= float(tolerance):
        print(
            "p-value: %f is higher than tolerance: %s" % (p_value, tolerance))
    else:
        print("p-value: %f is lower than tolerance: %s" % (p_value, tolerance))


def compare_pitch_function(password1, password2, file1, file2, tolerance):
    data1_raw, data1_curve = read_pitch(file1)
    data2_raw, data2_curve = read_pitch(file2)

    if len(data1_raw) < len(data2_raw):
        data2_raw = data2_raw[0:len(data1_raw)]
    else:
        data1_raw = data1_raw[0:len(data2_raw)]

    if len(data1_curve) < len(data2_curve):
        data2_curve = data2_curve[0:len(data1_curve)]
    else:
        data1_curve = data1_curve[0:len(data2_curve)]

    slope, intercept, r_value, p_value, std_err = stats.linregress(data1_raw,
                                                                   data2_raw)
    print("REGRESSION ANALYSIS FROM RAW DATA")
    print("SLOPE = %f" % slope)
    print("INTERCEPT = %f" % intercept)
    print("R-VALUE = %f" % r_value)
    print("P-VALUE = %f" % p_value)
    print("STD-ERROR = %f" % std_err)

    print("-----VERDICT-----")
    if float(p_value) >= float(tolerance):
        print(
            "p-value: %f is higher than tolerance: %s" % (p_value, tolerance))
    else:
        print("p-value: %f is lower than tolerance: %s" % (p_value, tolerance))

    slope, intercept, r_value, p_value, std_err = stats.linregress(data1_curve,
                                                                   data2_curve)
    print("REGRESSION ANALYSIS FROM CURVED APPROXIMATION FUNCTION")
    print("SLOPE = %f" % slope)
    print("INTERCEPT = %f" % intercept)
    print("R-VALUE = %f" % r_value)
    print("P-VALUE = %f" % p_value)
    print("STD-ERROR = %f" % std_err)

    print("-----VERDICT-----")
    if float(p_value) >= float(tolerance):
        print(
            "p-value: %f is higher than tolerance: %s" % (p_value, tolerance))
    else:
        print("p-value: %f is lower than tolerance: %s" % (p_value, tolerance))

    calculate_entropy(len(password1))
    if password1 != password2:
        calculate_entropy(len(password2))

