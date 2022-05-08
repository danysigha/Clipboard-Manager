import sqlite3
import card
import bcrypt
import platform
import smtplib
import ssl
import string
import random
import clipboardManager_DB as db

class password_decorator:
    def __init__(self, function):
        self.function = function
        # self.dao = DataAccessor()
    def password_is_valid(self, pwd):
        h = db.get_password()
        return bcrypt.checkpw(pwd.encode('utf-8'), h)


    def __call__(self, *args, **kwargs):
        pwd = args[0]
        # if self.password_is_valid(pwd):
        if self.password_is_valid(pwd):
            self.function(*args, **kwargs)
            result = True
        else:
            result = False

        return result

class DataAccessor:
    def __init__(self):
        pass
# decryption takes place here
    # UI grabs the decryption key from user and pass to data access object
    def storeCard(self, card_id, content, dataType, hideCard):
        db.addCard(1, card_id, content, dataType, hideCard)
        # card.Card(content, dataType, db.getLastCardID()+1)

    def deleteCard(self, id):
        db.deleteCard(id)
        # db.deleteCard()
    # def updateCard(self):
    #     pass
    def readCard(self, id):
        return db.pasteCard(id)

    def getAllCards(self):
        return db.getAllCards()

    def hideCard(self, card_status, card_id):
        db.hideCard(card_status, card_id)

    def changeShelftime(self, month):
        db.changeShelftime(month)

    def get_user_status(self):
        return db.get_user_status()

    def password_is_valid(self, pwd):
        h = db.get_password()
        return bcrypt.checkpw(pwd.encode('utf-8'), h)

    # sends encrypted password to database
    @password_decorator
    def change_password(oldpwd, newpwd):
        salt = bcrypt.gensalt()
        hashed_pwd = bcrypt.hashpw(newpwd.encode('utf-8'), salt)
        db.change_password(hashed_pwd)

    def set_password(self, newpwd):
        salt = bcrypt.gensalt()
        hashed_pwd = bcrypt.hashpw(newpwd.encode('utf-8'), salt)
        db.change_password(hashed_pwd)
        self.set_password_state(1)

    def set_password_state(self, state):
        db.set_password_state(state)

    def get_password_state(self):
        return db.get_password_state()

    def get_password(self):
        return db.get_password()

    def get_email(self):
        return db.get_email()

    def create_user(self, email):
        db.create_user(email)

    def set_email(self, email):
        db.set_email(email)

    def resetdb(self):
        db.resetdb()

    def send_email(self):
        # conn = sqlite3.connect('ClipboardManager_DB.db')
        # cursor = conn.cursor()
        # records = cursor.execute("""SELECT email FROM user LIMIT 1""")
        # email = ''
        # for row in records:
        #     email = row[0]
        email = self.get_email()
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "yourclipboardmanager@gmail.com"
        os = platform.system()
        receiver_email = email
        # if os == 'Darwin':
        #     password = "ecqibpmoeknjxwbm"
        # elif os == 'Windows':
        #     password = "qourwmshfkltqnnc"

        password = "ecqibpmoeknjxwbm"
        temp = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

        self.set_password(temp)
        # conn = sqlite3.connect('ClipboardManager_DB.db')
        # cursor = conn.cursor()
        # salt = bcrypt.gensalt()
        # hashed_pwd = bcrypt.hashpw(temp.encode('utf-8'), salt)
        # cursor.execute("""UPDATE user SET password = (?) WHERE userID = 1""", (hashed_pwd,))
        # conn.commit()

        message = ("""\
    		Subject: Your temporary password.
    		This is your temporary password: {}. Please use this password to sign in and
    		remember to change password to your own.""".format(temp))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)


if __name__ == "__main__":
        # dao1 = DataAccessObject()
        # dao1.initializeUI()
        pass


