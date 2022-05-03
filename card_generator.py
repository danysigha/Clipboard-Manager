from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QLabel, QMenu, QMainWindow
from PyQt5.QtGui import QPixmap
# from PyQt5 import QtCore
import uuid
# import dao
import card
import test_2
import grab_clipboard as grabClip


class CardRenderer:

    def __init__(self, parent, dao):  # - content - to add
        # super(newCopy, self).__init__(parent)
        # self.label = QLabel()
        # self.name = str(id)
        self.parent = parent
        self._dao = dao
        self._row = 0
        self._column = 0
        self._rowSpan = 1
        self._columnSpan = 1
        self._position = [self._row, self._column, self._rowSpan, self._columnSpan] # not updated when we delete cards

        # self.label.setObjectName(self.name)

    # def grabNewItem(self):
    #     return self.label

    def initializeUI(self, content, position=None):
        # card_list = dict()
        if position == None: # if not position
            position = self._position
        print(self._position, 'in initialize function before we initialized')

        for i in content:
            new_card = CardObject(self.parent, position, self._dao, self)
            if i[2] == "Image":
                pixmap = QPixmap(i[1])
                pixmap4 = pixmap.scaled(150, 100, Qt.KeepAspectRatio)
                new_card.addToInterface(i[0], pixmap4, i[2], i[3], i[4], i[5], i[6])
            elif i[2] == "Text":
                new_card.addToInterface(i[0], i[1], i[2], i[3], i[4], i[5], i[6])

        print(position, 'in initialize function after we initialized')
        # print(self._position)


