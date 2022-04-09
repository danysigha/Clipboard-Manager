import PIL.Image as Image
import os
import io
from PyQt5.QtCore import QTimer
from AppKit import NSPasteboard, NSStringPboardType, NSTIFFPboardType, NSPasteboardTypePNG, NSURL, NSURLPboardType

class clipboardManager():
    def __init__(self, pasteboardCount, pasteboard):
        self._currentCount = pasteboardCount
        self._pb = pasteboard

        def updateUI(self):
            """Check if clipboard item count changed and update interface accordingly by creating
            new widget"""

            if self._currentCount != self._pb.changeCount():

                data_type = self._pb.types()  # only used to check data type

                if NSStringPboardType in data_type:
                    pbstring = self.pb.stringForType_(NSStringPboardType)
                    self.label_16.setText(pbstring)
                    # print("Pastboard string: %s" % pbstring)

                elif NSTIFFPboardType in data_type:
                    # pbimage = self.pb.dataForType_(NSTIFFPboardType)
                    pbimage = self.pb.dataForType_(NSTIFFPboardType)
                    image = Image.open(io.BytesIO(pbimage))  # check what image.open does
                    filepath = os.path.abspath(os.getcwd()) + "/img_copy/img_copy_" + str(
                        self.changeCount) + ".png"  # check if this line is neccessary
                    image.save(filepath, quality=95)  # is this really a PNG??? - you can specify format here
                    # image.thumbnail(size, Image.ANTIALIAS)
                    pixmap = QPixmap(filepath)
                    pixmap4 = pixmap.scaled(200, 150, Qt.KeepAspectRatio)
                    # pixmap2 = pixmap.scaledToWidth(200)
                    # pixmap = pixmap.scaledToHeight(150, Qt.SmoothTransformation);
                    # pixmap = pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    # print(pbimage)
                    self.label_16.setPixmap(pixmap4)
                    self.changeCount = self.pb.changeCount()

                #missing URL implementation for now

        def manage_clip(self):
            self.pb = NSPasteboard.generalPasteboard()
            self.changeCount = self.pb.changeCount()
            self.timer = QTimer()  # set up your QTimer
            self.timer.timeout.connect(lambda: self.updateClip(self.changeCount))  # connect it to your update function
            self.timer.start(1000)  # set it to timeout in 5000 ms
