#!/usr/bin/env python
"""
A client/server code for Raspberry Pi ADC input

Xaratustrah
2016

"""

import sys

# Calibration constants

CAL_SLOPE = 0.9801675611142459
CAL_ITCPT = -0.012535071714850021

# ADC Voltage
RAIL_VOLTAGE = 3.3
ADC_QUANTIZATION = 2 ** 12  # for 12 bit ADC

# calibration range in mA
RANGE_DIC_mA = {0: '1000', 1: '300', 2: '100', 3: '30', 4: '10', 5: '3', 6: '1', 7: '0.3'}


def plot_calibration_curve(filename):
    import numpy as np
    import numpy.ma as ma
    from scipy import stats
    import matplotlib.pyplot as plt
    
    dat = np.genfromtxt(filename)
    currents = np.array([0.1, 1.0, 2.0, 3.0])
    values = np.array([])
    for i in currents:
        mask = [a != i for a in dat[:, 0]]
        mx = ma.masked_array(dat[:, 1], mask)
        values = np.append(values, int(mx.mean()) * RAIL_VOLTAGE / ADC_QUANTIZATION)

    slope, intercept, r_value, p_value, std_err = stats.linregress(currents, values)

    line = currents * slope + intercept

    print('Write the following values back into this source code for use in other modules.')
    print('Slope: {}'.format(slope))
    print('Intercept: {}'.format(intercept))

    plt.plot(currents, line, 'r-')
    plt.errorbar(currents, values, yerr=std_err, fmt='.', color='blue')
    plt.xlabel('Calibration current [mA]')
    plt.ylabel('Measured current [mA]')
    plt.title('Relation between reference and measured currents')
    plt.grid(1)
    plt.show()


def get_calibrated_value(adc_int_value):
    value = adc_int_value * RAIL_VOLTAGE / ADC_QUANTIZATION
    return (value - CAL_ITCPT) / CAL_SLOPE


def main():
    plot_calibration_curve(sys.argv[1])


# ----------------------------

if __name__ == '__main__':
    main()
