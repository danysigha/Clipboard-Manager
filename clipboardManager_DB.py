## create table################################################

# 1. import module
import sqlite3

# 2. open DB file
conn = sqlite3.connect('trialClipboardManager.db')

# 3. make cursor
cursor = conn.cursor()
###############################################################

# 4. SQL command to create
CREATE_CARD_ENTITY = """
    CREATE TABLE IF NOT EXISTS card(
        cardId INTEGER primary key,
        cardAddedYear INTEGER not null,
        cardAddedMonth INTEGER not null,
        cardAddedDate INTEGER not null,
        cardModifiedYear INTEGER not null,
        cardModifiedMonth INTEGER not null,
        cardModifiedDate INTEGER not null,
        cardContent TEXT not null,
        cardCategory TEXT not null
    );"""

CREATE_FOLDER_ENTITY = """
    CREATE TABLE IF NOT EXISTS folder(
        folderID INTEGER primary key,
        folderName TEXT not null
    );"""

CREATE_USER_ENTITY = """
    CREATE TABLE IF NOT EXISTS user(
        userID INTEGER primary key,
        password TEXT not null,
        currentCardID INTEGER not null,
        shelfTime INTEGER not null
    );"""

# TODO: add category data + user_category data

CREATE_FOLDER_CONTAINS_ENTITY = """
    CREATE TABLE IF NOT EXISTS folder_contains(
        folderID INTEGER,
        cardID INTEGER
    );"""

CREATE_USER_FOLDER_ENTITY = """
    CREATE TABLE IF NOT EXISTS user_folder(
        userID INTEGER,
        folderID INTEGER
    );"""

CREATE_USER_CARD_ENTITY = """
    CREATE TABLE IF NOT EXISTS user_card(
        userID INTEGER,
        cardID INTEGER
    );"""


# 4.1 card datas?
    # card datas
user1_card_datas = [
    (1,2012,3,21,2022,3,21,'this is the user1\'s card content1 and it is in folderID 1','user1\'s card category 1'),
    (2,2013,3,21,2022,3,22,'this is the user1\'s card content2 and it is in folderID 2','user1\'s card category 1'),
    (3,2014,3,21,2022,3,22,'this is the user1\'s card content3 and it is in folderID 2','user1\'s card category 2'),
    (4,2015,3,21,2022,3,21,'this is the user1\'s card content4 and it is in folderID 1','user1\'s card category 2')
]

user2_card_datas = [
    (5,2012,3,21,2022,3,21,'this is the user2\'s card content1 and it is in folderID 3','user2\'s card category 1'),
    (6,2013,3,21,2022,3,22,'this is the user2\'s card content2 and it is in folderID 3','user2\'s card category 1'),
    (7,2014,3,21,2022,3,22,'this is the user2\'s card content3 and it is in folderID 4','user2\'s card category 2'),
    (8,2015,3,21,2022,3,21,'this is the user2\'s card content4 and it is in folderID 4','user2\'s card category 2')
]

    # folder datas
user1_folder_datas = [
    (1, 'user1 folder1'),
    (2, 'user1 folder2')
]

user2_folder_datas = [
    (3, 'user2 folder1'),
    (4, 'user2 folder2')
]

    # user datas
    #id, password      , currentCardID,    shelfTime (month-wise)
user_datas = [
    (1, 'user_password1', 4,               120),
    (2, 'user_password2', 8,               140)
]

    # folder_contains data
        # user1 owns folderID 1 and 2
            # in folderID 1, there are card 1 and 4
            # in folderID 2, there are card 2 and 3
        # user 2 owns folderID 3 and 4
            # in folderID 3, there are card 5 and 6
            # in folderID 4, there are card 7 and 8
  # folderID, cardID
folder_contains_datas = [
    (1,         1),
    (1,         4),
    (2,         2),
    (2,         3),
    (3,         5),
    (3,         6),
    (4,         7),
    (4,         8)
]

    # user_folder data -> who owns what folderIDs
   # userrID, folderID
user_folder_datas = [
    (1,         1),
    (1,         2),
    (2,         3),
    (2,         4)
]

    # user_card data -> who owns what cardIDs
   # userID, cardID
user_card_datas = [
    (1,        1),
    (1,        2),
    (1,        3),
    (1,        4),
    (2,        5),
    (2,        6),
    (2,        7),
    (2,        8),
]


# 5. run SQL command
cursor.execute(CREATE_CARD_ENTITY)
cursor.execute(CREATE_FOLDER_ENTITY)
cursor.execute(CREATE_USER_ENTITY)
cursor.execute(CREATE_FOLDER_CONTAINS_ENTITY)
cursor.execute(CREATE_USER_FOLDER_ENTITY)
cursor.execute(CREATE_USER_CARD_ENTITY)

# 5.1 try inputting datas(?)
    # card datas
cursor.executemany("INSERT INTO card VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", user1_card_datas)
cursor.executemany("INSERT INTO card VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", user2_card_datas)
    # folder datas
cursor.executemany("INSERT INTO folder VALUES (?, ?)", user1_folder_datas)
cursor.executemany("INSERT INTO folder VALUES (?, ?)", user2_folder_datas)
    # user datas
cursor.executemany("INSERT INTO user VALUES (?, ?, ?, ?)", user_datas)
    # folder_contains
cursor.executemany("INSERT INTO folder_contains VALUES (?, ?)", folder_contains_datas)
    # user_folder
cursor.executemany("INSERT INTO user_folder VALUES (?, ?)", user_folder_datas)
    # user_card
cursor.executemany("INSERT INTO user_card VALUES (?, ?)", user_card_datas)

# 6. check if the table was made well
cursor.execute('SELECT * FROM card WHERE cardAddedYear > 2013;')
table_list = cursor.fetchall()
for i in range(len(table_list)):
    print("=========== card " + str(table_list[i][0]) +  " ===========")
    for j in range(len(table_list[i])):
        print(table_list[i][j])

print("===============================")

# 6. close DB
conn.close()
