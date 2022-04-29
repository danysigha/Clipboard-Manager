import dao
import card
import card_generator as cardVisual
import PIL.Image as Image
import uuid
import os
import io
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
from AppKit import NSPasteboard, NSStringPboardType, NSTIFFPboardType, NSPasteboardTypePNG, NSURL, NSURLPboardType


class ClipboardManager():

    def __init__(self, scrollarea):  # main,
        self._pb = NSPasteboard.generalPasteboard()
        self._currentCount = NSPasteboard.generalPasteboard().changeCount()
        self._timer = QTimer()  # set up your QTimer
        self._ui = scrollarea  # pass label as test

        self._row = 0
        self._column = 0
        self._rowSpan = 1
        self._columnSpan = 1
        self._position = [self._row, self._column, self._rowSpan, self._columnSpan]
        # self._cardID = 1

    def initializeUI(self, content):
        for i in content:
            if i[2] == 'Text':
                newItem = cardVisual.CardRenderer(self._ui, self._position)
                newItem.grabNewItem().setText(i[1])
            elif i[2] == "Image":
                pixmap = QPixmap(i[1])
                pixmap4 = pixmap.scaled(150, 100, Qt.KeepAspectRatio)
                newItem = cardVisual.CardRenderer(self._ui, self._position)
                newItem.grabNewItem().setPixmap(pixmap4)


    def updateUI(self):
        """Check if clipboard item count changed and update interface accordingly by creating
        new widget"""

        if self._currentCount != self._pb.changeCount():

            data_type = self._pb.types()  # only used to check data type

            if NSStringPboardType in data_type:
                pbstring = self._pb.stringForType_(NSStringPboardType)
                # self.label_16.setText(pbstring) #need to create new widget instead
                # print("Pastboard string: %s" % pbstring)
                category = "Text"
                dao.DataAccessor().storeCard(pbstring, category)
                # card.Card(pbstring, category, self._cardID)
                # self._cardID += 1
                newItem = cardVisual.CardRenderer(self._ui, self._position)
                newItem.grabNewItem().setText(pbstring)
                # print(pbstring)

            elif NSTIFFPboardType in data_type:
                # pbimage = self.pb.dataForType_(NSTIFFPboardType)

                pbimage = self._pb.dataForType_(NSTIFFPboardType)
                image = Image.open(io.BytesIO(pbimage))  # check what image.open does
                filepath = os.path.abspath(os.getcwd()) + "/img_copy/" + str(
                    uuid.uuid4()) + ".png"  # check if this line is neccessary
                image.save(filepath, quality=95)  # is this really a PNG??? - you can specify format here
                # image.thumbnail(size, Image.ANTIALIAS)
                category = "Image"
                dao.DataAccessor().storeCard(filepath, category)
                # card.Card(filepath, category, self._cardID)
                # self._cardID += 1
                pixmap = QPixmap(filepath)
                pixmap4 = pixmap.scaled(150, 100, Qt.KeepAspectRatio)
                # pixmap2 = pixmap.scaledToWidth(200)
                # pixmap = pixmap.scaledToHeight(150, Qt.SmoothTransformation);
                # pixmap = pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                # print(pbimage)
                # self._position += 1
                # pos = (self._position) % 3
                # self._colons[pos] += 1
                newItem = cardVisual.CardRenderer(self._ui, self._position)
                newItem.grabNewItem().setPixmap(pixmap4)  # need to create new widget instead
                # print("Success!!")
            self._currentCount = self._pb.changeCount()

            # missing URL implementation for now

    def manage_clip(self):
        self._currentCount = self._pb.changeCount()
        self._timer.timeout.connect(lambda: self.updateUI())  # connect it to your update function
        self._timer.start(1000)  # set it to timeout in 1 second


if __name__ == "__main__":
    gc = ClipboardManager()
    gc.manage_clip()