class CardObject():
    def __init__(self, parent, position, dao, cardMaker):
        self.card_data = None
        self.label = QLabel()
        self._dao = dao
        self._cardMaker = cardMaker
        # self.id = uuid.uuid1().hex
        self.parent = parent
        self._position = position

    def addToInterface(self, ID, content, category, addedDate, modifiedDate, folderID, hideCard):
        # self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        # print('before', self._position)
        self.card_data = card.Card(ID, content, category, addedDate, modifiedDate, folderID, hideCard)
        print(self.card_data)
        print(self._position, 'in add function before we increment')
        self.label.setMinimumSize(QSize(200, 150))
        self.label.setMaximumSize(QSize(200, 150))

        self.label.setStyleSheet(u"*{\n"
                                 "border:4px solid black;\n"
                                 "  border-radius: 15px;\n"
                                 "  padding: 15px;\n"
                                 "  background-color: white;\n"
                                 "color: black;\n"
                                 "}")
        self.label.setWordWrap(True)
        self.label.setTextFormat(Qt.RichText)
        self.label.setOpenExternalLinks(True)

        if category == 'Text':
            # self.label.setTextFormat(Qt.RichText)
            # self.label.setOpenExternalLinks(True)
            # valid = validators.url(copy1)
            # if valid:
            #     self.addCopy().setText("<a href={}>{}</a>".format(copy1, copy1))
            # else:
            #
            #     self.addCopy().setText(copy1)
            #     self.addCopy().adjustSize()
            self.label.setText(content)
            if self.card_data.hideCard:
                self.label.setStyleSheet(u"*{\n"
                                         "border:4px solid black;\n"
                                         "  border-radius: 15px;\n"
                                         "  padding: 15px;\n"
                                         # "  box-shadow: 0px 0px 20px 20px black;\n"
                                         "  background-color: white;\n"
                                         "color: white;\n"
                                         "}")
            else:
                self.label.setStyleSheet(u"*{\n"
                                         "border:4px solid black;\n"
                                         "  border-radius: 15px;\n"
                                         "  padding: 15px;\n"
                                         # "  box-shadow: 0px 0px 20px 20px black;\n"
                                         "  background-color: white;\n"
                                         "color: black;\n"
                                         "}")
                self.label.setTextInteractionFlags(Qt.TextBrowserInteraction)


        elif category == 'Image':
            if self.card_data.hideCard:

                if self.card_data.cardCategory == "Image":
                    # self.hideImage()
                    pixmap = QPixmap()
                    pixmap.fill(Qt.white)
                    self.label.setPixmap(pixmap)
            else:
                self.label.setPixmap(content)

        self.label.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.label.customContextMenuRequested.connect(self.customMenuEvent)
        self.label.customContextMenuRequested.connect(
            lambda pos, child=self.label: self.customMenuEvent(pos, child))

        self.parent.addWidget(self.label, self._position[0], self._position[1], self._position[2],
                              self._position[3],
                              Qt.AlignTop)

        if (self._position[1] + 1) % 3 == 0:
            self._position[0] += 1
            self._position[1] = 0
        else:
            self._position[1] += 1

        # print('after', self._position)

    # def hideImage(self):

    def reset(self):
        layout = self.parent
        for i in reversed(range(layout.count())):
            widgetToRemove = layout.itemAt(i).widget()
            # remove it from the layout list
            layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)
            widgetToRemove.deleteLater()

        print(self._position, 'in reset function after reset')
        # CardRenderer(self.parent, self._dao).initializeUI(self._dao.getAllCards(), self._position)
        self._cardMaker.initializeUI(self._dao.getAllCards(), self._cardMaker._position)


        # self._cardMaker(self.parent, self._dao).initializeUI(self._dao.getAllCards())


    def customMenuEvent(self, eventPosition, child):
        # child = self._main_window.childAt(self._main_window.sender().mapTo(self._main_window, eventPosition))
        # print(child)
        contextMenu = QMenu()
        delCard = contextMenu.addAction("Delete")
        hideCard = contextMenu.addAction("Toggle visibility")
        # quitAct = contextMenu.addAction("Quit")
        action = contextMenu.exec_(self.label.mapToGlobal(eventPosition))

        if action == delCard:
            self._dao.deleteCard(int(self.card_data.cardID))
            self._cardMaker._position = [0, 0, 1, 1]
            self.reset()

            # if (self._position[1] % 3) == 0:
            #     self._position[0] -= 1
            #     self._position[1] = 2
            # else:
            #     self._position[1] -= 1
            #
            # self.parent.removeWidget(self.label)
            # # self.label.hide()
            # self.label.deleteLater()

        if action == hideCard:
            if self.card_data.hideCard == False:

                self._dao.hideCard(1, self.card_data.cardID)

                if self.card_data.cardCategory == "Image":
                    # self.hideImage()
                    pixmap = QPixmap()
                    pixmap.fill(Qt.white)
                    self.label.setPixmap(pixmap)

                else:
                    self.label.setStyleSheet(u"*{\n"
                                             "border:4px solid black;\n"
                                             "  border-radius: 15px;\n"
                                             "  padding: 15px;\n"
                                             # "  box-shadow: 0px 0px 20px 20px black;\n"
                                             "  background-color: white;\n"
                                             "color: white;\n"
                                             "}")
                self.label.setTextInteractionFlags(Qt.NoTextInteraction)

                # action = contextMenu.actions()[1]
                # action.setText("Show")
                self.card_data.hideCard = True
                # contextMenu.exec_(self.label.mapToGlobal(eventPosition)) #just pops up new menu - does not work

            else:

                self._dao.hideCard(0, self.card_data.cardID)

                if self.card_data.cardCategory == "Image":
                    pixmap = QPixmap(self.card_data.cardContent)
                    self.label.setPixmap(pixmap)

                else:
                    self.label.setStyleSheet(u"*{\n"
                                             "border:4px solid black;\n"
                                             "  border-radius: 15px;\n"
                                             "  padding: 15px;\n"
                                             # "  box-shadow: 0px 0px 20px 20px black;\n"
                                             "  background-color: white;\n"
                                             "color: black;\n"
                                             "}")
                    self.label.setTextInteractionFlags(Qt.TextBrowserInteraction)

                # action = contextMenu.actions()[1]
                # action.setText("Hide")
                self.card_data.hideCard = False
                # self.label.setTextInteractionFlags(Qt.TextBrowserInteraction)
                # contextMenu.exec_(self.label.mapToGlobal(eventPosition))

            # add setFavorite option
            # update in db
            # if hideCard.text() == 'Show'
            # else:
            # print(hideCard)
            # contextMenu.removeAction(hideCard)
            # hideCard.setText('Show')
            # contextMenu.addAction("Show")
            # hideCard.setText('Show')
            # hideCard = contextMenu.addAction("Show")
            # if hide self.cardObject.hideCard == false:

            # contextMenu.parent = None

            # else
            # self.label.setStyleSheet(u"*{\n"
            #                          "border:4px solid black;\n"
            #                          "  border-radius: 15px;\n"
            #                          "  padding: 15px;\n"
            #                          # "  box-shadow: 0px 0px 20px 20px black;\n"
            #                          "  background-color: white;\n"
            #                          "}")
            # self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # if action == quitAct:
        #     QMainWindow.close()