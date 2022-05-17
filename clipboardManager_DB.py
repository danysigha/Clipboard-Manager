import sqlite3


def connectToDb():
    """
    Creates a connection to the database.

    """

    conn = sqlite3.connect('ClipboardManager_DB.db, pragma key=’secretKey’')
    cursor = conn.cursor()
    return conn, cursor


def closeDb(conn):
    """
    Closes the connection to the database.

    """

    conn.commit()
    conn.close()


def initalizeDb():
    """
    Initially creates the database and all the tables.

    """

    conn, cursor = connectToDb()
    cursor = conn.cursor()
    CREATE_CARD_ENTITY = """
        CREATE TABLE IF NOT EXISTS card(
            cardID TEXT not null,
            cardContent TEXT not null,
            cardCategory TEXT not null,
            hideCard INTEGER not null,
            favoriteCard INTEGER not null
        );"""

    

    CREATE_USER_ENTITY = """
        CREATE TABLE IF NOT EXISTS user(
            userID INTEGER primary key,
            currentCardID INTEGER not null,
            defaultFolderID INTEGER not null,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            password_exists BOOLEAN NOT NULL
        );"""
    closeDb(conn)

def addCard(userID, card_id, content, category, hideCard, favoriteCard):
    """
    Adds record of a new card with the given parameters.

    """

    conn, cursor = connectToDb()
    cursor.execute('SELECT defaultFolderID FROM user WHERE userID == ' + str(userID) + ";") \
            defaultFolderID_loc = 1
    cursor.execute(
        'INSERT INTO card(cardID, cardContent, cardCategory, hideCard, favoriteCard) VALUES(?, ?, ?, ?, ?, ?)',
        (card_id, content, category, defaultFolderID_loc, hideCard, favoriteCard))
    closeDb(conn)

def getSearchCards(search):
    """
    Queries the database for cards that contain the query and returns them.

    Parameters:
    search (str): the search query to query the database with

    """

    conn, cursor = connectToDb()
    cursor.execute("""SELECT * FROM card WHERE cardContent LIKE """ + "\"%" + str(search) + "%\"")
    records = cursor.fetchall()
    closeDb(conn)
    return records

def getFavoriteCards():
    """
    Queries the database for cards that are favorited and returns them.

    """

    conn, cursor = connectToDb()
    cursor.execute("""SELECT * FROM card WHERE favoriteCard = "1" """)
    records = cursor.fetchall()
    closeDb(conn)
    return records


def deleteCard(cardId):
    """
    Removes card record from the database.

    Parameters:
    cardId (str): the desired card key

    """

    conn, cursor = connectToDb()
    cursor.execute('DELETE FROM card WHERE cardID == "' + str(cardId) + '";')
    conn.commit()
    conn.close()


def getUserStatus():
    """
    Queries the database for the current status of the user.

    """
    conn, cursor = connectToDb()
    cursor.execute("SELECT count(*) FROM user" + ';')
    count = cursor.fetchall()[0][0]
    closeDb(conn)
    return count


def getPassword():
    """
    Queries the database for the current password stored.

    """
    conn, cursor = connectToDb()
    cursor.execute("""SELECT password FROM user""")
    table = cursor.fetchall()
    pwd = table[0][0]
    closeDb(conn)
    return pwd


def getEmail():
    """
    Queries the database for the email stored.

    """

    conn, cursor = connectToDb()
    cursor.execute("""SELECT email FROM user""")
    table = cursor.fetchall()
    email = table[0][0]
    closeDb(conn)
    return email


def setEmail(email):
    """
    Send the email to the database.

    """

    conn, cursor = connectToDb()
    cursor.execute("""UPDATE user SET email = (?) WHERE userID = 1""", (email,))
    closeDb(conn)


def createUser(email):
    """
    Sends user information to database to occupy user table.

    """

    conn, cursor = connectToDb()
    user_datas = [
        (1, 4, 1, email, "", 0),
    ]
    cursor.executemany("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?)", user_datas)
    closeDb(conn)


