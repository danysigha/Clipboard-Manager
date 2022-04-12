## create table################################################

# 1. import module
import sqlite3
# ----------> Added for just testing (LISA)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from tkinter import Tk
from PIL import ImageGrab
# ----------> Added for just testing (LISA)
from password_hashing import encryptPassword

#encoding
# <<git clone https://github.com/sqlcipher/sqlcipher.git>> needed
# brew install wget
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# sudo wget https://www.openssl.org/source/openssl-1.0.2e.tar.gz
# sudo tar -zxvf openssl-1.0.2e.tar.gz
# cd openssl-1.0.2e
# sudo ./config --prefix=/usr --openssldir=/usr/local/openssl shared
# sudo make
# sudo make install

# from clipboardManager_functions import *

# 2. open DB file
conn = sqlite3.connect('sql-encrypt/sqlcipher/ClipboardManager_DB.db, pragma key=’secretKey’')

# 3. make cursor
cursor = conn.cursor()
###############################################################

# 4. SQL command to create
CREATE_CARD_ENTITY = """
    CREATE TABLE IF NOT EXISTS card(
        cardId INTEGER primary key AUTOINCREMENT,
        cardContent TEXT not null,
        cardCategory TEXT not null,
        cardAddedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        cardModifiedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        folderID INTEGER not null
    );"""

CREATE_FOLDER_ENTITY = """
    CREATE TABLE IF NOT EXISTS folder(
        folderID INTEGER primary key AUTOINCREMENT,
        folderName TEXT not null,
        userID INTEGER not null
    );"""

CREATE_USER_ENTITY = """
    CREATE TABLE IF NOT EXISTS user(
        userID INTEGER primary key,
        currentCardID INTEGER not null,
        defaultFolderID INTEGER not null,
        shelfTime INTEGER not null
    );"""

# 4.1 card datas?
    # card datas
user1_card_datas = [
    (1,'this is the user1\'s card content1 and it is in folderID 1','user1\'s card category 1',"2012-01-21 00:00:00.000","2022-03-21 00:00:00.000", 1),
    (2,'this is the user1\'s card content2 and it is in folderID 2','user1\'s card category 1',"2013-02-21 00:00:00.000","2022-03-22 00:00:00.000", 2),
    (3,'this is the user1\'s card content3 and it is in folderID 2','user1\'s card category 2',"2014-03-21 00:00:00.000","2022-03-22 00:00:00.000", 2),
    (4,'this is the user1\'s card content4 and it is in folderID 1','user1\'s card category 2',"2015-04-21 00:00:00.000","2022-03-21 00:00:00.000", 1)
]

user2_card_datas = [
    (5,'this is the user2\'s card content1 and it is in folderID 3','user2\'s card category 1',"2012-02-21 00:00:00.000","2022-03-21 00:00:00.000", 3),
    (6,'this is the user2\'s card content2 and it is in folderID 3','user2\'s card category 1',"2013-03-21 00:00:00.000","2022-03-22 00:00:00.000", 3),
    (7,'this is the user2\'s card content3 and it is in folderID 4','user2\'s card category 2',"2014-04-21 00:00:00.000","2022-03-22 00:00:00.000", 4),
    (8,'this is the user2\'s card content4 and it is in folderID 4','user2\'s card category 2',"2015-05-21 00:00:00.000","2022-03-21 00:00:00.000", 4)
]

    # folder datas
    # user1 owns folderID 1 and 2
        # in folderID 1, there are card 1 and 4
        # in folderID 2, there are card 2 and 3
    # user 2 owns folderID 3 and 4
        # in folderID 3, there are card 5 and 6
        # in folderID 4, there are card 7 and 8
user1_folder_datas = [
    (1, 'user1 folder1 (default)', 1),
    (2, 'user1 folder2', 1)
]

user2_folder_datas = [
    (3, 'user2 folder1 (default)', 2),
    (4, 'user2 folder2', 2)
]

    # user datas
    #id, currentCardID,  defaultFolderID, shelfTime (month-wise)
