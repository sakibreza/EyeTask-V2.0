from threading import Thread

import cv2
from PyQt5.QtGui import QImage, QPixmap


# Commands :
# left
# right
# up
# down
# press
# exit

class Controller:
    def __init__(self, main_window, giveOutput):
        # self.speech_detector = Speech()
        self.giveOutput = giveOutput
        self.main_window = main_window
        self.cap = cv2.VideoCapture(0)
        self.thread = Thread(target=self.inputs)

    def getInput(self):
        _, img = self.cap.read()

        outImage = toQImage(img)
        outImage = outImage.rgbSwapped()
        self.main_window.main_image_label.setPixmap(QPixmap.fromImage(outImage))

        if not self.thread.is_alive():
            self.thread = Thread(target=self.inputs)
            self.thread.start()

    def inputs(self):
        str = input("Enter the command : ")
        self.giveOutput(str)


def toQImage(raw_img):
    from numpy import copy
    img = copy(raw_img)
    qformat = QImage.Format_Indexed8
    if len(img.shape) == 3:
        if img.shape[2] == 4:
            qformat = QImage.Format_RGBA8888
        else:
            qformat = QImage.Format_RGB888

    outImg = QImage(img.tobytes(), img.shape[1], img.shape[0], img.strides[0], qformat)
    return outImg
