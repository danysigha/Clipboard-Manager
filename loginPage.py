from PyQt5 import uic
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLabel, QTextEdit, QPushButton, QLineEdit, QComboBox
import sqlite3
from mini_dao2 import dao as dao
#from user import User as user


class login(QDialog):

	def __init__(self):
		super(login, self).__init__()

		#load ui file
		uic.loadUi("welcomescreen.ui", self)


		#performance
		self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
		self.login.clicked.connect(self.gotoMainPage)
		self.show()

	#goes to the password pages
	def gotoMainPage(self):
		pwd = self.lineEdit.text()
		if (dao.password_is_valid(pwd)):
			widget.setCurrentIndex(widget.currentIndex()+1)
		else:
			self.label_3.setText("Incorrect password. Please try again.")
			self.lineEdit.clear()

#main
app = QApplication(sys.argv)

#intialize QStackWidget
# QStackedwidget is a stack of QDialogs
# we load different uis with it and each dialog is an index in the list
#increment by one we show UI # 2 and so forth
widget = QtWidgets.QStackedWidget()

window1 = login() #page 1

#add the objects created above^ to the stack of screens
widget.addWidget(window1)
widget.setFixedHeight(803)
widget.setFixedWidth(789)

#show the widget
widget.show()


try:
    sys.exit(app.exec_())
except:
    print("Exiting")