user_datas = [
    (1, 4,               1,               120),
    (2, 8,               3,               140)
]

# 5. run SQL command
cursor.execute(CREATE_CARD_ENTITY)
cursor.execute(CREATE_FOLDER_ENTITY)
cursor.execute(CREATE_USER_ENTITY)

# 5.1 try inputting datas(?)
    # card datas
cursor.executemany("INSERT INTO card VALUES (?, ?, ?, ?, ?, ?)", user1_card_datas)
cursor.executemany("INSERT INTO card VALUES (?, ?, ?, ?, ?, ?)", user2_card_datas)
    # folder datas
cursor.executemany("INSERT INTO folder VALUES (?, ?, ?)", user1_folder_datas)
cursor.executemany("INSERT INTO folder VALUES (?, ?, ?)", user2_folder_datas)
    # user datas
cursor.executemany("INSERT INTO user VALUES (?, ?, ?, ?)", user_datas)

# some functions
def print_table(table_content): # just for printing all the result
    for i in range(len(table_content)):
        print("=========== " + str(table_content[i][0]) +  " ===========")
        for j in range(len(table_content[i])):
            print(table_content[i][j])

    print("===============================")

def test_db(userID, data_type = "all"):
    test_info_card = ["cardID", "cardContent", "cardCategory", "cardAddedDate", "cardModifiedDate", "folderID"]
    test_info_folder = ["folderID", "folderName", "userID"]
    test_info_user = ["userID", "currentCardID", "currentCardID", "shelfTime"]

    # print user table
    if (data_type == "user"):
        cursor.execute('SELECT * FROM user WHERE userID == ' + str(userID) + ';')
        table_list = cursor.fetchall()
        for i in range(len(table_list)):
            print("=============================")
            for j in range(len(table_list[i])):
                print(test_info_user[j] + ": " + str(table_list[i][j]))

    # print folder table
    elif (data_type == "folder"):
        cursor.execute('SELECT * FROM folder WHERE userID == ' + str(userID) + ';')
        table_list = cursor.fetchall()
        for i in range(len(table_list)):
            print("=============================")
            for j in range(len(table_list[i])):
                print(test_info_folder[j] + ": " + str(table_list[i][j]))

    # print card table
    elif (data_type == "card"):
        cursor.execute('SELECT cardID, cardContent, cardCategory, cardAddedDate, cardModifiedDate, card.folderID FROM card, folder WHERE folder.userID == ' + str(userID) + ' AND folder.folderID == card.folderID')
        table_list = cursor.fetchall()
        for i in range(len(table_list)):
            print("=============================")
            for j in range(len(table_list[i])):
                print(test_info_card[j] + ": " + str(table_list[i][j]))

            # result = cursor.fetchall()
            # print(result)
            # print("Belongs to user " + str(result[0][0]))

    else:
        print("========= USER =========")
        test_db(userID, "user")
        print("========= FOLDER =========")
        test_db(userID, "folder")
        print("========= CARD =========")
        test_db(userID, "card")

def addCard(userID, content, category): # to be implemented even more later -> copy card
    # find the user's default folder
    cursor.execute('SELECT defaultFolderID FROM user WHERE userID == ' + str(userID) + ";")
    defaultFolderID_loc = cursor.fetchall()[0][0]

    cursor.execute('INSERT INTO card(cardContent, cardCategory, cardAddedDate, cardModifiedDate, folderID) VALUES(?, ?, datetime("now", "localtime"), datetime("now", "localtime"), ?)', (content, category, defaultFolderID_loc))

    # get the currentCardID -> maybe can be done by the upper layer or dnt need it
    # cursor.execute('SELECT cardID FROM card, folder WHERE card.folderID == folder.folderID AND folder.userID == '+ str(userID) + ';')
    # result = cursor.fetchall()
    # cardIDs = list()
    # for i in range(len(result)):
    #     cardIDs.append(result[i][0])
    # cardIDs.sort() # so cardIDs[-1] would be the most recent card added (currentCardID)

    # cursor.execute('UPDATE user SET currentCardID = ' + str(cardIDs[-1]) + ' WHERE userID == ' + str(userID) + ';')

