import PIL.Image as Image
import uuid
import os
import io
from PyQt5.QtCore import QTimer, Qt, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QHBoxLayout
from AppKit import NSPasteboard, NSStringPboardType, NSTIFFPboardType, NSPasteboardTypePNG, NSURL, NSURLPboardType


class clipboardManager():
    # add class newCopy here!

    class newCopy():  # QGridLayout
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
            parent.addWidget(self.label, position[0], position[1], position[2], position[3], Qt.AlignTop)
            if (position[1] + 1) % 3 == 0:
                position[0] += 1
                position[1] = 0
            else:
                position[1] += 1

            # layout = QGridLayout()
            # layout = QHBoxLayout()
            # layout.addWidget(self.label)
            # self.setLayout(layout)

        def grabNewItem(self):
            return self.label

    def __init__(self, scrollarea):  # main,
        self._pb = NSPasteboard.generalPasteboard()
        self._currentCount = NSPasteboard.generalPasteboard().changeCount()
        self._timer = QTimer()  # set up your QTimer
        self._ui = scrollarea  # pass label as test
        # self._main_ui = main

        #self._position = -1

        self._row = 0
        self._column = 0
        self._rowSpan = 1
        self._columnSpan = 1
        self._position = [self._row, self._column, self._rowSpan, self._columnSpan]


    def updateUI(self):
        """Check if clipboard item count changed and update interface accordingly by creating
        new widget"""

        if self._currentCount != self._pb.changeCount():

            data_type = self._pb.types()  # only used to check data type

            if NSStringPboardType in data_type:
                pbstring = self._pb.stringForType_(NSStringPboardType)
                # self.label_16.setText(pbstring) #need to create new widget instead
                # print("Pastboard string: %s" % pbstring)
                newItem = self.newCopy(self._ui, self._position)
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
                pixmap = QPixmap(filepath)
                pixmap4 = pixmap.scaled(150, 100, Qt.KeepAspectRatio)
                # pixmap2 = pixmap.scaledToWidth(200)
                # pixmap = pixmap.scaledToHeight(150, Qt.SmoothTransformation);
                # pixmap = pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                # print(pbimage)
                # self._position += 1
                # pos = (self._position) % 3
                # self._colons[pos] += 1
                newItem = self.newCopy(self._ui, self._position)
                newItem.grabNewItem().setPixmap(pixmap4)  # need to create new widget instead
                # print("Success!!")

                #newItem = newCopy(self._ui, self._colons, content) add
            self._currentCount = self._pb.changeCount()

            # missing URL implementation for now

    def manage_clip(self):
        self._currentCount = self._pb.changeCount()
        self._timer.timeout.connect(lambda: self.updateUI())  # connect it to your update function
        self._timer.start(1000)  # set it to timeout in 1 second


if __name__ == "__main__":
    gc = clipboardManager()
    gc.manage_clip()
