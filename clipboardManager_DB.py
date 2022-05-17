import sqlite3

def connectToDb():
    """Creates a connection to the database"""
    conn = sqlite3.connect('ClipboardManager_DB.db, pragma key=’secretKey’')
    cursor = conn.cursor()
    return conn,cursor

def closeDb(conn):
    """Closes the connection to the database"""
    conn.commit()
    conn.close()
    

def initalizeDb():
    """Initally creates the database and all the tables"""
    conn,cursor = connectToDb()

    cursor = conn.cursor()
    CREATE_CARD_ENTITY = """
        CREATE TABLE IF NOT EXISTS card(
            cardID TEXT not null,
            cardContent TEXT not null,
            cardCategory TEXT not null,
            cardAddedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            cardModifiedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            folderID INTEGER not null,
            hideCard INTEGER not null,
            favoriteCard INTEGER not null
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
            shelfTime INTEGER not null,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            password_exists BOOLEAN NOT NULL
        );"""
    closeDb(conn)

def addCard(userID, card_id, content, category, hideCard, favoriteCard): 
    """ Adds record of a new card with the given parameters"""
    
    conn,cursor = connectToDb()
    cursor.execute('SELECT defaultFolderID FROM user WHERE userID == ' + str(userID) + ";")\
    defaultFolderID_loc = 1
    cursor.execute('INSERT INTO card(cardID, cardContent, cardCategory, cardAddedDate, cardModifiedDate, folderID, hideCard, favoriteCard) VALUES(?, ?, ?, datetime("now", "localtime"), datetime("now", "localtime"), ?, ?, ?)', (card_id, content, category, defaultFolderID_loc, hideCard, favoriteCard))
    closeDb(conn)


def getSearchCards(search):
    """
    Queries the database for cards that contain the query and returns them

    Parameters:
    
    search (str): the search query to query the database with
    
    """
    
    conn,cursor = connectToDb()
    cursor.execute("""SELECT * FROM card WHERE cardContent LIKE """ + "\"%" + str(search) + "%\"")
    records = cursor.fetchall()

    closeDb(conn)
    
    return records


def getFavoriteCards():
    """ Queries the database for cards that are favorited and returns them"""
    
    conn,cursor = connectToDb()
    cursor.execute("""SELECT * FROM card WHERE favoriteCard = "1" """)
    records = cursor.fetchall()

    closeDb(conn)
    return records



def deleteCard(cardId):
    """
    Removes card record from the database

    Parameters:
    
    cardId (str): the desired card key 
    
    
    """
    conn,cursor = connectToDb()
    cursor.execute('DELETE FROM card WHERE cardID == "' + str(cardId) + '";')
    conn.commit()
    conn.close()



def getUserStatus():
    conn,cursor = connectToDb()
    cursor.execute("SELECT count(*) FROM user"+ ';')
    count = cursor.fetchall()[0][0]
    closeDb(conn)
    return count

def getPassword():
    conn,cursor = connectToDb()
    cursor.execute("""SELECT password FROM user""")
    table = cursor.fetchall()
    pwd = table[0][0]
    closeDb(conn)
    return pwd

def getEmail():
    conn,cursor = connectToDb()
    cursor.execute("""SELECT email FROM user""")
    table = cursor.fetchall()
    email = table[0][0]
    closeDb(conn)
    return email

def setEmail(email):
    conn,cursor = connectToDb()
    cursor.execute("""UPDATE user SET email = (?) WHERE userID = 1""", (email,))
    closeDb(conn)

def createUser(email):
    conn,cursor = connectToDb()
    user_datas = [
        (1, 4, 1, 12, email, "", 0),
    ]
    cursor.executemany("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?, ?)", user_datas)
    closeDb(conn)



def changePassword(newPwd):
    conn,cursor = connectToDb()
    cursor.execute("""UPDATE user SET password = (?) WHERE userID = 1""", (newPwd,))
    closeDb(conn)

def setPasswordState(state):
    conn,cursor = connectToDb()
    cursor.execute("""UPDATE user SET password_exists = (?) WHERE userID = 1""", (state,))
    closeDb(conn)

def getPasswordState():
    conn,cursor = connectToDb()
    cursor.execute("""SELECT password_exists FROM user""")
    table = cursor.fetchall()
    state = table[0][0]
    closeDb(conn)
    return state


def getAllCards():
    """Returns all card records from the database"""
    
    conn,cursor = connectToDb()
    cursor.execute("SELECT * FROM card")
    records = cursor.fetchall()
    closeDb(conn)
    return records

def getTextCards():
    """Returns all card records that contain "Text" in their cardCategory field"""
    conn,cursor = connectToDb()

    cursor.execute("""SELECT * FROM card WHERE cardCategory = "Text" """)
    records = cursor.fetchall()

    closeDb(conn)
    return records

def getImageCards():
    """Returns all card records that contain "Image" in their cardCategory field"""
    
    conn,cursor = connectToDb()
    cursor.execute("""SELECT * FROM card WHERE cardCategory = "Image" """)
    records = cursor.fetchall()
    closeDb(conn)
    return records

def getUrlCards():
    """Returns all card records that contain "URL" in their cardCategory field"""

    conn,cursor = connectToDb()
    cursor.execute("""SELECT * FROM card WHERE cardCategory = "URL" """)
    records = cursor.fetchall()
    closeDb(conn)
    return records

def automaticDeleteShelftime(userID): # must be called in login page
    conn,cursor = connectToDb()
    # this must be called once in a while by the main system for the system to check and delete
    cursor.execute('SELECT userID, shelfTime FROM user WHERE userID == ' + str(userID))
    shelftime_months = cursor.fetchall()[0][1]
    # print(shelftime_months)
    cursor.execute('DELETE FROM card WHERE cardAddedDate <= datetime(\'now\', \'localtime\', \'-' + str(shelftime_months) +' months\');')
    closeDb(conn)

def changeShelftime(month):
    conn,cursor = connectToDb()
    cursor.execute("""UPDATE user SET shelfTime = (?) WHERE userID = 1""", (month,))
    closeDb(conn)

def hideCard(newCardStatus, cardId):
    """
    Sets the card record's hidden  field
    
    Parameters:
    
    newCardStatus (int): 1 or 0 mapping to true or false respectively
    
    cardId (str): the desired card key 

    """
    conn,cursor = connectToDb()
    cursor.execute('UPDATE card SET hideCard = "' + str(newCardStatus) + '" WHERE cardID == "' + str(cardId) + '";')
    closeDb(conn)


def favoriteCard(favoriteStatus, cardId):
    """
    Sets the card record's hidden  field
    
    Parameters:
    
    favoriteStatus (int): 1 or 0 mapping to true or false respectively
    
    cardId (str): the desired card key 

    """
    conn,cursor = connectToDb()
    cursor.execute(
        'UPDATE card SET favoriteCard = "' + str(favoriteStatus) + '" WHERE cardID == "' + str(cardId) + '";')

    closeDb(conn)


def resetdb():
    conn,cursor = connectToDb()
    cursor.execute("""DELETE FROM user""")
    cursor.execute("""DELETE FROM folder""")
    cursor.execute("""DELETE FROM card""")
    closeDb(conn)
