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
    def __init__(self):
        super(UI, self).__init__()

        # load the UI
        uic.loadUi("new_main_window.ui", self)

        self.gridLayout2 = QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout2.setSpacing(0)
        self.gridLayout2.setObjectName(u"gridLayout_2")
        self.gridLayout2.setContentsMargins(0, 0, 0, 0)

        self.dao = dao.DataAccessor()
        self.cardMaker = card_generator.CardRenderer(self.gridLayout2, self.dao)

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
        self.resetGrid()
        self.cardMaker.numCheck = 1
        self.cardMaker.initializeUI(self.cardMaker._dao.getAllCards(), self.cardMaker._position)

    def press_text(self):
        self.resetGrid()
        # print(self._cardMaker._position, 'in reset function after reset')
        self.cardMaker.numCheck = 2
        self.cardMaker.initializeUI(self.cardMaker._dao.getTextCards(), self.cardMaker._position)

    def press_image(self):
        self.resetGrid()
        # print(self._cardMaker._position, 'in reset function after reset')
        self.cardMaker.numCheck = 3
        self.cardMaker.initializeUI(self.cardMaker._dao.getImageCards(), self.cardMaker._position)

    def press_url(self):
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

    def favorite_it(self):
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
        window1 = settings.mainSetting(self, self.dao, self.window)  # page 1
        window2 = settings.setPassword(self.dao, self.window)  # page 2
        window3 = settings.shelftime(self.dao, self.window)  # page 3
        window4 = settings.currentPasswordPage(self.dao, self.window)  # page 4
        window5 = settings.resetApplication(self.dao, self.window, self)  # page 5
        # add the objects created above^ to the stack of screens
        self.window.addWidget(window1)
        self.window.addWidget(window2)
        self.window.addWidget(window3)
        self.window.addWidget(window4)
        self.window.addWidget(window5)
        self.window.setFixedHeight(493)
        self.window.setFixedWidth(370)

        qr = self.window.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.window.move(qr.topLeft())
        # show the widget
        self.window.show()
        self.hide()

    # def setupUi(self, MainWindow):
    #     if not MainWindow.objectName():
    #         MainWindow.setObjectName(u"Clippy")
    #     MainWindow.resize(831, 800)
    #     MainWindow.setStyleSheet(u"*{\n"
    #                              "border: none;\n"
    #                              "}")
    #     self.centralwidget = QWidget(MainWindow)
    #     self.centralwidget.setObjectName(u"centralwidget")
    #     self.horizontalLayout = QHBoxLayout(self.centralwidget)
    #     self.horizontalLayout.setSpacing(0)
    #     self.horizontalLayout.setObjectName(u"horizontalLayout")
    #     self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
    #     self.left_menu_frame = QFrame(self.centralwidget)
    #     self.left_menu_frame.setObjectName(u"left_menu_frame")
    #     self.left_menu_frame.setMinimumSize(QSize(200, 0))
    #     self.left_menu_frame.setMaximumSize(QSize(20, 16777215))
    #     self.left_menu_frame.setFrameShape(QFrame.NoFrame)
    #     self.left_menu_frame.setFrameShadow(QFrame.Raised)
    #     self.horizontalLayout_5 = QHBoxLayout(self.left_menu_frame)
    #     self.horizontalLayout_5.setSpacing(0)
    #     self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
    #     self.horizontalLayout_5.setContentsMargins(0, 12, 0, 0)
    #     self.scrollArea = QScrollArea(self.left_menu_frame)
    #     self.scrollArea.setObjectName(u"scrollArea")
    #
    #     self.scrollArea.setWidgetResizable(True)
    #     self.scrollAreaWidgetContents = QWidget()
    #     self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
    #     self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 200, 788))
    #     self.scrollAreaWidgetContents.setMinimumSize(QSize(100, 0))
    #     self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
    #     self.gridLayout.setSpacing(0)
    #     self.gridLayout.setObjectName(u"gridLayout")
    #     self.gridLayout.setContentsMargins(0, 0, 0, 0)
    #     self.folder_1_cards = QPushButton(self.scrollAreaWidgetContents)
    #     self.folder_1_cards.setObjectName(u"folder_1_cards")
    #     icon = QIcon()
    #     icon.addFile(u":/icons/Icons/folder_white_24dp.svg", QSize(), QIcon.Normal, QIcon.Off)
    #     self.folder_1_cards.setIcon(icon)
    #     self.folder_1_cards.setIconSize(QSize(30, 30))
    #
    #     self.gridLayout.addWidget(self.folder_1_cards, 8, 0, 1, 1)
    #
    #     self.label_9 = QLabel(self.scrollAreaWidgetContents)
    #     self.label_9.setObjectName(u"label_9")
    #
    #     self.gridLayout.addWidget(self.label_9, 10, 1, 1, 1, Qt.AlignLeft)
    #
    #     self.label = QLabel(self.scrollAreaWidgetContents)
    #     self.label.setObjectName(u"label")
    #     font = QFont()
    #     font.setPointSize(14)
    #     self.label.setFont(font)
    #     self.label.setTextFormat(Qt.AutoText)
    #
    #     self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
    #
    #     self.link_cards = QPushButton(self.scrollAreaWidgetContents)
    #     self.link_cards.setObjectName(u"link_cards")
    #     icon1 = QIcon()
    #     icon1.addFile(u":/icons/Icons/link_white_24dp.svg", QSize(), QIcon.Normal, QIcon.Off)
    #     self.link_cards.setIcon(icon1)
    #     self.link_cards.setIconSize(QSize(30, 30))
    #
    #     self.gridLayout.addWidget(self.link_cards, 6, 0, 1, 1)
    #
    #     self.gif_cards = QPushButton(self.scrollAreaWidgetContents)
    #     self.gif_cards.setObjectName(u"gif_cards")
    #     icon2 = QIcon()
    #     icon2.addFile(u":/icons/Icons/gif_white_24dp.svg", QSize(), QIcon.Normal, QIcon.Off)
    #     self.gif_cards.setIcon(icon2)
    #     self.gif_cards.setIconSize(QSize(30, 30))
    #
    #     self.gridLayout.addWidget(self.gif_cards, 2, 0, 1, 1)
    #
    #     self.label_7 = QLabel(self.scrollAreaWidgetContents)
    #     self.label_7.setObjectName(u"label_7")
    #
    #     self.gridLayout.addWidget(self.label_7, 6, 1, 1, 1, Qt.AlignLeft)
    #
    #     self.label_6 = QLabel(self.scrollAreaWidgetContents)
    #     self.label_6.setObjectName(u"label_6")
    #     self.label_6.setMargin(0)
    #
    #     self.gridLayout.addWidget(self.label_6, 4, 1, 1, 1, Qt.AlignLeft)
    #
    #     self.label_11 = QLabel(self.scrollAreaWidgetContents)
    #     self.label_11.setObjectName(u"label_11")
    #     self.label_11.setMaximumSize(QSize(16777215, 60))
    #     self.label_11.setMargin(20)
    #
    #     self.gridLayout.addWidget(self.label_11, 7, 0, 1, 2)
    #
    #     self.all_cards = QPushButton(self.scrollAreaWidgetContents)
    #     self.all_cards.setObjectName(u"all_cards")
    #
    #     icon3 = QIcon()
    #     icon3.addFile(u":/icons/Icons/style_white_24dp.svg", QSize(), QIcon.Normal, QIcon.Off)
    #     self.all_cards.setIcon(icon3)
    #     self.all_cards.setIconSize(QSize(30, 30))
    #
    #     self.gridLayout.addWidget(self.all_cards, 0, 0, 1, 1)
    #
    #     self.label_14 = QLabel(self.scrollAreaWidgetContents)
    #     self.label_14.setObjectName(u"label_14")
    #
    #     self.gridLayout.addWidget(self.label_14, 12, 1, 1, 1, Qt.AlignLeft)
    #
    #     self.app_1_cards = QPushButton(self.scrollAreaWidgetContents)
    #     self.app_1_cards.setObjectName(u"app_1_cards")
    #     icon4 = QIcon()
    #     icon4.addFile(u":/icons/Icons/category_white_24dp.svg", QSize(), QIcon.Normal, QIcon.Off)
    #     self.app_1_cards.setIcon(icon4)
    #     self.app_1_cards.setIconSize(QSize(30, 30))
    #
    #     self.gridLayout.addWidget(self.app_1_cards, 12, 0, 1, 1)
    #
    #     self.label_12 = QLabel(self.scrollAreaWidgetContents)
    #     self.label_12.setObjectName(u"label_12")
    #
    #     self.gridLayout.addWidget(self.label_12, 13, 1, 1, 1, Qt.AlignLeft)
    #
    #     self.favorite_cards = QPushButton(self.scrollAreaWidgetContents)
    #     self.favorite_cards.setObjectName(u"favorite_cards")
    #     icon5 = QIcon()
    #     icon5.addFile(u":/icons/Icons/favorite_white_24dp.svg", QSize(), QIcon.Normal, QIcon.Off)
    #     self.favorite_cards.setIcon(icon5)
    #     self.favorite_cards.setIconSize(QSize(30, 30))
    #
    #     self.gridLayout.addWidget(self.favorite_cards, 1, 0, 1, 1)
    #
    #     self.label_4 = QLabel(self.scrollAreaWidgetContents)
    #     self.label_4.setObjectName(u"label_4")
    #     self.label_4.setMaximumSize(QSize(16777215, 60))
    #     self.label_4.setMargin(20)
    #
    #     self.gridLayout.addWidget(self.label_4, 3, 0, 1, 2)
    #
    #     self.label_3 = QLabel(self.scrollAreaWidgetContents)
    #     self.label_3.setObjectName(u"label_3")
    #     self.label_3.setFont(font)
    #
    #     self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
    #
    #     self.label_10 = QLabel(self.scrollAreaWidgetContents)
    #     self.label_10.setObjectName(u"label_10")
    #
    #     self.gridLayout.addWidget(self.label_10, 8, 1, 1, 1, Qt.AlignLeft)
    #
    #     self.label_8 = QLabel(self.scrollAreaWidgetContents)
    #     self.label_8.setObjectName(u"label_8")
    #
    #     self.gridLayout.addWidget(self.label_8, 9, 1, 1, 1, Qt.AlignLeft)
    #
    #     self.label_13 = QLabel(self.scrollAreaWidgetContents)
    #     self.label_13.setObjectName(u"label_13")
    #
    #     self.gridLayout.addWidget(self.label_13, 14, 1, 1, 1, Qt.AlignLeft)
    #
    #     self.app_3_cards = QPushButton(self.scrollAreaWidgetContents)
    #     self.app_3_cards.setObjectName(u"app_3_cards")
    #     self.app_3_cards.setIcon(icon4)
    #     self.app_3_cards.setIconSize(QSize(30, 30))
    #
    #     self.gridLayout.addWidget(self.app_3_cards, 14, 0, 1, 1)
    #
    #     self.image_cards = QPushButton(self.scrollAreaWidgetContents)
    #     self.image_cards.setObjectName(u"image_cards")
    #     icon6 = QIcon()
    #     icon6.addFile(u":/icons/Icons/image_white_24dp.svg", QSize(), QIcon.Normal, QIcon.Off)
    #     self.image_cards.setIcon(icon6)
    #     self.image_cards.setIconSize(QSize(30, 30))
    #
    #     self.gridLayout.addWidget(self.image_cards, 5, 0, 1, 1)
    #
    #     self.text_cards = QPushButton(self.scrollAreaWidgetContents)
    #     self.text_cards.setObjectName(u"text_cards")
    #     icon7 = QIcon()
    #     icon7.addFile(u":/icons/Icons/title_white_24dp.svg", QSize(), QIcon.Normal, QIcon.Off)
    #     self.text_cards.setIcon(icon7)
    #     self.text_cards.setIconSize(QSize(30, 30))
    #
    #     self.gridLayout.addWidget(self.text_cards, 4, 0, 1, 1)
    #
    #     self.label_2 = QLabel(self.scrollAreaWidgetContents)
    #     self.label_2.setObjectName(u"label_2")
    #     self.label_2.setFont(font)
    #
    #     self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
    #
    #     self.app_2_cards = QPushButton(self.scrollAreaWidgetContents)
    #     self.app_2_cards.setObjectName(u"app_2_cards")
    #     self.app_2_cards.setIcon(icon4)
    #     self.app_2_cards.setIconSize(QSize(30, 30))
    #
    #     self.gridLayout.addWidget(self.app_2_cards, 13, 0, 1, 1)
    #
    #     self.label_5 = QLabel(self.scrollAreaWidgetContents)
    #     self.label_5.setObjectName(u"label_5")
    #
    #     self.gridLayout.addWidget(self.label_5, 5, 1, 1, 1, Qt.AlignLeft)
    #
    #     self.folder_3_cards = QPushButton(self.scrollAreaWidgetContents)
    #     self.folder_3_cards.setObjectName(u"folder_3_cards")
    #     self.folder_3_cards.setIcon(icon)
    #     self.folder_3_cards.setIconSize(QSize(30, 30))
    #
    #     self.gridLayout.addWidget(self.folder_3_cards, 10, 0, 1, 1)
    #
    #     self.label_15 = QLabel(self.scrollAreaWidgetContents)
    #     self.label_15.setObjectName(u"label_15")
    #     self.label_15.setMaximumSize(QSize(16777215, 60))
    #     self.label_15.setMargin(20)
    #
    #     self.gridLayout.addWidget(self.label_15, 11, 0, 1, 1)
    #
    #     self.folder_2_cards = QPushButton(self.scrollAreaWidgetContents)
    #     self.folder_2_cards.setObjectName(u"folder_2_cards")
    #     self.folder_2_cards.setIcon(icon)
    #     self.folder_2_cards.setIconSize(QSize(30, 30))
    #
    #     self.gridLayout.addWidget(self.folder_2_cards, 9, 0, 1, 1)
    #
    #     self.scrollArea.setWidget(self.scrollAreaWidgetContents)
    #
    #     self.horizontalLayout_5.addWidget(self.scrollArea)
    #
    #     self.horizontalLayout.addWidget(self.left_menu_frame)
    #
    #     self.right_frame = QFrame(self.centralwidget)
    #     self.right_frame.setObjectName(u"right_frame")
    #     self.right_frame.setFrameShape(QFrame.StyledPanel)
    #     self.right_frame.setFrameShadow(QFrame.Raised)
    #     self.verticalLayout = QVBoxLayout(self.right_frame)
    #     self.verticalLayout.setSpacing(0)
    #     self.verticalLayout.setObjectName(u"verticalLayout")
    #     self.verticalLayout.setContentsMargins(0, 0, 0, 0)
    #     self.header_frame = QFrame(self.right_frame)
    #     self.header_frame.setObjectName(u"header_frame")
    #     self.header_frame.setFrameShape(QFrame.NoFrame)
    #     self.header_frame.setFrameShadow(QFrame.Raised)
    #     self.horizontalLayout_2 = QHBoxLayout(self.header_frame)
    #     self.horizontalLayout_2.setSpacing(0)
    #     self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
    #     self.horizontalLayout_2.setContentsMargins(0, 12, 0, 0)
    #     self.left_header_frame = QFrame(self.header_frame)
    #     self.left_header_frame.setObjectName(u"left_header_frame")
    #     self.left_header_frame.setFrameShape(QFrame.StyledPanel)
    #     self.left_header_frame.setFrameShadow(QFrame.Raised)
    #     self.horizontalLayout_4 = QHBoxLayout(self.left_header_frame)
    #     self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
    #     self.lineEdit = QLineEdit(self.left_header_frame)
    #     self.lineEdit.setObjectName(u"lineEdit")
    #
    #     self.horizontalLayout_4.addWidget(self.lineEdit)
    #
    #     self.search_button = QPushButton(self.left_header_frame)
    #     self.search_button.setObjectName(u"search_button")
    #     icon8 = QIcon()
    #     icon8.addFile(u":/icons/Icons/search_white_24dp.svg", QSize(), QIcon.Normal, QIcon.Off)
    #     self.search_button.setIcon(icon8)
    #
    #     self.horizontalLayout_4.addWidget(self.search_button)
    #
    #     self.horizontalLayout_2.addWidget(self.left_header_frame, 0, Qt.AlignRight)
    #
    #     self.right_header_frame = QFrame(self.header_frame)
    #     self.right_header_frame.setObjectName(u"right_header_frame")
    #     self.right_header_frame.setFrameShape(QFrame.StyledPanel)
    #     self.right_header_frame.setFrameShadow(QFrame.Raised)
    #     self.horizontalLayout_3 = QHBoxLayout(self.right_header_frame)
    #     self.horizontalLayout_3.setSpacing(12)
    #     self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
    #     self.horizontalLayout_3.setContentsMargins(0, 0, 12, 0)
    #     self.side_bar_button = QPushButton(self.right_header_frame)
    #     self.side_bar_button.setObjectName(u"side_bar_button")
    #     icon9 = QIcon()
    #     icon9.addFile(u":/icons/Icons/view_sidebar_white_24dp.svg", QSize(), QIcon.Normal, QIcon.Off)
    #     self.side_bar_button.setIcon(icon9)
    #     self.side_bar_button.setIconSize(QSize(22, 22))
    #
    #     self.horizontalLayout_3.addWidget(self.side_bar_button)
    #
    #     self.anchor_button = QPushButton(self.right_header_frame)
    #     self.anchor_button.setObjectName(u"anchor_button")
    #     icon10 = QIcon()
    #     icon10.addFile(u":/icons/Icons/anchor_white_24dp.svg", QSize(), QIcon.Normal, QIcon.Off)
    #     self.anchor_button.setIcon(icon10)
    #     self.anchor_button.setIconSize(QSize(22, 22))
    #
    #     self.horizontalLayout_3.addWidget(self.anchor_button)
    #
    #     self.settings_button = QPushButton(self.right_header_frame, clicked=lambda: self.openWindow(self.dao))
    #
    #     self.settings_button.setObjectName(u"settings_button")
    #     icon11 = QIcon()
    #     icon11.addFile(u":/icons/Icons/settings_white_24dp.svg", QSize(), QIcon.Normal, QIcon.Off)
    #     self.settings_button.setIcon(icon11)
    #     self.settings_button.setIconSize(QSize(22, 22))
    #
    #     self.horizontalLayout_3.addWidget(self.settings_button)
    #
    #     self.horizontalLayout_2.addWidget(self.right_header_frame, 0, Qt.AlignRight)
    #
    #     self.verticalLayout.addWidget(self.header_frame)
    #
    #     self.center_frame = QFrame(self.right_frame)
    #     self.center_frame.setObjectName(u"center_frame")
    #     self.center_frame.setFrameShape(QFrame.NoFrame)
    #     self.center_frame.setFrameShadow(QFrame.Raised)
    #     self.horizontalLayout_7 = QHBoxLayout(self.center_frame)
    #     self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
    #
    #     self.scrollArea_2 = QScrollArea(self.center_frame)
    #     self.scrollArea_2.setObjectName(u"scrollArea_2")
    #
    #     self.scrollArea_2.setWidgetResizable(True)
    #     self.scrollAreaWidgetContents_2 = QWidget()
    #     self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
    #     self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 607, 688))
    #
    #     self.gridLayout2 = QGridLayout(self.scrollAreaWidgetContents_2)
    #     self.gridLayout2.setSpacing(0)
    #     self.gridLayout2.setObjectName(u"gridLayout_2")
    #     self.gridLayout2.setContentsMargins(0, 0, 0, 0)
    #
    #     self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
    #
    #     self.horizontalLayout_7.addWidget(self.scrollArea_2, Qt.AlignTop)
    #
    #     self.verticalLayout.addWidget(self.center_frame)
    #
    #     self.footer_frame = QFrame(self.right_frame)
    #     self.footer_frame.setObjectName(u"footer_frame")
    #     self.footer_frame.setFrameShape(QFrame.NoFrame)
    #     self.footer_frame.setFrameShadow(QFrame.Raised)
    #     self.horizontalLayout_6 = QHBoxLayout(self.footer_frame)
    #     self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
    #     self.frame = QFrame(self.footer_frame)
    #     self.frame.setObjectName(u"frame")
    #     self.frame.setFrameShape(QFrame.StyledPanel)
    #     self.frame.setFrameShadow(QFrame.Raised)
    #
    #     self.horizontalLayout_6.addWidget(self.frame)
    #
    #     self.size_grip = QFrame(self.footer_frame)
    #     self.size_grip.setObjectName(u"size_grip")
    #     self.size_grip.setMinimumSize(QSize(10, 10))
    #     self.size_grip.setMaximumSize(QSize(10, 10))
    #     self.size_grip.setFrameShape(QFrame.StyledPanel)
    #     self.size_grip.setFrameShadow(QFrame.Raised)
    #
    #     self.horizontalLayout_6.addWidget(self.size_grip, 0, Qt.AlignBottom)
    #
    #     self.verticalLayout.addWidget(self.footer_frame)
    #
    #     self.horizontalLayout.addWidget(self.right_frame)
    #
    #     MainWindow.setCentralWidget(self.centralwidget)
    #
    #     self.retranslateUi(MainWindow)
    #
    #     QMetaObject.connectSlotsByName(MainWindow)
    #     # setupUi
    #
    # def retranslateUi(self, MainWindow):
    #     MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
    #     self.folder_1_cards.setText("")
    #     self.label_9.setText(QCoreApplication.translate("MainWindow", u"Folder 3", None))
    #     self.label.setText(QCoreApplication.translate("MainWindow", u"All cards", None))
    #     self.link_cards.setText("")
    #     self.gif_cards.setText("")
    #     self.label_7.setText(QCoreApplication.translate("MainWindow", u"URL", None))
    #     self.label_6.setText(QCoreApplication.translate("MainWindow", u"Text", None))
    #     self.label_11.setText(QCoreApplication.translate("MainWindow", u"Folders", None))
    #     self.all_cards.setText("")
    #     self.label_14.setText(QCoreApplication.translate("MainWindow", u"App 1", None))
    #     self.app_1_cards.setText("")
    #     self.label_12.setText(QCoreApplication.translate("MainWindow", u"App 2", None))
    #     self.favorite_cards.setText("")
    #     self.label_4.setText(QCoreApplication.translate("MainWindow", u"Types", None))
    #     self.label_3.setText(QCoreApplication.translate("MainWindow", u"GIFs", None))
    #     self.label_10.setText(QCoreApplication.translate("MainWindow", u"Folder 1", None))
    #     self.label_8.setText(QCoreApplication.translate("MainWindow", u"Folder 2", None))
    #     self.label_13.setText(QCoreApplication.translate("MainWindow", u"App 3", None))
    #     self.app_3_cards.setText("")
    #     self.image_cards.setText("")
    #     self.text_cards.setText("")
    #     self.label_2.setText(QCoreApplication.translate("MainWindow", u"Favorites", None))
    #     self.app_2_cards.setText("")
    #     self.label_5.setText(QCoreApplication.translate("MainWindow", u"Image", None))
    #     self.folder_3_cards.setText("")
    #     self.label_15.setText(QCoreApplication.translate("MainWindow", u"Apps", None))
    #     self.folder_2_cards.setText("")
    #     self.search_button.setText("")
    #     self.side_bar_button.setText("")
    #     self.anchor_button.setText("")
    #     self.settings_button.setText("")
    #     #retranslateUi


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # MainWindow = QMainWindow()
    ui = UI()
    # ui.setupUi(MainWindow)

    ui.cardMaker.initializeUI(ui.dao.getAllCards())
    gc = grabClip.ClipboardManager(ui.cardMaker, ui.dao)
    gc.manage_clip()
    # MainWindow.show()

    widget = QStackedWidget()
    window1 = loginPage.login(ui.dao, widget, ui)  
    window2 = loginPage.newUser(ui.dao, widget, ui)
    window3 =  loginPage.login2(ui.dao, widget, ui) 
    widget.addWidget(window1)
    widget.addWidget(window2)
    widget.addWidget(window3)
    widget.setFixedHeight(493)
    widget.setFixedWidth(370)
    qr = widget.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    widget.move(qr.topLeft())

    qr1 = ui.frameGeometry()
    cp1 = QDesktopWidget().availableGeometry().center()
    qr1.moveCenter(cp)
    ui.move(qr1.topLeft())

    widget.show()

    sys.exit(app.exec_())
