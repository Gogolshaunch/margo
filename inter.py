import json
import os
from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton
from assistant import Assistant

with open('data_file.json', "r") as file:
    configuration = json.load(file)


def increase():
    assistant.run()


def com():
    os.system('python make_com')


def com1():
    t2 = Thread(target=com)
    t2.start()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 550)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.micro = QtWidgets.QLabel(self.centralwidget)
        self.micro.setGeometry(QtCore.QRect(225, 40, 300, 300))
        self.micro.setText("")
        self.micro.setPixmap(QtGui.QPixmap("mir.png"))
        self.micro.setObjectName("micro")
        self.voice = QtWidgets.QLabel(self.centralwidget)
        self.voice.setGeometry(QtCore.QRect(115, 275, 470, 240))
        self.voice.setText("")
        self.voice.setPixmap(QtGui.QPixmap("1.png"))
        self.voice.setObjectName("voice")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        makeButton = QPushButton(self.centralwidget)
        makeButton.setGeometry(QtCore.QRect(220, 470, 260, 40))
        makeButton.setText(_translate("MainWindow", "+"))
        makeButton.clicked.connect(com1)


if __name__ == "__main__":
    import sys
    t1 = Thread(target=increase)
    t1.start()

    assistant = Assistant(configuration)
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
