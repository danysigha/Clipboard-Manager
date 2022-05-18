from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, \
    QHBoxLayout, QLabel, QLineEdit, QScrollArea, QFrame, QWidget, QGridLayout, QVBoxLayout, \
    QDialog, QSizePolicy, QStyle, QStackedWidget, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize, QRect, QCoreApplication, QMetaObject, Qt, pyqtSlot
import icons
import grab_clipboard as grabClip
from PyQt5 import uic
import sys
import dao
import card_generator
import settings
import loginPage


class UI(QMainWindow):

    ALL_STATE = False
    FAVORITE_STATE = False
    TEXT_STATE = False
    IMAGE_STATE = False
    URL_STATE = False


    def __init__(self):
        super(UI, self).__init__()

        # load the UI
        uic.loadUi("new_main_window.ui", self)

        self.gridLayout2 = QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout2.setSpacing(0)
        self.gridLayout2.setObjectName(u"gridLayout_2")
        self.gridLayout2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout2.setHorizontalSpacing(10)
        self.gridLayout2.setVerticalSpacing(10)

        self.dao = dao.DataAccessor()
        self.cardMaker = card_generator.CardRenderer(self.gridLayout2, self.dao)

        self.menu = self.findChild(QGridLayout, "gridLayout")

        self.settings_button = self.findChild(QPushButton, "settings_button")
        self.settings_button.clicked.connect(self.openWindow)
        self.left_menu_frame = self.findChild(QFrame, "left_menu_frame")
        self.side_bar_button = self.findChild(QPushButton, "side_bar_button")
        self.side_bar_button.clicked.connect(self.hideMenu)
        self.all_cards = self.findChild(QPushButton, "all_cards")
        self.all_cards.clicked.connect(self.press_all)
        self.favorite_cards = self.findChild(QPushButton, "favorite_cards")
        self.favorite_cards.clicked.connect(self.favorite_it)
        self.text_cards = self.findChild(QPushButton, "text_cards")
        self.text_cards.clicked.connect(self.press_text)
        self.image_cards = self.findChild(QPushButton, "image_cards")
        self.image_cards.clicked.connect(self.press_image)
        self.link_cards = self.findChild(QPushButton, "link_cards")
        self.link_cards.clicked.connect(self.press_url)
        self.search_button = self.findChild(QPushButton, "search_button")
        self.search_button.clicked.connect(self.search_it)
        self.searchBar = self.findChild(QLineEdit, "lineEdit")
        self.searchBar.returnPressed.connect(self.search_it)


    def setState(self):
        for i in range(self.menu.count()):
            widget = self.menu.itemAt(i).widget()
            if widget.objectName() == "all_cards" and self.ALL_STATE:
                self.setfocus(widget)

            elif widget.objectName() == "favorite_cards" and self.FAVORITE_STATE:
                self.setfocus(widget)

            elif widget.objectName() == "text_cards" and self.TEXT_STATE:
                self.setfocus(widget)

            elif widget.objectName() == "image_cards" and self.IMAGE_STATE:
                self.setfocus(widget)

            elif widget.objectName() == "link_cards" and self.URL_STATE:
                self.setfocus(widget)

            elif widget.objectName() != "label_4":
                widget.setStyleSheet(u"QPushButton:hover{\n"
                             "background-color: rgba(255, 227, 251, 59);\n"
                             "}"
                              u"QPushButton{\n"
                                     "border: node;\n"
                                     "}")

    def setfocus(self, button):
        button.setStyleSheet(u"QPushButton{\n"
                             "  background-color: rgba(255, 227, 251, 59);\n"
                             "}"
                             u"QPushButton{\n"
                             "border: solid;\n"
                             "border-color: black;\n"
                              "border-width: 1px\n"
                             "}"
                             )

    def resetGrid(self):
        self.cardMaker._position = [0, 0, 1, 1]
        layout = self.gridLayout2
        for i in reversed(range(layout.count())):
            widgetToRemove = layout.itemAt(i).widget()
            # remove it from the layout list
            layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)
            widgetToRemove.deleteLater()

    def press_all(self):
        self.ALL_STATE = True
        self.FAVORITE_STATE = False
        self.TEXT_STATE = False
        self.IMAGE_STATE = False
        self.URL_STATE = False
        self.setState()
        self.resetGrid()
        self.cardMaker.numCheck = 1
        self.cardMaker.initializeUI(self.cardMaker._dao.getAllCards(), self.cardMaker._position)

    def press_text(self):
        self.ALL_STATE = False
        self.FAVORITE_STATE = False
        self.TEXT_STATE = True
        self.IMAGE_STATE = False
        self.URL_STATE = False
        self.setState()
        self.resetGrid()
        # print(self._cardMaker._position, 'in reset function after reset')
        self.cardMaker.numCheck = 2
        self.cardMaker.initializeUI(self.cardMaker._dao.getTextCards(), self.cardMaker._position)

    def press_image(self):
        self.ALL_STATE = False
        self.FAVORITE_STATE = False
        self.TEXT_STATE = False
        self.IMAGE_STATE = True
        self.URL_STATE = False
        self.setState()
        self.resetGrid()
        # print(self._cardMaker._position, 'in reset function after reset')
        self.cardMaker.numCheck = 3
        self.cardMaker.initializeUI(self.cardMaker._dao.getImageCards(), self.cardMaker._position)

    def press_url(self):
        self.ALL_STATE = False
        self.FAVORITE_STATE = False
        self.TEXT_STATE = False
        self.IMAGE_STATE = False
        self.URL_STATE = True
        self.setState()
        self.resetGrid()
       #print(self._cardMaker._position, 'in reset function after reset')
        self.cardMaker.numCheck = 4
        self.cardMaker.initializeUI(self.cardMaker._dao.getURLCards(), self.cardMaker._position)

    def search_it(self):

        search = self.lineEdit.text()
        if search:
            self.resetGrid()
            # print(self._cardMaker._position, 'in reset function after reset')
            self.cardMaker.numCheck = 5
            self.cardMaker.initializeUI(self.cardMaker._dao.getSearchCards(search), self.cardMaker._position)
        # ---------------new Changes ----------------------------------#
        # added the function for the favorite button

    # use for loop over a list of the states
    # use a function that takes the state that needs to change and loop over the rest to set to False
    def favorite_it(self):
        self.ALL_STATE = False
        self.FAVORITE_STATE = True
        self.TEXT_STATE = False
        self.IMAGE_STATE = False
        self.URL_STATE = False
        self.setState()
        self.resetGrid()
        # print(self._cardMaker._position, 'in reset function after reset')
        self.cardMaker.numCheck = 6
        self.cardMaker.initializeUI(self.cardMaker._dao.getFavoriteCards(), self.cardMaker._position)

    def hideMenu(self):
        if self.left_menu_frame.isVisible():
            self.left_menu_frame.hide()
        else:
            self.left_menu_frame.show()

    def openWindow(self):
        self.window = QStackedWidget()
        window1 = settings.MainSetting(self, self.dao, self.window)  # page 1
        window2 = settings.SetFirstPassword(self.dao, self.window)  # page 2
        window3 = settings.ChangePasswordPage(self.dao, self.window)  # page 4
        window4 = settings.ResetApplication(self.dao, self.window, self)  # page 5
        window5 = settings.DisablePasswordPage(self.dao, self.window)  # page 6
        # add the objects created above^ to the stack of screens
        self.window.addWidget(window1)
        self.window.addWidget(window2)
        self.window.addWidget(window3)
        self.window.addWidget(window4)
        self.window.addWidget(window5)
        self.window.setFixedHeight(493)
        self.window.setFixedWidth(370)
        self.window.show()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UI()
    ui.cardMaker.initializeUI(ui.dao.getAllCards())
    gc = grabClip.ClipboardManager(ui.cardMaker, ui.dao)
    gc.manage_clip()
    widget = QStackedWidget()
    window1 = loginPage.WelcomeScreen(ui.dao, widget, ui)  # page 1
    window2 = loginPage.NewUser(ui.dao, widget, ui)
    window3 = loginPage.WelcomeScreenPasswordPage(ui.dao, widget, ui)  # page 1
    widget.addWidget(window1)
    widget.addWidget(window2)
    widget.addWidget(window3)
    widget.setFixedHeight(493)
    widget.setFixedWidth(370)
    widget.show()

    sys.exit(app.exec_())
