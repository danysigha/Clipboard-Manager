import sqlite3
import card
import clipboardManager_DB as db


class DataAccessor:
    def __init__(self):
        pass
# decryption takes place here
    # UI grabs the decryption key from user and pass to data access object
    def storeCard(self, content, dataType):
        db.addCard(1, content, dataType)
        # card.Card(content, dataType, db.getLastCardID()+1)

    def deleteCard(self, id):
        db.deleteCard(id)
        # db.deleteCard()
    # def updateCard(self):
    #     pass
    def readCard(self, id):
        return db.pasteCard(id)

    def getNextID(self):
        return 1+db.getLastCardID()

    def getAllCards(self):
        return db.getAllCards()


    # def initializeUI(self):
    #     conn = sqlite3.connect("ClipboardManager_DB.db")
    #     c = conn.cursor
    #     c.execute('SELECT * FROM card')
    #     records = c.fectchall()
    #     conn.commit()
    #     conn.close()
    #
    #     for i in records:
    #         print(i)

    # def decryption(self, key):
    #     pass

if __name__ == "__main__":
        # dao1 = DataAccessObject()
        # dao1.initializeUI()
        pass


