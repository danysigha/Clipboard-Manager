from PyQt5 import uic
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLabel, QTextEdit, QPushButton, QLineEdit, QComboBox
import sqlite3
from mini_dao2 import dao as dao
#from user import User as user


class newUser(QDialog):

	def __init__(self):
		super(newUser, self).__init__()

		#load ui file
		uic.loadUi("new_user.ui", self)


		#performance
		self.enter.clicked.connect(self.gotoMainPage)
		self.show()

	#goes to the password pages
	def gotoMainPage(self):
		email1 = self.lineEdit.text()
		email2 = self.lineEdit_2.text()
		if (email1 == email2):
			dao.set_email(email1)
			widget.setCurrentIndex(widget.currentIndex()+1)
		else:
			self.label_3.setText("Emails do not match, please try again.")
			self.lineEdit.clear()
			self.lineEdit_2.clear()

#main
app = QApplication(sys.argv)

#intialize QStackWidget
# QStackedwidget is a stack of QDialogs
# we load different uis with it and each dialog is an index in the list
#increment by one we show UI # 2 and so forth
widget = QtWidgets.QStackedWidget()

window1 = newUser() #page 1

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