"""
A client/server code for Raspberry Pi ADC input

Xaratustrah
2016

adapted from:

https://wiki.python.org/moin/PyQt/Writing%20a%20client%20for%20a%20zeromq%20service


"""
from PyQt5.QtCore import pyqtSignal, QThread
import zmq

# calibration constant
CALIBRATION = 3.3

# resolution of the ADC
ADC_RES = 12
N_STEPS = 2 ** ADC_RES


class ZMQListener(QThread):
    message = pyqtSignal(str)
    err_msg = pyqtSignal(str)

    def __init__(self, host, port):
        QThread.__init__(self)

        self.host = host
        self.port = port
        self.running = True

        context = zmq.Context()

        try:
            self.sock = context.socket(zmq.SUB)
            self.sock.connect("tcp://{}:{}".format(self.host, self.port))
            topic_filter = '10001'
            self.sock.setsockopt_string(zmq.SUBSCRIBE, topic_filter)

        except(ConnectionRefusedError):
            self.err_msg.emit('Server not running. Aborting...')

        except(EOFError, KeyboardInterrupt):
            self.err_msg.emit('User input cancelled. Aborting...')

    def loop(self):
        while self.running:
            string = self.sock.recv()
            topic, time, value = string.split()
            value = float(value) * CALIBRATION / N_STEPS
            value = int(value * 100) / 100
            self.message.emit(str(value))
            # self.message.emit('{:.2e}'.format(value))

    def __del__(self):
        self.terminate()
        self.quit()
        self.wait()
