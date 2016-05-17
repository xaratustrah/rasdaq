#!/usr/bin/python

import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 1)

while True:
    antwort = spi.xfer([1, 128, 0])
if 0 <= antwort[1] <= 3:
    wert = ((antwort[1] * 256) + antwort[2]) * 0.00322
print("{}".format(wert))
time.sleep(0.5)
