from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QLineEdit, QStackedWidget
from PyQt5 import uic
import sys
class UI(QMainWindow):
     def __init__(self):
         super(UI, self).__init__()

         #load the UI
         uic.loadUi("main.ui", self)

        #define your widgets
        # self.label = self.findChild(QLabel, "label_9")
        # self.textedit = self.findChild(QLineEdit, "lineEdit")
        # self.button = self.findChild(QPushButton, "search_button")


         #show the app
         self.show()

#initialize the app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()