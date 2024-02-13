"""
A client/server code for Raspberry Pi ADC input

Xaratustrah
2016

adapted from:

https://wiki.python.org/moin/PyQt/Writing%20a%20client%20for%20a%20zeromq%20service


"""
from PyQt5.QtCore import pyqtSignal, QThread
import zmq


class ZMQListener(QThread):
    message = pyqtSignal(str)
    err_msg = pyqtSignal(str)

    def __init__(self, host, port, topic_filter):
        QThread.__init__(self)

        self.host = host
        self.port = port
        self.topic_filter = topic_filter
        self.running = True

        context = zmq.Context()

        try:
            self.sock = context.socket(zmq.SUB)
            self.sock.connect("tcp://{}:{}".format(self.host, self.port))
            self.sock.setsockopt_string(zmq.SUBSCRIBE, self.topic_filter)

        except(ConnectionRefusedError):
            self.err_msg.emit('Server not running. Aborting...')

        except(EOFError, KeyboardInterrupt):
            self.err_msg.emit('User input cancelled. Aborting...')

    def loop(self):
        while self.running:
            ba = self.sock.recv()
            self.message.emit(ba.decode("utf-8"))

    def __del__(self):
        self.terminate()
        self.quit()
        self.wait()
