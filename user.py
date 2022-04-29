class User():
    def __init__(self, userID, password=None, currentCardID=None):
        self.userID = userID
        self._password = password
        self.currentCardID = currentCardID
<<<<<<< HEAD
        self._saltText = None
        self._pwdExist = False
=======
        self.num_of_cards = 0
        self.num_of_folders = 0
>>>>>>> 093e10f1e1585f3356ebb9403d6c9ab8b68c9353

    def setPassword(self, newPassword):
        self._password = newPassword
    # deleteExpiredCard should this be done in the user class?

    def unlock(self):
        pass #implemented by Tina
