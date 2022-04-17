import sqlite3
import clipboardManager_DB as db

class DataAccessObject():
    def __init__(self):
        pass
# decryption takes place here
    # UI grabs the decryption key from user and pass to data access object


    def initializeUI(self):
        conn = sqlite3.connect("ClipboardManager_DB.db")
        c = conn.cursor
        c.execute('SELECT * FROM card')
        records = c.fectchall()
        conn.commit()
        conn.close()

        for i in records:
            print(i)

    def decryption(self, key):
        pass

if __name__ == "__main__":
        dao1 = DataAccessObject()
        dao1.initializeUI()



