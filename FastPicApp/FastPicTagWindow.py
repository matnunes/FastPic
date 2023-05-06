from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox)
from PyQt5.QtCore import QDataStream, QIODevice
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket

import time

from PyQt5.uic import loadUi

from FastPicUiTag import Ui_FastPicTagWindow

import MySQLdb as mdb
import configServer

class FastPicTagWindow(QWidget, Ui_FastPicTagWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_FastPicTagWindow()
        self.ui.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.ui.btnExitTagUi.clicked.connect(self.handleBtnExit)
        self.ui.btnPrintTag.clicked.connect(self.handleBtnPrint)
        self.ui.chkSamsung.toggled.connect(lambda:self.btnHandleState(self.ui.chkSamsung))
        self.ui.chkMotorola.toggled.connect(lambda:self.btnHandleState(self.ui.chkMotorola))
        self.ui.chkApple.toggled.connect(lambda:self.btnHandleState(self.ui.chkApple))
        self.ui.chkLG.toggled.connect(lambda:self.btnHandleState(self.ui.chkLG))
        self.ui.chkXiaomi.toggled.connect(lambda:self.btnHandleState(self.ui.chkXiaomi))

    def handleBtnExit(self):
        self.close()
                
    def handleBtnPrint(self):        
        print("printing tag...brrp")
        self.ui.btnPrintTag.setEnabled(False)

        self.tcpSocket = QTcpSocket(self)
        self.tcpSocket.connectToHost(configServer.printer['ip'], configServer.printer['port'], QIODevice.ReadWrite)

        self.blockSize = 0
        self.tcpSocket.waitForConnected(1000)
        # send any message you like it could come from a widget text.
        
        print_data = "^XA^CFE^FO10,09^FDINFO/CELULAR^FS^CFD"
        print_data += "^FO12,37^FDOrgao/Unidade: ^FS"
        print_data += "^FO12,57^FDCaso id:  ^FS"
        print_data += "^XZ"

        self.tcpSocket.write(print_data.encode('utf-8'))
        self.ui.btnPrintTag.setEnabled(True)

    def btnHandleState(self,btnSource):
        deviceMaker = ""
        if (btnSource == self.ui.chkSamsung):
            deviceMaker = 'Samsung'
        if (btnSource == self.ui.chkMotorola):
            deviceMaker = 'Motorola'
        if (btnSource == self.ui.chkApple):
            deviceMaker = 'Apple'
        if (btnSource == self.ui.chkLG):
            deviceMaker = 'LG'
        if (btnSource == self.ui.chkXiaomi):
            deviceMaker = 'Xiaomi'            

        try:
            db = mdb.connect(configServer.mysql['ip'], configServer.mysql['user'], configServer.mysql['password'], configServer.mysql['dbname'])
            print('Connection', 'Database Connected Successfully')
            cursor = db.cursor()
            cursor.execute("SELECT modelo, COUNT(*) AS num from celulares.celular WHERE fabricante LIKE '"+deviceMaker+"' GROUP BY modelo ORDER BY num DESC LIMIT 0,25;")
            rs = cursor.fetchall()

            self.ui.lstDevices.clear()
            self.ui.lstDevices.addItem('-')

            for i in rs:
                self.ui.lstDevices.addItem(i[0])
            db.close()

        except mdb.Error as e:
            print('Connection', 'Failed To Connect Database')

    def setLblCaseId(self,value):
        if value != "":
            self.ui.lblCaseId.setText(value)