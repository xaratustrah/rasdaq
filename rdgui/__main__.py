#!/usr/bin/env python
"""
A data logger for Raspberry PI with ADC input

xaratustrah
2016
2024 update 

"""

import sys
from PyQt5.QtWidgets import QApplication
from rdgui.mainwindow import mainWindow

def main():
    """
    Start the application
    :return:
    """
    app = QApplication(sys.argv)
    form = mainWindow()
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
