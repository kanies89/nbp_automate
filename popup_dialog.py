# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pop_up.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def __init__(self):
        self.pushButton = None
        self.checkBox = None
        self.checkBox_2 = None
        self.label_3 = None
        self.line = None
        self.label_4 = None
        self.commandLinkButton = None
        self.label_2 = None
        self.label = None
        self.verticalLayout = None
        self.horizontalLayout = None
        self.horizontalLayoutWidget = None

    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(474, 270)
        self.horizontalLayoutWidget = QtWidgets.QWidget(dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 434, 231))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.commandLinkButton = QtWidgets.QCommandLinkButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.commandLinkButton.setFont(font)
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.verticalLayout.addWidget(self.commandLinkButton)
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.line = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.checkBox_2 = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout.addWidget(self.checkBox_2)
        self.checkBox = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setEnabled(False)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("Reminder", "Reminder"))
        self.label.setText(_translate("Dialog", "NBP AR1 / AR2 Automated report."))
        self.label_2.setText(_translate("Dialog", "Before proceeding further please get aquainted with instruction. Link below."))
        self.commandLinkButton.setText(_translate("Dialog", "Instructables"))
        self.label_4.setText(_translate("Dialog", "Please remember that this only generates last quarter report."))
        self.label_3.setText(_translate("Dialog", "Please confirm that:"))
        self.checkBox_2.setText(_translate("Dialog", "Mastercard fraud transactions \"YYYY_Q Mastercard.xlsx\" external file is provided."))
        self.checkBox.setText(_translate("Dialog", "Microsoft ODBC driver is installed at your operating system."))
        self.pushButton.setText(_translate("Dialog", "Proceed"))
