# import dao
import datetime
import card
import card_generator
import PIL.Image as Image
import uuid
import os
import io
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
from AppKit import NSPasteboard, NSStringPboardType, NSTIFFPboardType, NSPasteboardTypePNG, NSURL, NSURLPboardType


class ClipboardManager:

    def __init__(self, card_renderer, dao):  # main,
        self._pb = NSPasteboard.generalPasteboard()
        self._currentCount = NSPasteboard.generalPasteboard().changeCount()
        self._timer = QTimer()  # set up your QTimer
        # self._ui = scrollarea  # pass label as test
        # self._cardID = 1
        self._cardRenderer = card_renderer
        self._dao = dao


    def updateUI(self):
        """Check if clipboard item count changed and update interface accordingly by creating
        new widget"""

        if self._currentCount != self._pb.changeCount():

            data_type = self._pb.types()  # only used to check data type

            # card_id = uuid.uuid1().hex
            card_id = self._dao.getNextID()

            if NSStringPboardType in data_type:
                pbstring = self._pb.stringForType_(NSStringPboardType)
                # self.label_16.setText(pbstring) #need to create new widget instead
                # print("Pastboard string: %s" % pbstring)
                category = "Text"
                self._dao.storeCard(pbstring, category, 0)

                # card.Card(pbstring, category, self._cardID)
                # self._cardID += 1
                # new_card = card_generator.CardRenderer(self._ui)
                # self._cardRenderer.CardObject(self._cardRenderer.parent,
                #                               self._cardRenderer._position,
                #                               self._dao
                #                               ).addToInterface(card_id,
                #                                                pbstring,
                #                                                category,
                #                                                datetime.datetime.now(),
                #                                                datetime.datetime.now(),
                #                                                1, 0)
                card_generator.CardObject(self._cardRenderer.parent,
                                              self._cardRenderer._position,
                                              self._dao
                                              ).addToInterface(card_id,
                                                               pbstring,
                                                               category,
                                                               datetime.datetime.now(),
                                                               datetime.datetime.now(),
                                                               1, 0)

                # newItem.grabNewItem().setText(pbstring)
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
                self._dao.storeCard(filepath, category, 0)
                pixmap = QPixmap(filepath)
                pixmap4 = pixmap.scaled(150, 100, Qt.KeepAspectRatio)
                # pixmap2 = pixmap.scaledToWidth(200)
                # pixmap = pixmap.scaledToHeight(150, Qt.SmoothTransformation);
                # pixmap = pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                # print(pbimage)
                # new_card = card_generator.CardRenderer(self._ui)
                # self._cardRenderer.CardObject(self._cardRenderer.parent,
                #                               self._cardRenderer._position,
                #                               self._dao
                #                               ).addToInterface(card_id,
                #                                                pixmap4,
                #                                                category,
                #                                                datetime.datetime.now(),
                #                                                datetime.datetime.now(),
                #                                                1, 0)
                card_generator.CardObject(self._cardRenderer.parent,
                                              self._cardRenderer._position,
                                              self._dao
                                              ).addToInterface(card_id,
                                                               pixmap4,
                                                               category,
                                                               datetime.datetime.now(),
                                                               datetime.datetime.now(),
                                                               1, 0)

                # newItem = cardVisual.CardRenderer(self._ui, self._position, dao.DataAccessor().getNextID())
                # newItem.grabNewItem().setPixmap(pixmap4)  # need to create new widget instead

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
