#!/usr/bin/env python
"""
A data logger for Raspberry PI with ADC input

xaratustrah
2016
2024 update 

"""

import datetime, time
import random
import argparse
import zmq
import os, sys
from loguru import logger
import toml

from .version import __version__

if os.name == "posix" and os.uname().machine == "armv7l":
    try:
        import RPi.GPIO as gpio
        import spidev
    except RuntimeError:
        print("""Error importing Raspberry Pi libraries!""")

# Raspberry PI pin assignment

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

def read_adc_channel(spi, channel):
    msg_up, msg_dn = (
        0x06, 0x00 
        if channel == 0
        else 0x06, 0x40
        if channel == 1
        else 0x06, 0x80
        if channel == 2
        else 0x06, 0xC0
    )

    resp = spi.xfer([msg_up, msg_dn, 0x00])
    value = (resp[1] << 8) + resp[2]
    value = int(value)

    # clip value
    if value <= 0:
        value = 0
    elif value > 4095:
        value = 4095

    return value

def read_all_adc_channels(spi, config_dic):
    num_average = config_dic['num_average']
    
    pot0, pot1, pot2, pot3 = 0, 0, 0, 0
    # do many measurements and average
    for i in range(num_average):
        pot0 += read_adc_channel(spi, 0)
        pot1 += read_adc_channel(spi, 1)
        pot2 += read_adc_channel(spi, 2)
        pot3 += read_adc_channel(spi, 3)
    return [
        int(pot0 / num_average),
        int(pot1 / num_average),
        int(pot2 / num_average),
        int(pot3 / num_average),
    ]

def start_server(host, port, config_dic):
    
    refresh_period = config_dic['refresh_period']
    
    # setup SPI
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 5000


    # setup GPIO
    gpio_setup()
    led_state = False
    context = zmq.Context()
    sock = context.socket(zmq.PUB)

    logger.info("tcp://{}:{}".format(host, port))
    sock.bind("tcp://{}:{}".format(host, port))

    logger.success('Server started. ctrl-c to abort.\n')
    try:
        while True:
            topic = '10001'  # just a number for identification
            # check status bits
            stat_bits = get_gpio_status_bits()

            value_list = read_all_adc_channels(spi, config_dic)
            
            # check time
            current_time = datetime.datetime.now().strftime('%Y-%m-%d@%H:%M:%S.%f')
            messagedata = current_time + ' ' + stat_bits + ' ' + ','.join(map(str, value_list))
            
            sock.send_string("{} {}".format(topic, messagedata))
            logger.info("{} {}".format(topic, messagedata))

            led_state = not led_state
            gpio.output(LED, led_state)

            time.sleep(refresh_period)

    except(EOFError, KeyboardInterrupt):
        logger.success('\nUser input cancelled. Aborting...')
        gpio.cleanup()
        spi.close()


def start_client(host, port, config_dic):
    
    adc_resolution, reference_voltage = config_dic['adc_resolution'], config_dic['reference_voltage']
    
    context = zmq.Context()
    logger.info('Client started. ctrl-c to abort.\n')
    try:
        sock = context.socket(zmq.SUB)
        sock.connect("tcp://{}:{}".format(host, port))
        topic_filter = '10001'
        sock.setsockopt_string(zmq.SUBSCRIBE, topic_filter)

        while True:
            msg_string = sock.recv().decode("utf-8")
            topic, time, stat_bits, value = msg_string.split(' ')
            # n_steps = 2 ** adc_resolution
            # value = float(value) * reference_voltage / n_steps
            logger.info(msg_string)

    except(ConnectionRefusedError):
        logger.error('Server not running. Aborting...')

    except(EOFError, KeyboardInterrupt):
        logger.success('\nUser input cancelled. Aborting...')


def main():
    parser = argparse.ArgumentParser(prog='rasdaq')
    parser.add_argument('--host', nargs=1, type=str, help='Host address', default='127.0.0.1')
    parser.add_argument('--port', nargs=1, type=int, help='Port number', default=1234)
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument(
        "--config",
        nargs=1,
        type=str,
        default=None,
        help="Path and name of the config TOML file.",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--client', action='store_true', help='Start client')
    group.add_argument('--server', action='store_true', help='Start server')

    parser.set_defaults(server=False)
    parser.set_defaults(client=False)

    logger.remove(0)
    logger.add(sys.stdout, level="INFO")

    args = parser.parse_args()

    if isinstance(args.host, list):
        host = args.host[0]
    else:
        host = args.host

    if isinstance(args.port, list):
        port = args.port[0]
    else:
        port = args.port

    config_dic = None
    
    if args.config:
        try:
            # load config file
            with open(args.config[0], "r") as f:
                config_dic = toml.load(f)

            for key in ["reference_voltage", "refresh_period", "adc_resolution", "num_average"]:
                assert key in config_dic.keys()

        except:
            logger.error("Config file does not have required format.")
            exit()

    else:
        logger.error("Please provide a config file.")
        exit()


    if args.server:

        start_server(host, port, config_dic)

    elif args.host:
        start_client(host, port, config_dic)

    else:
        parser.print_help()


# ----------------------------

if __name__ == '__main__':
    main()
