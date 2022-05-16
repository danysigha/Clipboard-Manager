from card import datetime,Card,uuid
import copy


class Folder(Card):

    numFolders = 0

    def __init__(self,folderName, cards=None):
        self.folderName = folderName
        self.folderID = uuid.uuid1().hex

        if cards is None:
            self.cards = []
        else:
            for element in cards:
                if not isinstance(element, Card):
                    raise Exception("element in list is not Card type")
            self.cards = cards

        #self.favorite = None

        Folder.numFolders+=1

    def addCard(self,card):
        #should we make folders duplicate protected?
        if card not in self.cards:
            self.cards.append(card)

    def removeCard(self,card):
        if card in self.cards:
            self.cards.remove(card)

    def filterByType(self, labelType):

        theCards=[]
        for card in self.cards:
           if  card.cardLabel==labelType:
               theCards.append(card)
        return theCards

    #returns the cards after the passed date object arguement
    def filterByDate(self,date):

        theCards=[]
        for card in self.cards:
           if  card.addedDate>=date:
               theCards.append(card)
        return theCards

    def sortByDateModified(self):

        #insertion sort
        theCards = copy.deepcopy(self.cards)
        if len(theCards)==1 or len(theCards)==0:
            return
        for i in range(1, len(theCards)):

         key = theCards[i]

         j = i-1
         while j >= 0 and key.modifiedDate<theCards[j].modifiedDate :
                theCards[j + 1] = theCards[j]
                j -= 1
         theCards[j + 1] = key

         return theCards

    def getHidden(self):
        theCards=[]
        for card in self.cards:
            if card.hideCard:
                theCards.append(card)
        return theCards


    def sortByDateAdded(self):

        theCards=[]
        for card in self.cards:
           if  card.cardLabel==labelType:
               theCards.append(card)
        return theCards

        #insertion sort
        theCards = copy.deepcopy(self.cards)
        if len(theCards)==1 or len(theCards)==0:
            return
        for i in range(1, len(theCards)):

         key = theCards[i]

         j = i-1
         while j >= 0 and key.addedDate<theCards[j].addedDate :
                theCards[j + 1] = theCards[j]
                j -= 1
         theCards[j + 1] = key

         return theCards

    @classmethod
    def getTotalFolders(cls):

        return cls.numFolders

    def __str__(self):
        string = "(" + self.folderID+") "+str(self.folderName)+":"+"["
        for card in self.cards:
           if  not card.hideCard:
               string+=str(card)+ ";" +"\n"
        string+="]"
        return  string

    def __del__(self):
        """
         self.folderName =None
         self.folderID = None
         self.cards = None
        """
