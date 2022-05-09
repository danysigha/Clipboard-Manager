import sqlite3
import card
import bcrypt
import platform
import smtplib
import ssl
import string
import random
import clipboardManager_DB as db
from email.message import EmailMessage

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
    def storeCard(self, card_id, content, dataType, hideCard, favoriteCard):
        db.addCard(1, card_id, content, dataType, hideCard, favoriteCard)
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

    def getTextCards(self):
        return db.getTextCards()

    def getImageCards(self):
        return db.getImageCards()

    def getURLCards(self):
        return db.getURLCards()

    def hideCard(self, card_status, card_id):
        db.hideCard(card_status, card_id)

    def getFavoriteCards(self):
        return db.getFavoriteCards()

    def favoriteCard(self, card_id, favorite_status):
        db.favoriteCard(card_id, favorite_status)

    def getSearchCards(self, search):
        return db.getSearchCards(search)

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
        sender_email = "yourclipboardmanager@gmail.com"
        receiver_email = self.get_email()
        os = platform.system()
        if os == 'Darwin':
            password = "ecqibpmoeknjxwbm"
        elif os == 'Windows':
            password = "qourwmshfkltqnnc"

        
        temp = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

        self.set_password(temp)
   

        plainText = ("""This is your temporary password: {}. Please use this password to sign in and
    		remember to change password to your own.""".format(temp))


        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        msg = EmailMessage()

        message = f'{plainText}\n'
        msg.set_content(message)
        msg['Subject'] = "Your temporary password."
        msg['From'] = sender_email
        msg['To'] = receiver_email
        server.send_message(msg)


if __name__ == "__main__":
        # dao1 = DataAccessObject()
        # dao1.initializeUI()
        pass


