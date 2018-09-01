from enum import IntEnum, auto

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi

from WheelChair import WheelChair
from inputs.Controller import Controller
from Resources.ResourceKeyboard import ResourceKeyboard

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
    SMS = auto()
    EMAIL = auto()


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

        self.resetButton.clicked.connect(self.resetAll)

        self.chair = WheelChair()
        
        self.keyboard = None
        self.sms = ""
        self.email = ""

        self.current_mode = MODE.MAIN
        self.current_focus = 0

        self.__initialize_buttons()

        self.main_controller = Controller(self, self.gotInput)

        self.player = None
        self.document = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.main_controller.getInput)
        self.timer.start(100)

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

        elif self.current_mode == MODE.AUDIO:
            if command == "right":
                self.player.nextItem()
            elif command == "left":
                if self.player.playing:
                    self.player.stop()
                else:
                    self.player.Close()
                    self.current_mode = MODE.MAIN
            elif command == "press":
                self.player.togglePlay()
                
        elif self.current_mode == MODE.VIDEO:
            if command == "right":
                self.player.nextItem()
            elif command == "left":
                if self.player.resourceVideo.process != None:
                    self.player.stop()
                else:
                    self.player.Close()
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
                if self.document.Open():
                    self.current_mode = MODE.NEWSING

        elif self.current_mode == MODE.NEWSING:
            if command == "right" or command == "down":
                self.document.scrollDown()
            elif command == "left" or command == "up":
                self.document.scrollUp()
            elif command == "press":
                self.document.Close()
                self.current_mode = MODE.NEWS
                
        elif self.current_mode == MODE.SMS:
            
            if self.keyboard != None:
                if command == "right" or command == "down":
                    self.keyboard.moveFocusRight()
                elif command == "left" or command == "up":
                    self.keyboard.moveFocusLeft()
                elif command == "gazeright":
                    self.keyboard.moveFloatRight()
                elif command == "gazeleft":
                    self.keyboard.moveFloatLeft()
                elif command == "press":
                    if self.keyboard.selectKey():
                        self.sms = self.keyboard.str
                        self.keyboard = None
                        
            else:
              
                if self.sms != "":
                    
                    from zeep import Client
                    
                    try:
                        url = 'https://api2.onnorokomsms.com/sendsms.asmx?WSDL'
                        client = Client(url)
                        userName = '01521313223'
                        password = '90053'
                        recipientNumber = '01521323429'
                        smsText = self.sms
                        smsType = 'TEXT'
                        maskName = ''
                        campaignName = ''
                        client.service.OneToOne(userName, password, recipientNumber, smsText, smsType, maskName, campaignName)
                        self.statusBar.showMessage("SMS sent",2000)
                        print('SMS sent!')
                    except Exception as e:
                        self.statusBar.showMessage("SMS not sent",2000)
                        print('SMS not sent!')
                        print(e)    
                    self.sms = ""
                        
                self.current_mode = MODE.MAIN
                
        elif self.current_mode == MODE.EMAIL:
            
            if self.keyboard != None:
                if command == "right" or command == "down":
                    self.keyboard.moveFocusRight()
                elif command == "left" or command == "up":
                    self.keyboard.moveFocusLeft()
                elif command == "gazeright":
                    self.keyboard.moveFloatRight()
                elif command == "gazeleft":
                    self.keyboard.moveFloatLeft()
                elif command == "press":
                    if self.keyboard.selectKey():
                        self.email = self.keyboard.str
                        self.keyboard = None
                        
            else:
                
                if self.email != "":
                    
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
            
                        body = self.email
                        msg.attach(MIMEText(body, 'plain'))
            
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(fromaddr, '060701cse')
                        text = msg.as_string()
                        server.sendmail(fromaddr, toaddr, text)
                        self.statusBar.showMessage("Email sending!",2000)
                        server.quit()
                        self.statusBar.showMessage("Email sent!",2000)
                        print('Email Sent Successfully')
                    except Exception as e:
                        self.statusBar.showMessage("Email not sent!",2000)
                        print('Email not sent')
                        print(e)
                    
                    self.email = ""
                    
                self.current_mode = MODE.MAIN
                

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
        self.b2_3.clicked.connect(self.playDocument)
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
        
    def playFan(self):
        self.chair.toggleFan()
     
    def controlWheel(self):
        self.current_mode = MODE.CHAIR
        self.chair.active = True
        from PyQt5 import QtWidgets
        sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
        height = sizeObject.height()
        width = sizeObject.width()
        self.move(int(width * 0.5), int(height * 0.1))
        
    def playLight(self):
        self.chair.toggleLight()

    def playMusic(self):
        from Players.Audio import Audio
        self.current_mode = MODE.AUDIO
        self.player = Audio()

    def playVideo(self):
        from Players.Video import Video
        self.current_mode = MODE.VIDEO
        self.player = Video()

    def playSMS(self):
        
        self.keyboard = ResourceKeyboard()
        
        self.current_mode = MODE.SMS

    def playEmail(self):
        
        self.keyboard = ResourceKeyboard()
        self.current_mode = MODE.EMAIL

    def playDocument(self):
        from Document import Document
        self.current_mode = MODE.NEWS
        self.document = Document()
