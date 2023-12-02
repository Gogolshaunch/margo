from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton

import assistant


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(880, 315)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(15, 20, 840, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(15, 130, 840, 30))
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(15, 175, 840, 30))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(15, 220, 840, 30))
        self.lineEdit_3.setObjectName("lineEdit_3")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Выберите тип функции"))
        comboBox = QtWidgets.QComboBox(self.centralwidget)
        comboBox.setGeometry(QtCore.QRect(15, 50, 840, 25))
        comboBox.setCurrentText("")
        comboBox.setObjectName("comboBox")
        comboBox.addItem("")
        comboBox.addItem("")
        comboBox.addItem("")

        comboBox.setCurrentText(_translate("MainWindow", "открытие файла"))
        comboBox.setItemText(0, _translate("MainWindow", "открытие файла"))
        comboBox.setItemText(1, _translate("MainWindow", "ответ на вопрос"))
        comboBox.setItemText(2, _translate("MainWindow", "открытие сайта"))
        comboBox.activated[str].connect(self.takeinputs)
        self.lineEdit.setText(_translate("MainWindow", ""))
        self.lineEdit_2.setText(_translate("MainWindow", ""))
        self.lineEdit_3.setText(_translate("MainWindow", ""))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(330, 260, 260, 40))
        self.pushButton.setText(_translate("MainWindow", "Дальше"))
        self.pushButton.setEnabled(False)

    def takeinputs(self, val):
        self.lineEdit.setText('Введите название функции')
        self.lineEdit_2.setText('Введите фразы вызова функции через запятую')
        if val == 'открытие файла':
            self.lineEdit_3.setText('Введите полный путь до файла')
        elif val == 'открытие сайта':
            self.lineEdit_3.setText('Введите ссылку сайта')
        elif val == 'ответ на вопрос':
            self.lineEdit_3.setText('Введите список ответов для данной функции через запятую')
        if self.lineEdit.text != '' and self.lineEdit_2.text != '' and self.lineEdit_3.text != '' and self.lineEdit.text != 'Введите название функции' and self.lineEdit_2.text != 'Введите фразы вызова функции через запятую' and self.lineEdit_3.text != 'Введите ссылку сайта' and self.lineEdit_3.text != 'Введите полный путь до файла' and self.lineEdit_3.text != 'Введите список ответов для данной функции через запятую':
            self.pushButton.setEnabled(True)
            self.pushButton.clicked.connect(assistant.assistant.make_com(self.lineEdit.text, self.lineEdit_2.text, self.lineEdit_3.text, val))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())