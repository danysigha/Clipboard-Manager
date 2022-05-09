from PyQt5 import uic
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLabel, QTextEdit, QPushButton, QLineEdit, QComboBox, \
    QMainWindow
import sqlite3
#from mini_dao2 import dao as dao
import new_main_window
import sys
# import dao
import card_generator
import grab_clipboard as grabClip



# from user import User as user


class mainSetting(QDialog):

    def __init__(self, parent, data_access_object, widget):
        super(mainSetting, self).__init__()

        # load ui file
        uic.loadUi("settings1.ui", self)

        # performance
        self._parent = parent
        self.widget = widget
        self.dao = data_access_object
        self.password.clicked.connect(self.gotoPasswordPage)
        self.pushButton_3.clicked.connect(self.gotoShelftime)
        self.pushButton_2.clicked.connect(self.goBack)#
        self.reset.clicked.connect(self.gotoResetPage)

        self.show()

    # goes to the password pages
    def gotoPasswordPage(self):

        if self.dao.get_password_state():
            self.widget.setCurrentIndex(self.widget.currentIndex() + 3)
        else:
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def gotoShelftime(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 2)

    def gotoResetPage(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 4)

    def goBack(self):
        self.widget.close()
        self._parent.show()

        # app = QApplication(sys.argv)
        # MainWindow = QMainWindow()
        # ui = new_main_window.UI()
        # ui.setupUi(MainWindow)
        # dataAccessObject = dao.DataAccessor()
        # cardMaker = card_generator.CardRenderer(ui.gridLayout2, dataAccessObject)
        # cardMaker.initializeUI(dataAccessObject.getAllCards())
        # gc = grabClip.ClipboardManager(cardMaker, dataAccessObject)
        # gc.manage_clip()
        # MainWindow.show()
        # widget.setCurrentIndex(widget.currentIndex() - 1)
        # MainWindow.show()


class setPassword(QDialog):

    def __init__(self, data_access_object, widget):
        super(setPassword, self).__init__()

        uic.loadUi("settings2.ui", self)

        self.dao = data_access_object
        self.widget = widget
        self.pwd1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwd2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton_2.clicked.connect(self.goBack)
        self.pushButton.clicked.connect(self.set_password)

    def goBack(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() - 1)

    def set_password(self):

        pwd1 = self.pwd1.text()
        pwd2 = self.pwd2.text()
        if (pwd1 == pwd2):
            self.dao.set_password(pwd1)
            self.label_4.setText("Password successfully saved")
        else:
            self.label_4.setText("The passwords do not match. Please try again.")
        self.pwd1.clear()
        self.pwd2.clear()




class shelftime(QDialog):
    def __init__(self, data_access_object, widget):
        super(shelftime, self).__init__()

        uic.loadUi("settings3.ui", self)

        self.dao = data_access_object
        self.widget = widget
        self.pushButton_3.clicked.connect(self.goBack)
        self.pushButton.clicked.connect(self.changeShelftime)

    def goBack(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() - 2)

    def changeShelftime(self):
        self.menu = self.findChild(QComboBox, "menu")
        if (self.menu.currentIndex() == 0):
            self.dao.changeShelftime(1)

        elif (self.menu.currentIndex() == 1):
            self.dao.changeShelftime(2)

        elif (self.menu.currentIndex() == 2):
            self.dao.changeShelftime(3)

        elif (self.menu.currentIndex() == 3):
            self.dao.changeShelftime(6)
        else:
            self.dao.changeShelftime(12)

        self.label_3.setText("Shelftime successfully updated.")


class resetApplication(QDialog):
    def __init__(self, data_access_object, widget, parent):
        super(resetApplication, self).__init__()

        uic.loadUi("settings4.ui", self)

        self.dao = data_access_object
        self.widget = widget
        self.parent = parent
        self.pushButton_2.clicked.connect(self.goBack)
        self.pushButton.clicked.connect(self.resetDB)


    def goBack(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() - 4)

    def resetDB(self):
        self.dao.resetdb()
        self.widget.close()
        self.parent.close()

