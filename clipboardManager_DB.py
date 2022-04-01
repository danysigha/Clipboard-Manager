## create table################################################

# 1. import module
import sqlite3
# from clipboardManager_functions import *

# 2. open DB file
conn = sqlite3.connect('ClipboardManager_DB.db')

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

# TODO: add category data + user_category data

# CREATE_FOLDER_CONTAINS_ENTITY = """
#     CREATE TABLE IF NOT EXISTS folder_contains(
#         folderID INTEGER,
#         cardID INTEGER
#     );"""
#
# CREATE_USER_FOLDER_ENTITY = """
#     CREATE TABLE IF NOT EXISTS user_folder(
#         userID INTEGER,
#         folderID INTEGER
#     );"""

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

    # folder_contains data
        # user1 owns folderID 1 and 2
            # in folderID 1, there are card 1 and 4
            # in folderID 2, there are card 2 and 3
        # user 2 owns folderID 3 and 4
            # in folderID 3, there are card 5 and 6
            # in folderID 4, there are card 7 and 8
  # folderID, cardID
# folder_contains_datas = [
#     (1,         1),
#     (1,         4),
#     (2,         2),
#     (2,         3),
#     (3,         5),
#     (3,         6),
#     (4,         7),
#     (4,         8)
# ]

    # user_folder data -> who owns what folderIDs
   # userrID, folderID
# user_folder_datas = [
#     (1,         1),
#     (1,         2),
#     (2,         3),
#     (2,         4)
# ]

# 5. run SQL command
cursor.execute(CREATE_CARD_ENTITY)
cursor.execute(CREATE_FOLDER_ENTITY)
cursor.execute(CREATE_USER_ENTITY)
# cursor.execute(CREATE_FOLDER_CONTAINS_ENTITY)
# cursor.execute(CREATE_USER_FOLDER_ENTITY)
#
# 5.1 try inputting datas(?)
    # card datas
cursor.executemany("INSERT INTO card VALUES (?, ?, ?, ?, ?, ?)", user1_card_datas)
cursor.executemany("INSERT INTO card VALUES (?, ?, ?, ?, ?, ?)", user2_card_datas)
    # folder datas
cursor.executemany("INSERT INTO folder VALUES (?, ?, ?)", user1_folder_datas)
cursor.executemany("INSERT INTO folder VALUES (?, ?, ?)", user2_folder_datas)
    # user datas
cursor.executemany("INSERT INTO user VALUES (?, ?, ?, ?)", user_datas)
#     # folder_contains
# cursor.executemany("INSERT INTO folder_contains VALUES (?, ?)", folder_contains_datas)
# #     # user_folder
# cursor.executemany("INSERT INTO user_folder VALUES (?, ?)", user_folder_datas)

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

# select GIF?

# sorting

# change shelf time

# set password?

# hide card

# favorite function

# create folder (HERE)
def createFolder(userID, folderName):
    cursor.execute("INSERT INTO folder(folderName, userID) VALUES(?, ?)", (folderName, userID))

# delete folder

# update folder
def updateFolder_ID_all(userID, currentFolderID, newFolderID):
    # this function changes the folderID inside the card entity, not the folder itself
    # this function changes all the folderIDs of the matching cards
    cursor.execute('UPDATE card SET folderID = ' + str(newFolderID) + ' WHERE folderID == ' + str(currentFolderID) + ';')

def updateFolder_ID_indiv(userID, cardID, newFolderID):
    cursor.execute('UPDATE card SET folderID = ' + str(newFolderID) + ' WHERE cardID == ' + str(cardID) +';')

# def updateFolder_Name(userID, currentFolderName, newFolderName): # because we do not know what the folderID is on point, let the program do it
    # find currentFolderID
    # cursor.execute('SELECT * FROM ')


# unlock password
# 6. check if the table was made well

createFolder(1, "temp folder name")
updateFolder_ID_indiv(1, 1, 5)
test_db(1, "card")

# createFolder(1, "new folder!")

# test_db(1)

# 6. close DB
conn.close()
