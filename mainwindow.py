"""
A client/server code for Raspberry Pi ADC input

Xaratustrah
2016

"""

from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5.QtCore import Qt, QCoreApplication
from mainwindow_ui import Ui_MainWindow
from aboutdialog_ui import Ui_AbooutDialog
import os, zmq
from version import __version__

# calibration constant
CALIBRATION = 3.3

# resolution of the ADC
ADC_RES = 12
N_STEPS = 2 ** ADC_RES


class mainWindow(QMainWindow, Ui_MainWindow):
    """
    The main class for the GUI window
    """

    def __init__(self, host, port):
        """
        The constructor and initiator.
        :return:
        """
        # initial setup
        super(mainWindow, self).__init__()
        self.setupUi(self)

        self.host = host
        self.port = port

        # UI related stuff
        self.connect_signals()

        self.show_message('Moin!')

    def connect_signals(self):
        """
        Connects signals.
        :return:
        """

        # Action about and Action quit will be shown differently in OSX

        self.actionAbout.triggered.connect(self.showAboutDialog)
        self.actionQuit.triggered.connect(QCoreApplication.instance().quit)
        # self.actionLoad_Freqlist.triggered.connect(self.save_file_dialog)

    def showAboutDialog(self):
        """
        Show about dialog
        :return:
        """
        about_dialog = QDialog()
        about_dialog.ui = Ui_AbooutDialog()
        about_dialog.ui.setupUi(about_dialog)
        about_dialog.ui.labelVersion.setText('Version: {}'.format(__version__))
        about_dialog.exec_()
        about_dialog.show()

    def show_message(self, message):
        """
        Implementation of an abstract method:
        Show text in status bar
        :param message:
        :return:
        """
        self.statusbar.showMessage(message)

    def start_client(self):
        context = zmq.Context()
        self.show_message('Client started. ctrl-c to abort.\n')
        try:
            sock = context.socket(zmq.SUB)
            sock.connect("tcp://{}:{}".format(self.host, self.port))
            topic_filter = '10001'
            sock.setsockopt_string(zmq.SUBSCRIBE, topic_filter)

            for update_nbr in range(5):
                string = sock.recv().decode("utf-8")
                topic, time, value = string.split()
                value = float(value) * CALIBRATION / N_STEPS
                self.show_message(time, value)

        except(ConnectionRefusedError):
            self.show_message('Server not running. Aborting...')

        except(EOFError, KeyboardInterrupt):
            self.show_message('\nUser input cancelled. Aborting...')
