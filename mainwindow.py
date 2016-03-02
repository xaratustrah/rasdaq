"""
A client/server code for Raspberry Pi ADC input

Xaratustrah
2016

"""

from PyQt5.QtWidgets import QMainWindow, QDialog, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt, QCoreApplication, QThread, QTimer
from mainwindow_ui import Ui_MainWindow
from aboutdialog_ui import Ui_AbooutDialog
from zmq_listener import ZMQListener
from ipaddress import ip_address
from version import __version__


class mainWindow(QMainWindow, Ui_MainWindow):
    """
    The main class for the GUI window
    """

    def __init__(self):
        """
        The constructor and initiator.
        :return:
        """
        # initial setup
        super(mainWindow, self).__init__()
        self.setupUi(self)
        self.thread = QThread()
        # self.zeromq_listener = None

        self.connected = False
        # self.zeromq_listener = None
        # text, ok = QInputDialog.getText(self, 'Settings', 'Enter the host address:', QLineEdit.Normal, '127.0.0.1')
        # if ok:
        #     host = str(text)
        # text, ok = QInputDialog.getText(self, 'Settings', 'Enter the port number:', QLineEdit.Normal, '1234')
        # if ok:
        #     port = int(text)

        # Connect signals
        self.connect_signals()

    def on_push_button_clicked(self):
        if self.pushButton.isChecked():

            try:
                host = str(ip_address(self.lineEdit_host.text()))
                port = self.lineEdit_port.text()
                if not port.isdigit():
                    raise ValueError

            except(ValueError):
                self.pushButton.setChecked(False)
                self.show_message('Please enter valid numeric IP address and port number.')
                return

            # self.zeromq_listener = None
            # del self.zeromq_listener
            self.zeromq_listener = ZMQListener(host, port)
            self.zeromq_listener.moveToThread(self.thread)
            self.zeromq_listener.message.connect(self.signal_received)
            self.zeromq_listener.err_msg.connect(self.show_message)

            self.thread.started.connect(self.zeromq_listener.loop)
            # QTimer.singleShot(0, self.thread.start# )
            self.thread.start()

            self.pushButton.setText('Stop')
            self.show_message('Connected to server: {}:{}'.format(host, port))
        else:
            self.zeromq_listener.running = False
            self.thread.terminate()
            self.pushButton.setText('Start')
            self.show_message('Disconnected.')

    def connect_signals(self):
        """
        Connects signals.
        :return:
        """

        # Action about and Action quit will be shown differently in OSX

        self.actionAbout.triggered.connect(self.show_about_dialog)
        self.actionQuit.triggered.connect(self.shutdown)
        self.pushButton.clicked.connect(self.on_push_button_clicked)

    def shutdown(self):
        self.zeromq_listener.running = False
        self.thread.terminate()
        self.thread.quit()
        self.thread.wait()
        QCoreApplication.instance().quit()

    def signal_received(self, message):
        # in case more digits are needed
        # self.lcdNumber.setDigitCount(8)
        if self.zeromq_listener.running:
            self.lcdNumber.display(float(message))
        else:
            self.lcdNumber.display(0)

    def closeEvent(self, event):
        self.zeromq_listener.running = False
        self.thread.terminate()
        self.thread.quit()
        self.thread.wait()

    def show_message(self, message):
        """
        Implementation of an abstract method:
        Show text in status bar
        :param message:
        :return:
        """
        self.statusbar.showMessage(message)

    def show_about_dialog(self):
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
