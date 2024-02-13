#!/usr/bin/env python
"""
A client/server code for Raspberry Pi ADC input

Xaratustrah
2016

"""

import datetime, time
import random
import argparse
import zmq
import os
from version import __version__

if os.name == 'posix' and os.uname().machine == 'armv7l':
    try:
        import RPi.GPIO as gpio
        import spidev
    except RuntimeError:
        print("""Error importing RPi.GPIO!  This is probably because you need superuser privileges.
                You can achieve this by using 'sudo' to run your script""")

# sleep time in seconds
SLEEP_TIME = 0.2

# calibration constant
CALIBRATION = 3.3

# resolution of the ADC
ADC_RES = 12
N_STEPS = 2 ** ADC_RES

# Assing GPIO pin numbers

# Output pins
LED = 31

# Input pins
RNG0 = 11
RNG1 = 13
RNG2 = 15
MODD = 7
RDDY = 8
PWWR = 10


def get_gpio_status_bits():
    gpio_status_bits = [gpio.input(PWWR), gpio.input(RDDY), gpio.input(MODD), gpio.input(RNG2), gpio.input(RNG1),
                        gpio.input(RNG0)]
    return ''.join([str(int(elem)) for elem in gpio_status_bits])


def gpio_setup():
    # turn off warnings
    gpio.setwarnings(False)

    # we need board numbering system
    gpio.setmode(gpio.BOARD)

    gpio.setup(LED, gpio.OUT)

    gpio.setup(PWWR, gpio.IN)
    gpio.setup(RDDY, gpio.IN)
    gpio.setup(MODD, gpio.IN)
    gpio.setup(RNG2, gpio.IN)
    gpio.setup(RNG1, gpio.IN)
    gpio.setup(RNG0, gpio.IN)


def start_server(host, port):
    # setup SPI
    spi = spidev.SpiDev()
    spi.open(0, 0)

    # setup GPIO
    gpio_setup()
    led_state = False
    context = zmq.Context()
    sock = context.socket(zmq.PUB)

    print("tcp://{}:{}".format(host, port))
    sock.bind("tcp://{}:{}".format(host, port))

    print('Server started. ctrl-c to abort.\n')
    try:
        while True:
            topic = '10001'  # just a number for identification
            # check status bits
            stat_bits = get_gpio_status_bits()
            # read SPI device 0,0 channel 0 single ended
            resp = spi.xfer([6, 0, 0])
            # check time
            current_time = datetime.datetime.now().strftime('%Y-%m-%d@%H:%M:%S.%f')

            value = (resp[1] << 8) + resp[2]
            messagedata = current_time + ' ' + stat_bits + ' ' + str(value)
            sock.send_string("{} {}".format(topic, messagedata))
            print("{} {}".format(topic, messagedata))

            led_state = not led_state
            gpio.output(LED, led_state)

            time.sleep(SLEEP_TIME)

    except(EOFError, KeyboardInterrupt):
        print('\nUser input cancelled. Aborting...')
        gpio.cleanup()
        spi.close()


def start_client(host, port):
    context = zmq.Context()
    print('Client started. ctrl-c to abort.\n')
    try:
        sock = context.socket(zmq.SUB)
        sock.connect("tcp://{}:{}".format(host, port))
        topic_filter = '10001'
        sock.setsockopt_string(zmq.SUBSCRIBE, topic_filter)

        for update_nbr in range(5):
            string = sock.recv().decode("utf-8")
            topic, time, stat_bits, value = string.split()
            # value = float(value) * CALIBRATION / N_STEPS
            print(time, stat_bits, value)

    except(ConnectionRefusedError):
        print('Server not running. Aborting...')

    except(EOFError, KeyboardInterrupt):
        print('\nUser input cancelled. Aborting...')


def main():
    parser = argparse.ArgumentParser(prog='rasdaq')
    parser.add_argument('--host', nargs=1, type=str, help='Host address', default='127.0.0.1')
    parser.add_argument('--port', nargs=1, type=int, help='Port number', default=1234)
    parser.add_argument('--version', action='version', version=__version__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--client', action='store_true', help='Start client')
    group.add_argument('--server', action='store_true', help='Start server')
    parser.set_defaults(server=False)
    parser.set_defaults(client=False)

    args = parser.parse_args()
    # check the first switches

    if isinstance(args.host, list):
        host = args.host[0]
    else:
        host = args.host

    if isinstance(args.port, list):
        port = args.port[0]
    else:
        port = args.port

    if args.server:

        start_server(host, port)

    elif args.host:
        start_client(host, port)

    else:
        parser.print_help()


# ----------------------------

if __name__ == '__main__':
    main()
