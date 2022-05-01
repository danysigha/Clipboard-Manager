import sys  # interaction with Python

from PyQt5.QtWidgets import *  # for classic application based on widgets
from PyQt5 import uic  # to read ui file
from PyQt5 import QtWidgets  # to create gui

class MyWin(QtWidgets.QMainWindow):  # create class witch inherit QMainWindow
    def __init__(self):  # constructor
        QtWidgets.QMainWindow.__init__(self)  # constructor of parent class
        uic.loadUi("gui.ui", self)  # load ui
        self.add_product.clicked.connect(self.add)
        self.remove_product.clicked.connect(self.remove)

    def add(self):
        h1 = QHBoxLayout()
        h1.addWidget(QLabel('Product'))
        h1.addWidget(QLabel('Weight'))
        h2 = QHBoxLayout()
        h2.addWidget(QLineEdit())
        h2.addWidget(QLineEdit())
        i = self.verticalLayout_2.count()
        self.verticalLayout_2.insertLayout(i - 2, h1)
        self.verticalLayout_2.insertLayout(i - 1, h2)

    def remove(self):
        i = self.verticalLayout_2.count()
        if i > 3:
            QWidget().setLayout(self.verticalLayout_2.takeAt(i - 3))
            QWidget().setLayout(self.verticalLayout_2.takeAt(i - 4))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = MyWin()

    ui.show()
    sys.exit(app.exec_())