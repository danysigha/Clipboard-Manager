from PyQt5 import uic
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLabel, QTextEdit, QPushButton, QLineEdit, QComboBox
import sqlite3
from mini_dao2 import dao as dao
#from user import User as user


class mainSetting(QDialog):

	def __init__(self):
		super(mainSetting, self).__init__()

		#load ui file
		uic.loadUi("settings1.ui", self)


		#performance
		self.password.clicked.connect(self.gotoPasswordPage)
		self.pushButton_3.clicked.connect(self.gotoShelftime)
		self.pushButton_2.clicked.connect(self.goBack)
		self.show()

	#goes to the password pages
	def gotoPasswordPage(self):
		
		if dao.get_password_exists():
			widget.setCurrentIndex(widget.currentIndex()+3)
		else:
			widget.setCurrentIndex(widget.currentIndex()+1)

	
	def gotoShelftime(self):
		widget.setCurrentIndex(widget.currentIndex()+2)

	def goBack(self):
		widget.setCurrentIndex(widget.currentIndex()-1)


class setPassword(QDialog):

	def __init__(self):
		super(setPassword, self).__init__()

		uic.loadUi("settings2.ui", self)

		self.pwd1.setEchoMode(QtWidgets.QLineEdit.Password)
		self.pwd2.setEchoMode(QtWidgets.QLineEdit.Password)
		self.pushButton_2.clicked.connect(self.goBack)
		self.pushButton.clicked.connect(self.set_password)


	def goBack(self):
		widget.setCurrentIndex(widget.currentIndex()-1)

	def set_password(self):

		pwd1 = self.pwd1.text()
		pwd2 = self.pwd2.text()
		if(pwd1 == pwd2):
			dao.set_password(pwd1)
			self.label_4.setText("Password successfully saved")
		else:
			self.label_4.setText("The passwords do not match. Please try again.")
		self.pwd1.clear()
		self.pwd2.clear()


class shelftime(QDialog):
	def __init__(self):
		super(shelftime, self).__init__()

		uic.loadUi("settings3.ui", self)

		self.pushButton_3.clicked.connect(self.goBack)
		self.pushButton.clicked.connect(self.changeShelftime)

	def goBack(self):
		widget.setCurrentIndex(widget.currentIndex()-2)

	def changeShelftime(self):
		self.menu = self.findChild(QComboBox, "menu")
		if(self.menu.currentIndex() == 0):
			dao.changeShelftime(1)

		elif(self.menu.currentIndex() == 1):
			dao.changeShelftime(2)

		elif(self.menu.currentIndex()== 2):
			dao.changeShelftime(3)

		elif(self.menu.currentIndex() == 3):
			dao.changeShelftime(6)
		else:
			dao.changeShelftime(12)

		self.label_3.setText("Shelftime successfully updated.")






class currentPasswordPage(QDialog):
	def __init__(self):
		super(currentPasswordPage, self).__init__()

		uic.loadUi("settings5.ui", self)

		self.pushButton_2.clicked.connect(self.goBack)
		self.pushButton.clicked.connect(self.setPassword)
		self.oldpwd.setEchoMode(QtWidgets.QLineEdit.Password)
		self.pwd1.setEchoMode(QtWidgets.QLineEdit.Password)
		self.pwd2.setEchoMode(QtWidgets.QLineEdit.Password)

	def goBack(self):
		widget.setCurrentIndex(widget.currentIndex()-3)


	def setPassword(self):
		oldpwd = self.oldpwd.text()
		pwd1 = self.pwd1.text()
		pwd2 = self.pwd2.text()
		if(pwd1 == pwd2 and dao.change_password(oldpwd, pwd1)):
			self.label_4.setText("Password successfully saved")

		elif(pwd1 == pwd2 and not dao.change_password(oldpwd, pwd1)):
			self.label_4.setText("The current password entered is incorrect. Please try again.")

		elif(pwd1 != pwd2 and dao.change_password(oldpwd, pwd1)):
			self.label_4.setText("The new passwords do not match. Please try again.")

		else:
			self.label_4.setText("One or more input has been incorrect. Please try again.")

		self.oldpwd.clear()
		self.pwd1.clear()
		self.pwd2.clear()
		


#main
app = QApplication(sys.argv)

#intialize QStackWidget
# QStackedwidget is a stack of QDialogs
# we load different uis with it and each dialog is an index in the list
#increment by one we show UI # 2 and so forth
widget = QtWidgets.QStackedWidget()

window1 = mainSetting() #page 1
window2 = setPassword() #page 2
window3 = shelftime() #page 3
window4 = currentPasswordPage() #page 4
#add the objects created above^ to the stack of screens
widget.addWidget(window1)
widget.addWidget(window2)
widget.addWidget(window3)
widget.addWidget(window4)
widget.setFixedHeight(803)
widget.setFixedWidth(789)

#show the widget
widget.show()


try:
    sys.exit(app.exec_())
except:
    print("Exiting")

