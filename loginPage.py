from PyQt5 import uic
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLabel, QTextEdit, QPushButton, QLineEdit, QComboBox, \
    QMainWindow
import sqlite3
import dao
import new_main_window
import card_generator
import grab_clipboard as grabClip
#from user import User as user


class login(QDialog):
    def __init__(self, data_access_object, widget, MainWindow):
        super(login, self).__init__()

        #load ui file
        uic.loadUi("welcomescreen.ui", self)
        self.dao = data_access_object
        self.flag = False
        self.widget = widget
        self.MainWindow = MainWindow
        #performance
        self.lineEdit.hide()
        self.label_4.hide()
        self.label_3.hide()
        self.pushButton.hide()
        if self.dao.get_user_status() != 0:
            self.flag = True
            self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.login.clicked.connect(self.gotoNextPage)

        self.show()

    #goes to the password pages
    def gotoNextPage(self):
        if self.flag:
            if self.dao.get_password_state() == True:
                self.lineEdit.show()
                self.label_4.show()
                self.pushButton.show()
                self.pushButton.clicked.connect(self.sendEmail)

                self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
                pwd = self.lineEdit.text()
                if self.dao.password_is_valid(pwd):
                    self.widget.close()
                    self.MainWindow.show()
                else:
                    self.label_3.setText("Incorrect password. Please try again.")
                    self.lineEdit.clear()
            else:
                self.widget.close()
                self.MainWindow.show()
        else:
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def sendEmail(self):
        self.dao.send_email()
        self.label_3.setText("A temporary password was sent to the email on file. Please check your email.")


class newUser(QDialog):

    def __init__(self, data_access_object, widget, MainWindow):
        super(newUser, self).__init__()

        #load ui file
        uic.loadUi("new_user.ui", self)

        #performance
        self.dao = data_access_object
        self.widget = widget
        self.enter.clicked.connect(self.gotoMainPage)
        self.MainWindow = MainWindow
        self.show()

    # goes to the password pages
    def gotoMainPage(self):
        email1 = self.lineEdit.text()
        email2 = self.lineEdit_2.text()
        if (email1 == email2):
            self.dao.create_user(email1)
            self.widget.close()
            self.MainWindow.show()

            # MainWindow = QMainWindow()
            # ui = new_main_window.UI()
            # ui.setupUi(MainWindow)
            # cardMaker = card_generator.CardRenderer(ui.gridLayout2, self.dao)
            # cardMaker.initializeUI(self.dao.getAllCards())
            # gc = grabClip.ClipboardManager(cardMaker, self.dao)
            # gc.manage_clip()
            # self.reject()
            # MainWindow.setVisible(1)
            # widget.setCurrentIndex(widget.currentIndex() + 1)

        else:
            self.label_2.setText("Emails do not match, please try again.")
            self.lineEdit.clear()
            self.lineEdit_2.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    #intialize QStackWidget
    # QStackedwidget is a stack of QDialogs
    # we load different uis with it and each dialog is an index in the list
    #increment by one we show UI # 2 and so forth
    widget = QtWidgets.QStackedWidget()
    data_access_object = dao.DataAccessor()
    window1 = login(data_access_object) #page 1
    window2 = newUser(data_access_object)

    #add the objects created above^ to the stack of screens
    widget.addWidget(window1)
    widget.addWidget(window2)
    widget.setFixedHeight(803)
    widget.setFixedWidth(789)

    #show the widget
    widget.show()


    sys.exit(app.exec_())
