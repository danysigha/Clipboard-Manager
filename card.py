

class Card:

    def __init__(self, id, cardContent, cardCategory, hideCard=False, favoriteCard =False):
        self._cardId = id
        self._cardContent = cardContent
        self._cardCategory = cardCategory
        if hideCard == 0:
            self._hideCard = False
        elif hideCard == 1:
            self._hideCard = True
        else:
            self._hideCard = hideCard

        if favoriteCard == 0:
            self._favoriteCard = False
        elif favoriteCard == 1:
            self._favoriteCard = True
        else:
            self._favoriteCard = favoriteCard

    def getId(self):
        return self._cardId

    def getCategory(self):
        return self._cardCategory

    def getContent(self):
        return self._cardContent

    def getViewStatus(self):
        return self._hideCard

    def getFavoriteStatus(self):
        return self._favoriteCard

    def setCategory(self, e):

        if not isinstance(e, str):
            raise Exception("Card label must be str type")

        self._cardCategory = e

    def setContent(self, e):
        if not isinstance(e, str):
            raise Exception("Card content must be str type")
        self._cardContent = e

    def setHidden(self, H):
        self._hideCard = H

    def setId(self, id):
        self._cardId = id

    def setFavorite(self, newStatus):
        self._favoriteCard = newStatus

    def __str__(self):
        string = "{\n" + "card ID: " + str(self._cardId) + ", " + "\ncard content: " + "\"" + str(
            self._cardContent) + "\"" + ", " + "\ncard type: " + str(
            self._cardCategory) + " , " + "\nHidden: " + str(self._hideCard) + "\nFavorite: " + str(self._favoriteCard)\
                 + "\n}"
        return string
