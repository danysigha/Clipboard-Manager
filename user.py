class User():
    def __init__(self, userID, password=None, currentCardID=None):
        self.userID = userID
        self._password = password
        self.currentCardID = currentCardID
        self._saltText = None
        self._pwdExist = False

    def setPassword(self, newPassword):
        self._password = newPassword
    # deleteExpiredCard should this be done in the user class?

    def unlock(self):
        pass #implemented by Tina