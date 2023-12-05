from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton
import configuration
from assistant import Assistant


class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 550)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.micro = QtWidgets.QLabel(self.centralwidget)
        self.micro.setGeometry(QtCore.QRect(225, 40, 300, 300))
        self.micro.setText("")
        self.micro.setPixmap(QtGui.QPixmap("image/mir.png"))
        self.micro.setObjectName("micro.py")
        self.voice = QtWidgets.QLabel(self.centralwidget)
        self.voice.setGeometry(QtCore.QRect(115, 275, 470, 240))
        self.voice.setText("")
        self.voice.setPixmap(QtGui.QPixmap("image/1.png"))
        self.voice.setObjectName("voice")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        pushButton = QPushButton(self.centralwidget)
        pushButton.setGeometry(QtCore.QRect(230, 470, 130, 40))
        pushButton.setText(_translate("MainWindow", "🎧"))
        pushButton.clicked.connect(assistant.run)

        makeButton = QPushButton(self.centralwidget)
        makeButton.setGeometry(QtCore.QRect(330, 470, 130, 40))
        makeButton.setText(_translate("MainWindow", "+"))
        makeButton.clicked.connect(assistant.make_com)


if __name__ == "__main__":
    import sys

    assistant = Assistant(configuration.commands)
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
