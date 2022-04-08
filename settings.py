from PyQt5 import uic
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLabel, QTextEdit, QPushButton 


class setting1(QDialog):

	count = 0
	def __init__(self):
		super(setting1, self).__init__()

		#load ui file
		uic.loadUi("settings1.ui", self)


		#performance
		self.password.clicked.connect(self.gotoSetting2)
		self.pushButton_3.clicked.connect(self.gotoSetting3)
		

		self.show()

	def gotoSetting2(self):
		widget.setCurrentIndex(widget.currentIndex()+1)

	def gotoSetting3(self):
		widget.setCurrentIndex(widget.currentIndex()+2)



class setting2(QDialog):
	def __init__(self):
		super(setting2, self).__init__()

		uic.loadUi("settings2.ui", self)

class setting3(QDialog):
	def __init__(self):
		super(setting3, self).__init__()

		uic.loadUi("settings3.ui", self)


#main
app = QApplication(sys.argv)

#intialize QStackWidget
# QStackedwidget is a stack of QDialogs
# we load different uis with it and each dialog is an index in the list
#increment by one we show UI # 2 and so forth
widget = QtWidgets.QStackedWidget()

window1 = setting1()
window2 = setting2()
window3 = setting3()

#add the objects created above^ to the stack of screens
widget.addWidget(window1)
widget.addWidget(window2)
widget.addWidget(window3)
widget.setFixedHeight(803)
widget.setFixedWidth(789)

#show the widget
widget.show()


try:
    sys.exit(app.exec_())
except:
    print("Exiting")

