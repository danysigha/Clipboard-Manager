from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QLabel

class CardRenderer():
    def __init__(self, parent, position):  # - parent=None
        # super(newCopy, self).__init__(parent)
        self.label = QLabel()
        self.label.setMinimumSize(QSize(200, 150))
        self.label.setMaximumSize(QSize(200, 150))
        self.label.setStyleSheet(u"*{\n"
                                 "border:4px solid black;\n"
                                 "  border-radius: 15px;\n"
                                 "  padding: 15px;\n"
                                 # "  box-shadow: 0px 0px 20px 20px black;\n"
                                 "  background-color: white;\n"
                                 "}")
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        parent.addWidget(self.label, position[0], position[1], position[2], position[3], Qt.AlignTop)
        if (position[1] + 1) % 3 == 0:
            position[0] += 1
            position[1] = 0
        else:
            position[1] += 1

    def grabNewItem(self):
        return self.label
