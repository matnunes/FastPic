from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Only needed for access to command line arguments
import sys
import os
import queue
import subprocess
import time

from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox)
from PyQt5.QtCore import QProcess
from PyQt5.QtCore import QTimer

from FastPicUi import Ui_FastPicMainWindow
from FastPicTagWindow import FastPicTagWindow

from PyQt5.uic import loadUi

from smb.SMBConnection import SMBConnection
import configServer

class Window(QMainWindow, Ui_FastPicMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.setupUi(self)
        self.ui = Ui_FastPicMainWindow()
        self.ui.setupUi(self)
        self.connectSignalsSlots()

        self.infoMsgQueue = queue.Queue()

        self.updateMsgUi = QTimer()
        self.updateMsgUi.timeout.connect(self.updateTextMsgUi)
        self.updateMsgUi.setInterval(1750)
        self.updateMsgUi.start()

    def connectSignalsSlots(self):
        self.ui.btnNumKeyZero.clicked.connect(lambda: self.handleBtn(self.ui.btnNumKeyZero.text()))
        self.ui.btnNumKeyOne.clicked.connect(lambda: self.handleBtn(self.ui.btnNumKeyOne.text()))
        self.ui.btnNumKeyTwo.clicked.connect(lambda: self.handleBtn(self.ui.btnNumKeyTwo.text()))
        self.ui.btnNumKeyThree.clicked.connect(lambda: self.handleBtn(self.ui.btnNumKeyThree.text()))
        self.ui.btnNumKeyFour.clicked.connect(lambda: self.handleBtn(self.ui.btnNumKeyFour.text()))
        self.ui.btnNumKeyFive.clicked.connect(lambda: self.handleBtn(self.ui.btnNumKeyFive.text()))
        self.ui.btnNumKeySix.clicked.connect(lambda: self.handleBtn(self.ui.btnNumKeySix.text()))
        self.ui.btnNumKeySeven.clicked.connect(lambda: self.handleBtn(self.ui.btnNumKeySeven.text()))
        self.ui.btnNumKeyEight.clicked.connect(lambda: self.handleBtn(self.ui.btnNumKeyEight.text()))
        self.ui.btnNumKeyNine.clicked.connect(lambda: self.handleBtn(self.ui.btnNumKeyNine.text()))
        self.ui.btnNumKeyDot.clicked.connect(lambda: self.handleBtn(self.ui.btnNumKeyDot.text()))
        self.ui.btnNumKeyBackspace.clicked.connect(lambda: self.handleBtn("bkspc"))

        self.ui.btnCamAction.clicked.connect(self.cameraAction)
        self.ui.btnDetailsForm.clicked.connect(self.openDetailsForm)
        self.ui.sliderCamSwitch.valueChanged.connect(self.switchActiveCamera)

    def updateTextMsgUi(self):
        if (self.infoMsgQueue.empty() == False):
            self.ui.lblStatus.setText(str(self.infoMsgQueue.get()))

    def camFinished(self):
        print('Capturing image finished')
        print('Write image start')
        self.writeImageSmb()
        self.infoMsgQueue.put(str(('Enviando imagem...')))
        print('Write image finished')
        self.ui.btnCamAction.setEnabled(True)
        self.infoMsgQueue.put(str(('Concluído')))
        self.infoMsgQueue.put(str(('')))
        
    def switchActiveCamera(self):
        if (self.ui.sliderCamSwitch.value() == 0):
            print("camera default")            
            self.ui.btnCamAction.setIcon(QIcon('camera-pi.png'))
        else:
            print("camera secondary")
            self.ui.btnCamAction.setIcon(QIcon('camera-canon.png'))

    def openDetailsForm(self):
        self.tagPrintUi = FastPicTagWindow()
        self.tagPrintUi.setupUi(self)
        self.tagPrintUi.setLblCaseId(self.ui.lblCaseId.text())
        self.tagPrintUi.showMaximized()

    def cameraAction(self):
        print('Capturing image')
        self.infoMsgQueue.put(str(('Capturando foto...')))
        self.ui.btnCamAction.setEnabled(False)
        self.p = QProcess()
        self.p.finished.connect(self.camFinished)

        if (self.ui.sliderCamSwitch.value() == 0):
            #default cam
            self.p.start("libcamera-still -n -t 200 -o /home/pi/FastPic-PyQt/temp_pic.jpg &")
        else:
            #secondary cam
            os.system('pkill gphoto2 &')
            self.p.start("python", ["capture-image.py"])

    def handleBtn(self,value):
        if value == "bkspc":
            self.ui.lblCaseId.setText(self.ui.lblCaseId.text()[:len(self.ui.lblCaseId.text())-1])
        else:
            self.ui.lblCaseId.setText(self.ui.lblCaseId.text()+value)

    def writeImageSmb(self):
        caseId = self.ui.lblCaseId.text()   #fix me BUG when a filename ends with dot (.). Must sanitize!!
        system_name = configServer.samba['ip']
        conn = SMBConnection(configServer.samba['user'],configServer.samba['password'],"rasp",configServer.samba['name'])
        #logging.debug('START connect SMB')
        try:
            if conn.connect(system_name,139):
                file_obj = open('/home/pi/FastPic-PyQt/temp_pic.jpg', 'rb')
                file_name = time.strftime("%Y%m%d-%H%M%S")

                if caseId != "":
                    svResponse = conn.listPath(configServer.samba['share'], '/', timeout=60)
                    folderExists = False
                    for i in range(len(svResponse)):
                        if svResponse[i].filename == caseId:
                            folderExists = True
                    if not folderExists :
                        conn.createDirectory(configServer.samba['share'],caseId)
                #logging.debug('WRITE file SMB START')
                conn.storeFile(configServer.samba['share'],caseId+'/'+file_name+'.jpg', file_obj)
                #logging.debug('WRITE file SMB END')
                conn.close()
            else :
                #logging.debug('MSG Erro')
                self.infoMsgQueue.put(str(('Erro!')))
                self.infoMsgQueue.put(str(('')))

        except Exception as insta:
            #logging.debug('MSG Erro copiar arquivo')
            print('Erro ao copiar o arquivo')
            self.infoMsgQueue.put(str(('Erro!')))
            self.infoMsgQueue.put(str(('')))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.showMaximized()
    sys.exit(app.exec())
