import datetime
import uuid


class Card:

    def __init__(self, id, cardContent, cardCategory, addedDate, modifiedDate, cardFolder, hideCard=False):
        # "make a UUID based on the host ID and current time" .hex removes dashes and
        # turns it into a string
        self.cardID = id
        self.cardContent = cardContent
        self.cardCategory = cardCategory
        self.addedDate = addedDate
        self.modifiedDate = modifiedDate
        self.cardFolder = cardFolder
        if hideCard == 0:
            self.hideCard = False
        elif hideCard == 1:
            self.hideCard = True
        else:
            self.hideCard = hideCard

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
        string = "{\n" + "card ID: " + str(self.cardID) + ", " + "\ncard content: " + "\"" + str(
            self.cardContent) + "\"" + ", " + "\ncard type: " + str(
            self.cardCategory) + " , " + "\ndate created: " + str(
            self.addedDate) + " , " + "\nlast modified: " + str(self.modifiedDate) + "\nfolder ID: " + str(
            self.cardFolder) + " , " + "\nHidden: " + str(self.hideCard) + "\n}"
        return string
