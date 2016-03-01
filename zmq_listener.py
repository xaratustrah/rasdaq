"""
A client/server code for Raspberry Pi ADC input

Xaratustrah
2016

adapted from:

https://wiki.python.org/moin/PyQt/Writing%20a%20client%20for%20a%20zeromq%20service


"""
from PyQt5.QtCore import pyqtSignal, QObject
import zmq

# calibration constant
CALIBRATION = 3.3

# resolution of the ADC
ADC_RES = 12
N_STEPS = 2 ** ADC_RES


class ZMQListener(QObject):
    message = pyqtSignal(str)

    def __init__(self, host, port):
        QObject.__init__(self)

        self.host = host
        self.port = port
        context = zmq.Context()
        try:
            self.sock = context.socket(zmq.SUB)
            self.sock.connect("tcp://{}:{}".format(self.host, self.port))
            topic_filter = '10001'
            self.sock.setsockopt_string(zmq.SUBSCRIBE, topic_filter)
        except(ConnectionRefusedError):
            print('Server not running. Aborting...')

        except(EOFError, KeyboardInterrupt):
            print('\nUser input cancelled. Aborting...')

        self.running = True

    def loop(self):
        while self.running:
            string = self.sock.recv()
            topic, time, value = string.split()
            value = float(value) * CALIBRATION / N_STEPS
            value = int(value * 100) / 100
            self.message.emit(str(value))
