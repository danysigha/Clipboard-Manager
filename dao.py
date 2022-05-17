import bcrypt
import platform
import smtplib
import ssl
import string
import random
import clipboardManager_DB as db


class PasswordDecorator:
    """
    This is a class for the password decorator.

    This class is a decorator for functions that requires password validation before being
    processed.

    Attributes
    function (function): the function to be called after password is checked

    """

    def __init__(self, function):
        """
        The constructor for the PasswordDecorator class.

        Parameters:
        function (function): the function to be called after password is checked

        """

        self.function = function

    def passwordIsValid(pwd):
        """
        The function to check password validity.
        Parameters:

        pwd(String): stores the password entered by user to be compared to current
        password stored
        """

        h = db.get_password()
        return bcrypt.checkpw(pwd.encode('utf-8'), h)

    def __call__(self, *args, **kwargs):
        """
        The wrapper function to run function if password is valid.

        """

        pwd = args[0]

        if self.passwordIsValid(pwd):
            self.function(*args, **kwargs)
            result = True
        else:
            result = False

        return result


class DataAccessor:
    """
    Data Accessor class that handles requests to the database

    """

    # decryption takes place here
    # UI grabs the decryption key from user and pass to data access object
    def storeCard(self, cardId, content, dataType, hideCard, favoriteCard):
        db.addCard(1, cardId, content, dataType, hideCard, favoriteCard)

    def deleteCard(self, id):
        """
        deletes card from the database

        Parameters:
        id (str): key to find the card in the database

        """

        db.deleteCard(id)

    def getAllCards(self):
        """
        returns all cards in the database

        """

        return db.getAllCards()

    def getTextCards(self):
        """
        returns all cards with cardCategory 'Text'

        """

        return db.getTextCards()

    def getImageCards(self):
        """
        returns all cards with cardCategory 'Image'

        """

        return db.getImageCards()

    def getURLCards(self):
        """
        returns all cards with cardCategory 'URL'

        """

        return db.getURLCards()

    def hideCard(self, cardStatus, cardId):
        """
        sets the hidden status of the card true or false

        Parameters:
        cardStatus (int): desired card status, value is 1 or 0 indicating true or false respectively
        CardId (str): key to find the card in the database

        """

        db.hideCard(card_status, card_id)

    def getFavoriteCards(self):
        """
        returns all cards from the db that are favorited

        """
        return db.getFavoriteCards()

    def favoriteCard(self, cardId, favoriteStatus):
        """
        sets the favorite status of the card to true or false

        Parameters:
        favoriteStatus (int): desired card status, value is 1 or 0 indicating true or false respectively
        CardId (str): key to find the card in the database

        """

        db.favoriteCard(card_id, favorite_status)

    def getSearchCards(self, search):
        """
        returns all cards that satisfy the search parameter

        Parameters:
        search (str): the search query

        """

        return db.getSearchCards(search)
    

    def getUserStatus(self):
        """
        Returns the status of the user

        """

        return db.getUserStatus()

    def passwordIsValid(self, pwd):
        """
        The function to check password validity.

        Parameters:
        pwd(String): stores the password entered by user to be compared to current
        password stored

        """

        h = db.getPassword()
        return bcrypt.checkpw(pwd.encode('utf-8'), h)

    # sends encrypted password to database
    @PasswordDecorator
    def changePassword(oldpwd, newpwd):
        """
        Encrypts and changes the password stored in the database

        Parameters:
        newpwd(String): the new password that will be encrypted and stored
        oldpwd(String): the old password that will be checked for validity before storing
        new password

        """

        salt = bcrypt.gensalt()
        hashed_pwd = bcrypt.hashpw(newpwd.encode('utf-8'), salt)
        db.changePassword(hashed_pwd)

    def setPassword(self, newpwd):
        """
        Encrypts and stores the new password in the database

        Parameters:
        newpwd(String): the password that will be encrypted and stored

        """

        salt = bcrypt.gensalt()
        hashed_pwd = bcrypt.hashpw(newpwd.encode('utf-8'), salt)
        db.change_password(hashed_pwd)
        self.set_password_state(1)

    def setPasswordState(self, state):
        """
        sets the state of the password

        Parameters:
        state(boolean): the current state of the password

        """

        db.set_password_state(state)

    def getPasswordState(self):
        """
        Returns the state of the password.

        Returns:
        state(boolean): the current state of the password

        """

        return db.getPasswordState()

    def getPassword(self):
        """
        Returns the current encrypted password obtained from database.

        Returns:
        password(binary): the current encrypted password

        """

        return db.getPassword()

    def getEmail(self):
        """
        Returns the email stored in the database.

        Returns:
        email(string): the email stored in the database

        """

        return db.getEmail()

    def createUser(self, email):
        db.createUser(email)

    def setEmail(self, email):
        """
        Sends the email to the database.
        """

        db.set_email(email)

    def resetDb(self):
        """
        Erases all contents in database.

        """

        db.resetDb()

    def sendEmail(self):
        """
        The function to send temporary password to user email.

        """

        email = self.getEmail()
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        senderEmail = "yourclipboardmanager@gmail.com"
        os = platform.system()
        receiverEmail = email

        password = "ecqibpmoeknjxwbm"
        temp = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

        self.setPassword(temp)

        message = ("""\
            Subject: Your temporary password.
            This is your temporary password: {}. Please use this password to sign in and
            remember to change password to your own.""".format(temp))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtpServer, port, context=context) as server:
            server.login(senderEmail, password)
            server.sendmail(senderEmail, receiverEmail, message)
