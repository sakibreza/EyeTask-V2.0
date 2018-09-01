from enum import IntEnum, auto

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from Document import Document
from WheelChair import WheelChair
from inputs.Controller import Controller


# from testing.Controller import Controller


class MODE(IntEnum):
    CHAIR = auto()
    MAIN = auto()
    SUBPROC = auto()
    AUDIO = auto()
    VIDEO = auto()
    NEWS = auto()
    PLAYING = auto()
    NEWSING = auto()


class METHOD(IntEnum):
    EYE_HELP = 0
    HEAD_HELP = 1
    VOICE_HELP = 2


class MainWindow(QMainWindow):
    def __init__(self):
        WINDOW_TITLE = "Eye Based Wheelchair Control & Task Manager"
        GUI_UI_LOCATION = "./UI/MainWindow.ui"

        super(MainWindow, self).__init__()
        loadUi(GUI_UI_LOCATION, self)
        self.setWindowTitle(WINDOW_TITLE)
        self.main_image_label.setScaledContents(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.b = QtGui.QPushButton("exit", self, clicked=self.close)

        self.resetButton.clicked.connect(self.resetAll)

        self.chair = WheelChair()

        self.current_mode = MODE.MAIN
        self.current_focus = 0

        self.__initialize_buttons()

        self.main_controller = Controller(self, self.gotInput)

        self.player = None
        self.document = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.main_controller.getInput)
        self.timer.start(10)

    def gotInput(self, command):
        print("Got input : " + str(command))

        if self.current_mode == MODE.MAIN:
            if command == "left":
                self.moveFocusLeft()
            elif command == "right":
                self.moveFocusRight()
            elif command == "up":
                self.moveFocusUp()
            elif command == "down":
                self.moveFocusDown()
            elif command == "press":
                self.pressFocused()

        elif self.current_mode == MODE.CHAIR:
            if command == "left":
                self.chair.left()
            elif command == "right":
                self.chair.right()
            elif command == "press":
                self.chair.toggleStartStop()
            elif command == "exit":
                self.chair.active = False
                self.current_mode = MODE.MAIN

        elif self.current_mode == MODE.AUDIO or self.current_mode == MODE.VIDEO:
            if command == "right":
                self.player.nextItem()
            elif command == "left":
                self.player.destroy()
                self.current_mode = MODE.MAIN
            elif command == "press":
                self.player.togglePlay()

        elif self.current_mode == MODE.NEWS:
            if command == "right" or command == "down":
                self.document.nextItem()
            elif command == "left" or command == "up":
                self.document.destroy()
                self.current_mode = MODE.MAIN
            elif command == "press":
                self.document.Open()
                self.current_mode = MODE.NEWSING

        elif self.current_mode == MODE.NEWSING:
            if command == "right" or command == "down":
                self.document.scrollDown()
            elif command == "left" or command == "up":
                self.document.scrollUp()
            elif command == "press":
                self.document.Close()

    def closeEvent(self, event):
        # self.main_controller.closed()
        # self.deleteLater()
        pass

    def resetAll(self):
        pass

    def __initialize_buttons(self):
        self.selectMethodComboBox.clear()
        self.selectMethodComboBox.addItems([
            "Eye-Help",
            "Head-Help",
            "Voice-Help"
        ])
        self.selectMethodComboBox.setCurrentIndex(METHOD.EYE_HELP)
        self.selectMethodComboBox.currentIndexChanged.connect(self.comboboxIndexChanged)

        self.buttons = [self.b1_1, self.b1_2,
                        self.b1_3, self.b2_1,
                        self.b2_2, self.b2_3,
                        self.b3_1, self.b3_2]
        for b in self.buttons:
            b.setAutoDefault(True)
        self.buttons[self.current_focus].setFocus(True)

        self.b1_1.clicked.connect(self.controlWheel)
        self.b1_2.clicked.connect(self.playSMS)
        self.b1_3.clicked.connect(self.playEmail)
        self.b2_1.clicked.connect(self.playVideo)
        self.b2_2.clicked.connect(self.playMusic)
        self.b2_3.clicked.connect(self.playBrowser)
        self.b3_1.clicked.connect(self.playLight)
        self.b3_2.clicked.connect(self.playFan)

    def comboboxIndexChanged(self):
        import cv2
        cv2.destroyAllWindows()
        # TODO
        if self.selectMethodComboBox.currentIndex() == METHOD.EYE_HELP:
            pass
        elif self.selectMethodComboBox.currentIndex() == METHOD.HEAD_HELP:
            pass
        elif self.selectMethodComboBox.currentIndex() == METHOD.VOICE_HELP:
            pass

    def controlWheel(self):
        self.current_mode = MODE.CHAIR
        self.chair.active = True
        from PyQt5 import QtWidgets
        sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
        height = sizeObject.height()
        width = sizeObject.width()
        self.move(int(width * 0.5), int(height * 0.1))

    def playFan(self):
        self.chair.toggleFan()

    def playLight(self):
        self.chair.toggleLight()

    def playMusic(self):
        from Players.Audio import Audio
        self.current_mode = MODE.AUDIO
        self.player = Audio()

    def playVideo(self):
        self.current_mode = MODE.VIDEO

    def moveFocusRight(self):
        if self.current_mode is MODE.MAIN:
            self.current_focus = (self.current_focus + 1) % 8
            self.buttons[self.current_focus].setFocus(True)

    def moveFocusLeft(self):
        self.current_focus = (self.current_focus - 1) % 8
        self.buttons[self.current_focus].setFocus(True)

    def moveFocusUp(self):
        self.current_focus = (self.current_focus - 2) % 8
        self.buttons[self.current_focus].setFocus(True)

    def moveFocusDown(self):
        self.current_focus = (self.current_focus + 2) % 8
        self.buttons[self.current_focus].setFocus(True)

    def pressFocused(self):
        self.buttons[self.current_focus].animateClick()

    def playSMS(self):
        from zeep import Client
        try:
            url = 'https://api2.onnorokomsms.com/sendsms.asmx?WSDL'
            client = Client(url)
            userName = '01521313223'
            password = '90053'
            recipientNumber = '01521323429'
            smsText = 'Help Me'
            smsType = 'TEXT'
            maskName = ''
            campaignName = ''
            client.service.OneToOne(userName, password, recipientNumber, smsText, smsType, maskName, campaignName)
            print('SMS sent!')
        except Exception as e:
            print('SMS nor sent!')
            print(e)

    def playEmail(self):
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        import smtplib
        try:
            fromaddr = 'eyegaze.kuet@gmail.com'
            toaddr = 'sakibreza1@gmail.com'
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = 'Doctor Appointment'

            body = 'I am facing problem.Please come to see me if you are free.'
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, '060701cse')
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
            print('Email Sent Successfully')
        except Exception as e:
            print('Email not sent')
            print(e)

    def playBrowser(self):
        self.current_mode = MODE.NEWS
        self.document = Document()
