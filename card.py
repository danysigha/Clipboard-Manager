import datetime
import uuid


class Card:

    def __init__(self, id, cardContent, cardCategory, hideCard=False, favoriteCard =False):
        """ Creates card object with the given parameters"""
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
        """returns card Id"""
        return self.cardId

    def getAddedDate(self):
        """returns card creation date"""
        return self.addedDate

    def getCardCategory(self):
        """returns the type of card content"""
        return self.cardCategory

    def getCardContent(self):
        """returns the card content"""
        return self.cardContent

   
    def setCardCategory(self, e):
        
        """
        sets card content to passed argument
        
        parameters:
            e (str): the value to set the card category to
        """

        

        if not isinstance(e, str):
            raise Exception("Card label must be str type")

        self.cardCategory = e


    def setCardContent(self, e):
        """
        sets card content to passed argument
        
        parameters:
            e (str): the value to set the card content to
        """
        if not isinstance(e, str):
            raise Exception("Card content must be str type")
        self.cardContent = e


    def setHidden(self, H):
        """
        sets card object hidden status
        
        parameters:
            H (bool): the value to set the hideCard to
        """
        self._hideCard = H

   

    def __str__(self):
        """returns string representation for card object"""
        
        string = "{\n" + "card ID: " + str(self._cardId) + ", " + "\ncard content: " + "\"" + str(
            self._cardContent) + "\"" + ", " + "\ncard type: " + str(
            self._cardCategory) + " , " + "\ndate created: " + str(
            self._addedDate) + " , " + "\nHidden: " + str(self._hideCard) +  "\n}"
        return string
