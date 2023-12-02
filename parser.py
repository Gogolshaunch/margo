from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from pytube import YouTube


class Ui_MainWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.resize(422, 255)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 40, 201, 111))
        self.label.setText("")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.takeinputs()

    def takeinputs(self):
        name, done1 = QtWidgets.QInputDialog.getText(
            self, 'Input Dialog', "Введите ссылку на видео с YouTube, которое вы хотите загрузить: ")

        if done1:
            yt = YouTube(name)
            ys = yt.streams.get_highest_resolution()
            ys.download('C://Users//HP//Desktop')
            self.label.setText('Готово!')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
