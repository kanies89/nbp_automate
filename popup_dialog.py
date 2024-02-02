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

    def setupUi(self, dialog, title, main_text, instructions_text, instructions_url, reminder_text, conditions_text,
                checkbox1_text, checkbox2_text, proceed_button_text, proceed_function):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("UI/logos/warning.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dialog.setWindowIcon(icon)
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

        # Set texts
        self.retranslateUi(dialog, title, main_text, instructions_text, reminder_text, conditions_text, checkbox1_text,
                            checkbox2_text, proceed_button_text)

        # Connect signals and slots
        self.commandLinkButton.clicked.connect(lambda: self.openInstructions(instructions_url))
        self.checkBox.stateChanged.connect(self.checkConditions)
        self.checkBox_2.stateChanged.connect(self.checkConditions)
        self.pushButton.clicked.connect(proceed_function)

        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog, title, main_text, instructions_text, reminder_text, conditions_text,
                      checkbox1_text, checkbox2_text, proceed_button_text):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("Reminder", title))
        self.label.setText(_translate("Dialog", main_text))
        self.label_2.setText(_translate("Dialog", instructions_text))
        self.commandLinkButton.setText(_translate("Dialog", "Instructables"))
        self.label_4.setText(_translate("Dialog", reminder_text))
        self.label_3.setText(_translate("Dialog", conditions_text))
        self.checkBox_2.setText(_translate("Dialog", checkbox1_text))
        self.checkBox.setText(_translate("Dialog", checkbox2_text))
        self.pushButton.setText(_translate("Dialog", proceed_button_text))

    def openInstructions(self, instructions_url):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(instructions_url))

    def checkConditions(self):
        if self.checkBox.isChecked() and self.checkBox_2.isChecked():
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)
