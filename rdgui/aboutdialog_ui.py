# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rsrc/aboutdialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AbooutDialog(object):
    def setupUi(self, AbooutDialog):
        AbooutDialog.setObjectName("AbooutDialog")
        AbooutDialog.resize(472, 505)
        self.verticalLayout = QtWidgets.QVBoxLayout(AbooutDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(AbooutDialog)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/icons/icon_128x128.png"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.labelTitle = QtWidgets.QLabel(AbooutDialog)
        self.labelTitle.setObjectName("labelTitle")
        self.verticalLayout.addWidget(self.labelTitle)
        self.labelVersion = QtWidgets.QLabel(AbooutDialog)
        self.labelVersion.setAlignment(QtCore.Qt.AlignCenter)
        self.labelVersion.setObjectName("labelVersion")
        self.verticalLayout.addWidget(self.labelVersion)
        self.labelDescription = QtWidgets.QLabel(AbooutDialog)
        self.labelDescription.setObjectName("labelDescription")
        self.verticalLayout.addWidget(self.labelDescription)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_ok = QtWidgets.QPushButton(AbooutDialog)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout.addWidget(self.pushButton_ok)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(AbooutDialog)
        self.pushButton_ok.pressed.connect(AbooutDialog.close)
        QtCore.QMetaObject.connectSlotsByName(AbooutDialog)

    def retranslateUi(self, AbooutDialog):
        _translate = QtCore.QCoreApplication.translate
        AbooutDialog.setWindowTitle(_translate("AbooutDialog", "Dialog"))
        self.labelTitle.setText(_translate("AbooutDialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; font-weight:600; text-decoration: underline; color:#ff0000;\">rasdaq</span></p><p align=\"center\"><span style=\" font-family:\'Menlo\'; font-size:24pt; font-weight:600; color:#000000;\">(</span><span style=\" font-family:\'Menlo\'; font-size:24pt; font-weight:600; color:#ff0000;\">RAS</span><span style=\" font-family:\'Menlo\'; font-size:24pt; font-weight:600; color:#000000;\">pberry pi </span><span style=\" font-family:\'Menlo\'; font-size:24pt; font-weight:600; color:#ff0000;\">D</span><span style=\" font-family:\'Menlo\'; font-size:24pt; font-weight:600; color:#000000;\">ata </span><span style=\" font-family:\'Menlo\'; font-size:24pt; font-weight:600; color:#ff0000;\">A</span><span style=\" font-family:\'Menlo\'; font-size:24pt; font-weight:600; color:#000000;\">c</span><span style=\" font-family:\'Menlo\'; font-size:24pt; font-weight:600; color:#ff0000;\">Q</span><span style=\" font-family:\'Menlo\'; font-size:24pt; font-weight:600; color:#000000;\">uisition)</span></p></body></html>"))
        self.labelVersion.setText(_translate("AbooutDialog", "TextLabel"))
        self.labelDescription.setText(_translate("AbooutDialog", "<html><head/><body><p align=\"center\">A visualizer for sorage ring\'s DCCT current.</p><p align=\"center\"><br/></p><p align=\"center\"><br/></p><p align=\"center\">Copyright (c) Shahab Sanjari 2016.</p><p align=\"center\">License: GPLv3</p><p align=\"center\"><br/></p></body></html>"))
        self.pushButton_ok.setText(_translate("AbooutDialog", "OK"))

from . import gui_rc
