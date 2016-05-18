#!/usr/bin/python

import spidev
import time
import RPi.GPIO as gpio

spi = spidev.SpiDev()
spi.open(0, 0)
gpio.setmode(gpio.BOARD)
LED = 31
INP = 33

gpio.setup(LED, gpio.OUT)
gpio.setup(INP, gpio.IN)

led_state = False

while True:
    resp = spi.xfer([6, 0, 0])
    adcv = (resp[1] << 8) + resp[2]
    print(adcv)
    if gpio.input(INP):
        led_state = not led_state
        gpio.output(LED, led_state)
    time.sleep(0.1)
