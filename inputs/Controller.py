import cv2
from PyQt5.QtGui import QImage, QPixmap

import MainWindow
from inputs.BlinkDetector import BlinkDetector
from inputs.FaceDetector import FaceDetector
from inputs.GazeDetector import GazeDetector
from inputs.Speech import Speech


# Commands :
# left
# right
# up
# down
# press
# exit

class Controller:
    def __init__(self, main_window, giveOutput):
        self.blink_detector = BlinkDetector()
        self.face_detector = FaceDetector()
        self.gaze_detector = GazeDetector()
        # self.speech_detector = Speech()
        self.giveOutput = giveOutput
        self.main_window = main_window
        self.cap = cv2.VideoCapture(0)

    def getInput(self):

        if self.main_window.current_mode is MainWindow.MODE.MAIN or self.main_window.current_mode is MainWindow.MODE.VIDEO or self.main_window.current_mode is MainWindow.MODE.AUDIO or self.main_window.current_mode is MainWindow.MODE.NEWS or self.main_window.current_mode is MainWindow.MODE.NEWSING:
            if self.main_window.selectMethodComboBox.currentIndex() == MainWindow.METHOD.EYE_HELP:
                _, img = self.cap.read()

                dicBlink = self.blink_detector.processImage(img, self.main_window.eyeThreshold.value())

                outImage = toQImage(dicBlink["img"])
                outImage = outImage.rgbSwapped()
                self.main_window.main_image_label.setPixmap(QPixmap.fromImage(outImage))
                label = "Blink Detector : " \
                        "both : " + str(dicBlink["both"]) + "\n" + \
                        "left : " + str(dicBlink["left"]) + "\n" + \
                        "right : " + str(dicBlink["right"]) + "\n" + \
                        "leftEAR : " + str(dicBlink["leftEAR"]) + "\n" + \
                        "rightEAR :" + str(dicBlink["rightEAR"]) + "\n" + \
                        "bothTotal : " + str(dicBlink["bothTotal"]) + "\n" + \
                        "leftTotal : " + str(dicBlink["leftTotal"]) + "\n" + \
                        "rightTotal : " + str(dicBlink["rightTotal"]) + "\n"
                self.main_window.image_info_textlabel.setText(label)

                if dicBlink["left"]:
                    self.giveOutput("left")
                    return
                elif dicBlink["right"]:
                    self.giveOutput("right")
                    return
                elif dicBlink["both"]:
                    self.giveOutput("press")
                    return

            elif self.main_window.selectMethodComboBox.currentIndex() == MainWindow.METHOD.HEAD_HELP:
                _, img = self.cap.read()

                dicBlink = self.blink_detector.processImage(img, self.main_window.eyeThreshold.value())

                outImage = toQImage(dicBlink["img"])
                outImage = outImage.rgbSwapped()
                self.main_window.main_image_label.setPixmap(QPixmap.fromImage(outImage))
                dicHead = self.face_detector.processImage(img)

                label = "Blink Detector : " \
                        "both : " + str(dicBlink["both"]) + "\n" \
                        "left : " + str(dicBlink["left"]) + "\n" \
                        "right : " + str(dicBlink["right"]) + "\n" \
                        "leftEAR : " + str(dicBlink["leftEAR"]) + "\n" \
                        "rightEAR :" + str(dicBlink["rightEAR"]) + "\n" \
                        "bothTotal : " + str(dicBlink["bothTotal"]) + "\n" \
                        "leftTotal : " + str(dicBlink["leftTotal"]) + "\n" \
                        "rightTotal : " + str(dicBlink["rightTotal"]) + "\n" \
                        "Head Detector : " + "\n" \
                        "direction : " + str(dicHead["direction"]) + "\n"
                self.main_window.image_info_textlabel.setText(label)

                head = dicHead["direction"]
                if head == "left":
                    self.giveOutput("left")
                    return
                elif head == "right":
                    self.giveOutput("right")
                    return
                elif head == "up":
                    self.giveOutput("up")
                    return
                elif head == "down":
                    self.giveOutput("down")
                    return
                elif dicBlink["both"]:
                    self.giveOutput("press")
                    return
                elif dicBlink["right"]:
                    self.face_detector.initPos(dicHead["face"])
                    return
                elif dicBlink["left"]:
                    self.giveOutput("exit")

        elif self.main_window.current_mode is MainWindow.MODE.CHAIR:
            if self.main_window.selectMethodComboBox.currentIndex() == MainWindow.METHOD.EYE_HELP:
                _, img = self.cap.read()
                dicGaze = self.gaze_detector.processImage(img)
                dicBlink = self.blink_detector.processImage(img, self.main_window.eyeThreshold.value())
                label = "Blink Detector : " \
                        "both : " + str(dicBlink["both"]) + "\n" \
                        "left : " + str(dicBlink["left"]) + "\n" \
                        "right : " + str(dicBlink["right"]) + "\n" \
                        "leftEAR : " + str(dicBlink["leftEAR"]) + "\n" \
                        "rightEAR :" + str(dicBlink["rightEAR"]) + "\n" \
                        "bothTotal : " + str(dicBlink["bothTotal"]) + "\n" \
                        "leftTotal : " + str(dicBlink["leftTotal"]) + "\n" \
                        "rightTotal : " + str(dicBlink["rightTotal"]) + "\n" \
                        "Gaze Detector : " + "\n" \
                        "direction : " + str(dicGaze["direction"]) + "\n"
                self.main_window.image_info_textlabel.setText(label)
                outImage = toQImage(dicBlink["img"])
                outImage = outImage.rgbSwapped()
                self.main_window.main_image_label.setPixmap(QPixmap.fromImage(outImage))
                self.giveOutput(dicGaze["direction"])
                if dicBlink["right"] or dicBlink["left"]:
                    self.giveOutput("exit")
                    cv2.destroyAllWindows()

                return

            elif self.main_window.selectMethodComboBox.currentIndex() == MainWindow.METHOD.HEAD_HELP:
                _, img = self.cap.read()
                dicBlink = self.blink_detector.processImage(img, self.main_window.eyeThreshold.value())
                dicHead = self.face_detector.processImage(img)

                label = "Blink Detector : " \
                        "both : " + str(dicBlink["both"]) + "\n" \
                        "left : " + str(dicBlink["left"]) + "\n" \
                        "right : " + str(dicBlink["right"]) + "\n" \
                        "leftEAR : " + str(dicBlink["leftEAR"]) + "\n" \
                        "rightEAR :" + str(dicBlink["rightEAR"]) + "\n" \
                        "bothTotal : " + str(dicBlink["bothTotal"]) + "\n" \
                        "leftTotal : " + str(dicBlink["leftTotal"]) + "\n" \
                        "rightTotal : " + str(dicBlink["rightTotal"]) + "\n" \
                        "Head Detector : " + "\n" \
                        "direction : " + str(dicBlink["rightTotal"]) + "\n"
                self.main_window.image_info_textlabel.setText(label)

                outImage = toQImage(dicBlink["img"])
                outImage = outImage.rgbSwapped()
                self.main_window.main_image_label.setPixmap(QPixmap.fromImage(outImage))
                head = dicHead["direction"]
                if head == "left":
                    self.giveOutput("left")
                    return
                elif head == "right":
                    self.giveOutput("right")
                    return
                elif head == "up":
                    self.giveOutput("up")
                    return
                elif head == "down":
                    self.giveOutput("down")
                    return
                elif dicBlink["both"]:
                    self.giveOutput("press")
                    return
                elif dicBlink["right"]:
                    self.face_detector.initPos(dicHead["face"])
                    return
                
        elif self.main_window.current_mode is MainWindow.MODE.SMS or self.main_window.current_mode is MainWindow.MODE.EMAIL:
            if self.main_window.selectMethodComboBox.currentIndex() == MainWindow.METHOD.EYE_HELP:
                _, img = self.cap.read()
                dicGaze = self.gaze_detector.processImage(img)
                dicBlink = self.blink_detector.processImage(img, self.main_window.eyeThreshold.value())
                label = "Blink Detector : " \
                        "both : " + str(dicBlink["both"]) + "\n" \
                        "left : " + str(dicBlink["left"]) + "\n" \
                        "right : " + str(dicBlink["right"]) + "\n" \
                        "leftEAR : " + str(dicBlink["leftEAR"]) + "\n" \
                        "rightEAR :" + str(dicBlink["rightEAR"]) + "\n" \
                        "bothTotal : " + str(dicBlink["bothTotal"]) + "\n" \
                        "leftTotal : " + str(dicBlink["leftTotal"]) + "\n" \
                        "rightTotal : " + str(dicBlink["rightTotal"]) + "\n" \
                        "Gaze Detector : " + "\n" \
                        "direction : " + str(dicGaze["direction"]) + "\n"
                self.main_window.image_info_textlabel.setText(label)
                outImage = toQImage(dicBlink["img"])
                outImage = outImage.rgbSwapped()
                self.main_window.main_image_label.setPixmap(QPixmap.fromImage(outImage))
                if dicBlink["left"]:
                    self.giveOutput("left")
                elif dicBlink["right"]:
                    self.giveOutput("right")
                elif dicBlink["both"]:
                    self.giveOutput("press")
                elif dicGaze["direction"] == "left":
                    self.giveOutput("gazeleft")
                elif dicGaze["direction"] == "right":
                    self.giveOutput("gazeright")
                


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
