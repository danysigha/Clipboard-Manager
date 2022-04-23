import datetime
import uuid

class Card:


    def __init__(self,cardCategory,cardContent):

        # "make a UUID based on the host ID and current time" .hex removes dashes and
        #turns it into a string
        self.cardID= uuid.uuid1().hex
        self.addedDate = datetime.datetime.now()
        self.modifiedDate = datetime.datetime.now()
        self.cardCategory = cardCategory
        self.cardContent = cardContent
        self.cardFolder ="default"
        self.hideCard = False

    #getter functions

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
    #setter functions
    def setCardCategory(self,e):

        if not isinstance(e,str):
            raise Exception("Card label must be str type")

        self.cardCategory = e
        self.modifiedDate =datetime.datetime.now()

    def setCardContent(self,e):
        if not isinstance(e,str):
            raise Exception("Card content must be str type")
        self.cardContent = e
        self.modifiedDate =datetime.datetime.now()

    def setCardFolder(folder):
        pass

    def setHidden(self,H):
        self.hideCard = H


    #delete card
    def __del__(self):
        print("card deleted")

    def __str__(self):

        string = "{ " + "card ID: " + self.cardID+ " , "  + "date created: " + str(self.addedDate) + " , " + " last modified: " + str(self.modifiedDate) + ", " + "label:"  + str(self.cardLabel) + " , " + "card content:" + "\""+ str(self.cardContent)+ "\""+"}"
        return string
