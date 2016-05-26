"""
A client/server code for Raspberry Pi ADC input

Xaratustrah
2016

"""

# Calibration constants
CAL_SLOPE = 1216.5958576739247
CAL_ITCPT = -15.558682952735126

# ADC Voltage
RAIL_VOLTAGE = 3.3
ADC_QUANTIZATION = 2 ** 12  # for 12 bit ADC
