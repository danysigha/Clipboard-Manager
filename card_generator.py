from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QLabel, QMenu, QMainWindow
from PyQt5.QtGui import QPixmap
# from PyQt5 import QtCore
import dao
import card
import test_2
import grab_clipboard as grabClip


class CardRenderer:

    class CardObject:
        def __init__(self, parent, position):
            self.card_data = None
            self.label = QLabel()
            self.parent = parent
            self._position = position

        def addToInterface(self, ID, content, category, addedDate, modifiedDate, folderID):
            # self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            # print('before', self._position)
            self.card_data = card.Card(ID, content, category, addedDate, modifiedDate, folderID)

            self.label.setMinimumSize(QSize(200, 150))
            self.label.setMaximumSize(QSize(200, 150))
            self.label.setStyleSheet(u"*{\n"
                                "border:4px solid black;\n"
                                "  border-radius: 15px;\n"
                                "  padding: 15px;\n"
                                # "  box-shadow: 0px 0px 20px 20px black;\n"
                                "  background-color: white;\n"
                                "}")
            self.label.setTextInteractionFlags(Qt.TextBrowserInteraction)

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

            elif category == 'Image':
                self.label.setPixmap(content)

            self.label.setContextMenuPolicy(Qt.CustomContextMenu)
            # self.label.customContextMenuRequested.connect(self.customMenuEvent)
            self.label.customContextMenuRequested.connect(
                lambda pos, child=self.label: self.customMenuEvent(pos, child))

            self.parent.addWidget(self.label, self._position[0], self._position[1], self._position[2], self._position[3],
                                  Qt.AlignTop)

            if (self._position[1] + 1) % 3 == 0:
                self._position[0] += 1
                self._position[1] = 0
            else:
                self._position[1] += 1

            # print('after', self._position)

        def customMenuEvent(self, eventPosition, child):
            # child = self._main_window.childAt(self._main_window.sender().mapTo(self._main_window, eventPosition))
            # print(child)
            contextMenu = QMenu()
            delCard = contextMenu.addAction("Delete")
            hideCard = contextMenu.addAction("Hide")
            # quitAct = contextMenu.addAction("Quit")
            action = contextMenu.exec_(self.label.mapToGlobal(eventPosition))

            if action == delCard:
                dao.DataAccessor().deleteCard(int(self.card_data.cardID))
                self.parent.removeWidget(self.label)
                # self.label.hide()
                self.label.deleteLater()

            if action == hideCard:
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

                action = contextMenu.actions()[1]
                action.setText("Show")

                self.label.setStyleSheet(u"*{\n"
                                         "border:4px solid black;\n"
                                         "  border-radius: 15px;\n"
                                         "  padding: 15px;\n"
                                         # "  box-shadow: 0px 0px 20px 20px black;\n"
                                         "  background-color: white;\n"
                                         "color: white;\n"
                                         "}")
                self.label.setTextInteractionFlags(Qt.NoTextInteraction)

                contextMenu.exec_(self.label.mapToGlobal(eventPosition))
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

    def __init__(self, parent):  # - content - to add
        # super(newCopy, self).__init__(parent)
        # self.label = QLabel()
        # self.name = str(id)
        self.parent = parent

        self._row = 0
        self._column = 0
        self._rowSpan = 1
        self._columnSpan = 1
        self._position = [self._row, self._column, self._rowSpan, self._columnSpan]

        # self.label.setObjectName(self.name)

    # def grabNewItem(self):
    #     return self.label

    def initializeUI(self, content):
        # card_list = dict()
        for i in content:
            new_card = self.CardObject(self.parent, self._position)
            if i[2] == "Image":
                pixmap = QPixmap(i[1])
                pixmap4 = pixmap.scaled(150, 100, Qt.KeepAspectRatio)
                new_card.addToInterface(i[0], pixmap4, i[2], i[3], i[4], i[5])
            elif i[2] == "Text":
                new_card.addToInterface(i[0], i[1], i[2], i[3], i[4], i[5])
        # print(self._position)
