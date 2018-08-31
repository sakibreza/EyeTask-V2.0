import subprocess
import pyautogui


class ResourcePdf:

    def Open(self, docName):
        file = "/Storage/Desktop/EyeTask-V2.0/Documents" + docName
        self.process = subprocess.Popen(["masterpdfeditor5", file])

    def scrollDown(self):
        pyautogui.press('down')

    def scrollUp(self):
        pyautogui.press('up')

    def Terminate(self):
        self.process.terminate()