# paste function to be implemented later
def pasteCard(cardID):
    cursor.execute('SELECT cardContent FROM card WHERE cardID == ' + str(cardID) + ';')
    result = cursor.fetchall()
    return result[0][0]

# delete
def deleteCard(cardID):
    cursor.execute('DELETE FROM card WHERE cardID == ' + str(cardID) + ';')

def automaticDelete_shelftime(userID):
    # this must be called once in a while by the main system for the system to check and delete
    cursor.execute('SELECT userID, shelfTime FROM user WHERE userID == ' + str(userID))
    shelftime_months = cursor.fetchall()[0][1]
    # print(shelftime_months)
    cursor.execute('DELETE FROM card WHERE cardAddedDate <= datetime(\'now\', \'localtime\', \'-' + str(shelftime_months) +' months\');')

# search
# def showCard(userID, searchType, searchContent):
    # cursor.execute('SELECT * FROM card, folder WHERE userID == ' + str(userID) + ' AND ' + str(searchType) + '')

# sorting
def sortCard(folderID, sortType):
    # the folderID is included because we usually will sort within the folder that the user is looking at currently.
    # please enter the folder that the user is currently taking a look at
    cursor.execute('SELECT * FROM card WHERE folderID == ' + str(folderID) + ' ORDER BY ' + str(sortType))
    return cursor.fetchall()

# change shelf time
def changeShelfTIme(userID, newShelfTime):
    cursor.execute('UPDATE user SET shelfTime = ' + str(newShelfTime) + ' WHERE userID == ' + str(userID) + ';')

# set password?

# hide card

# favorite function

# create folder (HERE)
def createFolder(userID, folderName):
    cursor.execute("INSERT INTO folder(folderName, userID) VALUES(?, ?)", (folderName, userID))

# delete folder
def deleteFolder(userID, folderID):
    cursor.execute('DELETE FROM folder WHERE folderID == ' + str(folderID) + ';')

# update folder
def updateFolderID_all(userID, currentFolderID, newFolderID):
    # this function changes the folderID inside the card entity, not the folder itself
    # this function changes all the folderIDs of the matching cards
    # can be used to change entire card deck.
    cursor.execute('UPDATE card SET folderID = ' + str(newFolderID) + ' WHERE folderID == ' + str(currentFolderID) + ';')

def updateFolderID_indiv(userID, cardID, newFolderID):
    # this function changes the folderID inside the card entity, but solely one card.
    cursor.execute('UPDATE card SET folderID = ' + str(newFolderID) + ' WHERE cardID == ' + str(cardID) +';')

# rename folder
def updateFolder_Name(userID, currentFolderName, newFolderName): # because we do not know what the folderID is on point, let the program do it
    # find currentFolderID
    cursor.execute('UPDATE card SET folderName = ' + str(newFolderName) + ' WHERE folderName == ' + str(currentFolderName))

# unlock password
# 6. check if the table was made well

# ----------> Added for just testing (LISA)
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.copyNow = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.press_it())
        self.copyNow.setGeometry(QtCore.QRect(60, 430, 131, 51))
        self.copyNow.setObjectName("copyNow")
        self.copyLabel = QtWidgets.QLabel(self.centralwidget)
        self.copyLabel.setGeometry(QtCore.QRect(40, 180, 251, 171))
        self.copyLabel.setText("")
        self.copyLabel.setObjectName("copyLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def press_it(self):
        try:
            copy = Tk().clipboard_get()
        except:
            copy = ImageGrab.grabclipboard()
        if isinstance(copy,str):
            self.copyLabel.setText(copy)
            addCard(1, copy, "Default")
            test_db(1, "card")
        else:
            copy.save('paste.png', 'PNG')
            pixmap = QPixmap('paste.png')
            self.copyLabel.setPixmap(pixmap)


           # self.resize(pixmap.width(),pixmap.height())



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.copyNow.setText(_translate("MainWindow", "grab copy"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

# ----------> Added for just testing (LISA)

# 6. close DB
conn.close()
