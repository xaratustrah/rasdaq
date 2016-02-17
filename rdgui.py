#!/usr/bin/env python
"""
A client/server code for Raspberry Pi ADC input

Xaratustrah
2016

"""

import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import mainWindow


def main():
    """
    Start the application
    :return:
    """
    app = QApplication(sys.argv)
    form = mainWindow("127.0.0.1", 1234)
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