def changePassword(newPwd):
    """
    Updates the current password in the database.

    """

    conn, cursor = connectToDb()
    cursor.execute("""UPDATE user SET password = (?) WHERE userID = 1""", (newPwd,))
    closeDb(conn)


def setPasswordState(state):
    """
    Updates the state of the password in database.

    """

    conn, cursor = connectToDb()
    cursor.execute("""UPDATE user SET password_exists = (?) WHERE userID = 1""", (state,))
    closeDb(conn)


def getPasswordState():
    """
    Queries the database for the current state of the password.

    """

    conn, cursor = connectToDb()
    cursor.execute("""SELECT password_exists FROM user""")
    table = cursor.fetchall()
    state = table[0][0]
    closeDb(conn)
    return state


def getAllCards():
    """
    Returns all card records from the database.

    """

    conn, cursor = connectToDb()
    cursor.execute("SELECT * FROM card")
    records = cursor.fetchall()
    closeDb(conn)
    return records


def getTextCards():
    """
    Returns all card records that contain "Text" in their cardCategory field.

    """

    conn, cursor = connectToDb()
    cursor.execute("""SELECT * FROM card WHERE cardCategory = "Text" """)
    records = cursor.fetchall()
    closeDb(conn)
    return records


def getImageCards():
    """
    Returns all card records that contain "Image" in their cardCategory field.

    """

    conn, cursor = connectToDb()
    cursor.execute("""SELECT * FROM card WHERE cardCategory = "Image" """)
    records = cursor.fetchall()
    closeDb(conn)
    return records


def getUrlCards():
    """
    Returns all card records that contain "URL" in their cardCategory field.

    """

    conn, cursor = connectToDb()
    cursor.execute("""SELECT * FROM card WHERE cardCategory = "URL" """)
    records = cursor.fetchall()
    closeDb(conn)
    return records


def automaticDeleteShelftime(userID):  # must be called in login page
    """
    Deletes the card information from card table.

    """

    conn, cursor = connectToDb()
    # this must be called once in a while by the main system for the system to check and delete
    cursor.execute('SELECT userID, shelfTime FROM user WHERE userID == ' + str(userID))
    shelftime_months = cursor.fetchall()[0][1]
    # print(shelftime_months)
    cursor.execute('DELETE FROM card WHERE cardAddedDate <= datetime(\'now\', \'localtime\', \'-' + str(
        shelftime_months) + ' months\');')
    closeDb(conn)


def changeShelfLife(month):
    """
    Updates the shelf life of cards.

    """

    conn, cursor = connectToDb()
    cursor.execute("""UPDATE user SET shelfTime = (?) WHERE userID = 1""", (month,))
    closeDb(conn)


def hideCard(newCardStatus, cardId):
    """
    Sets the card record's hidden  field.

    Parameters:
    newCardStatus (int): 1 or 0 mapping to true or false respectively
    cardId (str): the desired card key

    """

    conn, cursor = connectToDb()
    cursor.execute('UPDATE card SET hideCard = "' + str(newCardStatus) + '" WHERE cardID == "' + str(cardId) + '";')
    closeDb(conn)


def favoriteCard(favoriteStatus, cardId):
    """
    Sets the card record's hidden  field.

    Parameters:
    favoriteStatus (int): 1 or 0 mapping to true or false respectively
    cardId (str): the desired card key

    """

    conn, cursor = connectToDb()
    cursor.execute(
        'UPDATE card SET favoriteCard = "' + str(favoriteStatus) + '" WHERE cardID == "' + str(cardId) + '";')
    closeDb(conn)


def resetdb():
    """
    Deletes all tables and information from database.

    """

    conn, cursor = connectToDb()
    cursor.execute("""DELETE FROM user""")
    cursor.execute("""DELETE FROM folder""")
    cursor.execute("""DELETE FROM card""")
    closeDb(conn)