class currentPasswordPage(QDialog):
    def __init__(self, data_access_object, widget):
        super(currentPasswordPage, self).__init__()

        uic.loadUi("settings5.ui", self)
        self.dao = data_access_object
        self.widget = widget
        self.pushButton_2.clicked.connect(self.goBack)
        self.pushButton_3.clicked.connect(self.sendEmail)
        self.pushButton.clicked.connect(self.setPassword)
        self.pushButton_4.clicked.connect(self.turnOffPasswordPage)
        self.oldpwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwd1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwd2.setEchoMode(QtWidgets.QLineEdit.Password)

    def goBack(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() - 3)

    def setPassword(self):
        oldpwd = self.oldpwd.text()
        pwd1 = self.pwd1.text()
        pwd2 = self.pwd2.text()
        if (pwd1 == pwd2 and self.dao.change_password(oldpwd, pwd1)):
            self.label_4.setText("Password successfully saved")

        elif (pwd1 == pwd2 and not self.dao.change_password(oldpwd, pwd1)):
            self.label_4.setText("The current password entered is incorrect. Please try again.")

        elif (pwd1 != pwd2 and self.dao.change_password(oldpwd, pwd1)):
            self.label_4.setText("The new passwords do not match. Please try again.")

        else:
            self.label_4.setText("One or more input has been incorrect. Please try again.")

        self.oldpwd.clear()
        self.pwd1.clear()
        self.pwd2.clear()


    def sendEmail(self):
        self.dao.send_email()
        self.label_4.setText("A temporary password was sent to the email on file. Please check your email.")

    def turnOffPasswordPage(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 2)

class disablePasswordPage(QDialog):

    def __init__(self, data_access_object, widget):
        super(disablePasswordPage, self).__init__()
        uic.loadUi("disablePwd.ui", self)

        self.widget = widget
        self.dao = data_access_object
        
        self.enter.clicked.connect(self.turnOffPassword)
        self.pushButton_2.clicked.connect(self.goBack)

    def turnOffPassword(self):
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        pwd = self.lineEdit.text()
        if self.dao.password_is_valid(pwd) == True:
            self.dao.set_password_state(0)
            self.widget.setCurrentIndex(self.widget.currentIndex() - 5)
        else:
            self.label_3.setText("The current password entered is incorrect. Please try again.")
            self.lineEdit.clear()

        

    def goBack(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() - 2)




if __name__ == "__main__":

    app = QApplication(sys.argv)

    # intialize QStackWidget
    # QStackedwidget is a stack of QDialogs
    # we load different uis with it and each dialog is an index in the list
    # increment by one we show UI # 2 and so forth
    widget = QtWidgets.QStackedWidget()

    window1 = mainSetting()  # page 1
    window2 = setPassword()  # page 2
    window3 = shelftime()  # page 3
    window4 = currentPasswordPage()  # page 4
    window5 = resetApplication()
    window6 = disablePasswordPage()  # page 3
    # add the objects created above^ to the stack of screens
    widget.addWidget(window1)
    widget.addWidget(window2)
    widget.addWidget(window3)
    widget.addWidget(window4)
    widget.addWidget(window5)
    widget.addWidget(window6)
    widget.setFixedHeight(493)
    widget.setFixedWidth(370)

    window1 = settings.mainSetting(self, self.dao, self.window)  # page 1
    window2 = settings.setPassword(self.dao, self.window)  # page 2
    window3 = settings.shelftime(self.dao, self.window)  # page 3
    window4 = settings.currentPasswordPage(self.dao, self.window)  # page 4
    window5 = settings.resetApplication(self.dao, self.window, self)  # page 5
    window6 = settings.disablePasswordPage(self.dao, self.window)  # page 6
       
       
    # show the widget
    widget.show()

    sys.exit(app.exec_())

    # print("Exiting")
