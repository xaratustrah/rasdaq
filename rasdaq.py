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

if os.name == 'posix' and os.uname().machine == 'armv7l':
    try:
        import RPi.GPIO as gpio
    except RuntimeError:
        print("""Error importing RPi.GPIO!  This is probably because you need superuser privileges.
                You can achieve this by using 'sudo' to run your script""")

__version_info__ = (0, 1, 0)
__version__ = '.'.join('%d' % d for d in __version_info__)

# sleep time in seconds
SLEEP_TIME = 0.2

# calibratio constant
CALIBRATION = 3.3

# resolution of the ADC
ADC_RES = 12
N_STEPS = 2 ** ADC_RES

# assing pin numbers

LED = 31
SCLK = 23
MISO = 21
MOSI = 19
CS = 29


# SCI Funktion
def get_adc_data(adCh, CLKPin, DINPin, DOUTPin, CSPin):
    """
    Getting analog data: modifed from original:
    https://www.raspiprojekt.de/machen/basics/schaltungen/26-analoge-signale-mit-dem-mcp3008-verarbeiten.html

    -------

    """
    # Pegel definieren
    gpio.output(CSPin, gpio.HIGH)
    gpio.output(CSPin, gpio.LOW)
    gpio.output(CLKPin, gpio.LOW)

    cmd = adCh
    cmd |= 0b00011000  # Kommando zum Abruf der Analogwerte des Datenkanals adCh

    # Bitfolge senden
    for i in range(5):
        if (cmd & 0x10):  # 4. Bit prüfen und mit 0 anfangen
            gpio.output(DINPin, gpio.HIGH)
        else:
            gpio.output(DINPin, gpio.LOW)
        # Clocksignal negative Flanke erzeugen
        gpio.output(CLKPin, gpio.HIGH)
        gpio.output(CLKPin, gpio.LOW)
        cmd <<= 1  # Bitfolge eine Position nach links verschieben

    # Datenabruf
    adchvalue = 0  # Wert auf 0 zurücksetzen
    for i in range(ADC_RES + 1):
        gpio.output(CLKPin, gpio.HIGH)
        gpio.output(CLKPin, gpio.LOW)
        adchvalue <<= 1  # 1 Postition nach links schieben
        if (gpio.input(DOUTPin)):
            adchvalue |= 0x01
    return adchvalue


def gpio_setup():
    # turn off warnings
    gpio.setwarnings(False)

    # we need board numbering system
    gpio.setmode(gpio.BOARD)

    gpio.setup(LED, gpio.OUT)
    gpio.setup(SCLK, gpio.OUT)
    gpio.setup(CS, gpio.OUT)
    gpio.setup(MOSI, gpio.OUT)
    gpio.setup(MISO, gpio.IN)


def start_server(host, port):
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
            # value = round(random.random() * 10, 3)
            value = get_adc_data(0, SCLK, MOSI, MISO, CS)
            current_time = datetime.datetime.now().strftime('%Y-%m-%d@%H:%M:%S.%f')
            messagedata = current_time + ' ' + str(value)
            sock.send_string("{} {}".format(topic, messagedata))
            print("{} {}".format(topic, messagedata))

            led_state = not led_state
            gpio.output(LED, led_state)

            time.sleep(SLEEP_TIME)

    except(EOFError, KeyboardInterrupt):
        print('\nUser input cancelled. Aborting...')
        gpio.cleanup()


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
            topic, time, value = string.split()
            value = float(value) * CALIBRATION / N_STEPS
            print(time, value)

    except(ConnectionRefusedError):
        print('Server not running. Aborting...')

    except(EOFError, KeyboardInterrupt):
        print('\nUser input cancelled. Aborting...')


def main():
    parser = argparse.ArgumentParser(prog='rasdaq')
    parser.add_argument('--host', nargs=1, type=str, help='Host address', default='localhost')
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
