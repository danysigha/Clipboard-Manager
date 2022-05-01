## create table################################################

# 1. import module
import sqlite3
# ----------> Added for just testing (LISA)
# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtGui import QIcon, QPixmap
# from tkinter import Tk
# from PIL import ImageGrab
# ----------> Added for just testing (LISA)
# from password_hashing import encryptPassword

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
# conn = sqlite3.connect('sql-encrypt/sqlcipher/ClipboardManager_DB.db, pragma key=’secret’')
conn = sqlite3.connect('ClipboardManager_DB.db')

# 3. make cursor
cursor = conn.cursor()
###############################################################

# 4. SQL command to create
CREATE_CARD_ENTITY = """
    CREATE TABLE IF NOT EXISTS card(
        cardId INTEGER primary key AUTOINCREMENT,
        cardContent TEXT NOT NULL,
        cardCategory TEXT NOT NULL,
        sourceApplication TEXT NOT NULL,
        dataType TEXT NOT NULL,
        cardAddedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        cardModifiedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        cardState INTEGER NOT NULL,
        favoriteSelected INTEGER NOT NULL,
        folderID INTEGER NOT NULL
    );"""

CREATE_FOLDER_ENTITY = """
    CREATE TABLE IF NOT EXISTS folder(
        folderID INTEGER primary key AUTOINCREMENT,
        folderName TEXT NOT NULL,
        userID INTEGER NOT NULL
    );"""

CREATE_USER_ENTITY = """
    CREATE TABLE IF NOT EXISTS user(
        userID INTEGER primary key AUTOINCREMENT,
        password TEXT NOT NULL,
        password_exists BOOLEAN NOT NULL,
        currentCardID INTEGER NOT NULL,
        defaultFolderID INTEGER NOT NULL,
        shelfTime INTEGER NOT NULL,
        email TEXT NOT NULL
    );"""

# 4.1 card datas
    # card datas
user1_card_datas = [
    (1,'this is the user1\'s card content1 and it is in folderID 1','user1\'s card category 1',"Kakaotalk", "Text", "2012-01-21 00:00:00.000","2022-03-21 00:00:00.000", 1, 0, 1),
    (2,'this is the user1\'s card content2 and it is in folderID 2','user1\'s card category 1',"Wechat","Text", "2013-02-21 00:00:00.000","2022-03-22 00:00:00.000", 1, 0, 2),
    (3,'this is the user1\'s card content3 and it is in folderID 2','user1\'s card category 2',"Whatsapp","Text", "2014-03-21 00:00:00.000","2022-03-22 00:00:00.000", 1, 0, 2),
    (4,'this is the user1\'s card content4 and it is in folderID 1','user1\'s card category 2',"Chrome","Text", "2015-04-21 00:00:00.000","2022-03-21 00:00:00.000", 1, 0, 1)
]

user2_card_datas = [
    (5,'this is the user2\'s card content1 and it is in folderID 3','user2\'s card category 1',"Wechat","Text", "2012-02-21 00:00:00.000","2022-03-21 00:00:00.000", 1, 0, 3),
    (6,'this is the user2\'s card content2 and it is in folderID 3','user2\'s card category 1',"Whatsapp","Text", "2013-03-21 00:00:00.000","2022-03-22 00:00:00.000", 1, 0, 3),
    (7,'this is the user2\'s card content3 and it is in folderID 4','user2\'s card category 2',"Chrome","Text", "2014-04-21 00:00:00.000","2022-03-22 00:00:00.000", 1, 0, 4),
    (8,'this is the user2\'s card content4 and it is in folderID 4','user2\'s card category 2',"Kakaotalk","Text", "2015-05-21 00:00:00.000","2022-03-21 00:00:00.000", 1, 0, 4)
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
    #id, password,       passwordExists,       currentCardID,  defaultFolderID, shelfTime (month-wise)
user_datas = [
    (1, "tempPassword1", False, 4,               1,               120, 'tinachen170@gmail.com'),
]

# 5. run SQL command
cursor.execute(CREATE_CARD_ENTITY)
cursor.execute(CREATE_FOLDER_ENTITY)
cursor.execute(CREATE_USER_ENTITY)

# 5.1 try inputting datas(?)
    # card datas
cursor.executemany("INSERT INTO card VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", user1_card_datas)
cursor.executemany("INSERT INTO card VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", user2_card_datas)
    # folder datas
cursor.executemany("INSERT INTO folder VALUES (?, ?, ?)", user1_folder_datas)
cursor.executemany("INSERT INTO folder VALUES (?, ?, ?)", user2_folder_datas)
    # user datas
cursor.executemany("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?)", user_datas)

conn.commit()


conn.close()