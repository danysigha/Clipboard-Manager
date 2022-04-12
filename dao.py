import sqlite3
import clipboardManager_DB as db

class dataaccessobject():
    pass
# decryption takes place here
    # UI grabs the decryption key from user and pass to data access object
    def grabAll(self):
        conn = sqlite3.connect("ClipboardManager_DB.db")
        c = conn.cursor
        c.execute('SELECT * FROM card')
        records = c.fectchall()
        conn.commit()
        conn.close()

