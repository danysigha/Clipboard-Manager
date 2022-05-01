import datetime
import uuid


class Card:

    def __init__(self, id, cardContent, cardCategory, addedDate, modifiedDate, cardFolder):
        # "make a UUID based on the host ID and current time" .hex removes dashes and
        # turns it into a string
        self.cardID = id
        self.cardContent = cardContent
        self.cardCategory = cardCategory
        self.addedDate = addedDate
        self.modifiedDate = modifiedDate
        self.cardFolder = cardFolder
        self.hideCard = False

    # getter functions

    def getID(self):
        return self.cardID

    def getAddedDate(self):
        return self.addedDate

    def getModifiedDate(self):
        return self.modifiedDate

    def getCardCategory(self):
        return self.cardCategory

    def getCardContent(self):
        return self.cardContent

    # setter functions
    def setCardCategory(self, e):

        if not isinstance(e, str):
            raise Exception("Card label must be str type")

        self.cardCategory = e
        self.modifiedDate = datetime.datetime.now()

    def setCardContent(self, e):
        if not isinstance(e, str):
            raise Exception("Card content must be str type")
        self.cardContent = e
        self.modifiedDate = datetime.datetime.now()

    def setCardFolder(folder):
        pass

    def setHidden(self, H):
        self.hideCard = H

    # delete card
    def __del__(self):
        # print("card deleted")
        # print(self)
        pass

    def __str__(self):
        string = "{ " + "card ID: " + str(self.cardID) + " , " + "date created: " + str(
            self.addedDate) + " , " + " last modified: " + str(self.modifiedDate) + ", " + "card content:" + "\"" + str(
            self.cardContent) + "\"" + "}"
        return string
