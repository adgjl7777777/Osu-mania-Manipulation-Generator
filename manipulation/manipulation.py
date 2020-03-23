# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 21:20:21 2020

@author: Transcendence
"""
import re
import copy as cp
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Anmitsutool.error import *
from Anmitsutool.core import *
from Anmitsutool.ln import *
from Anmitsutool.mashall import *


class SETGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        palette = QPalette()
        palette.setBrush(QPalette.Background,QBrush(QPixmap("background.png")))
        self.setPalette(palette)
        self.fname=""
        self.parts=0
        self.fparts=1
        self.thereitis="./"
        self.fontid1 = QFontDatabase.addApplicationFont("quicksand/Quicksand-Regular.ttf")
        self.fontid2 = QFontDatabase.addApplicationFont("quicksand/Quicksand-Bold.ttf")
        self.desired = [0,2147483647]
        self.snap = [4]
        self.mashmode = [0]
        self.setWindowIcon(QIcon("icon.png"))

        self.inputl = QLabel(".osu File Directory",self)
        self.setbigFont(self.inputl)
        self.inputl.move(30, 40)
 
        self.fd = QLineEdit("",self)        
        self.fd.setPlaceholderText("Enter the File Directory...")
        self.fd.textChanged[str].connect(self.onChanged)
        self.fd.setStyleSheet("background-color: #444444;"
                              "border-style: solid;"
                              "border-width: 2px;"
                              "border-color: White;"
                              "padding: 8px;"
                              "color: White;"
                              "selection-color: White;"
                              "selection-background-color: #444444;"
                              "font-size: 16px;")
        self.fd.textEdited[str].connect(self.dEdited)
        self.fd.editingFinished.connect(self.fEdited)
        self.fd.move(300, 40)
        self.fd.resize(500,38)
        

        self.fo = QPushButton("Open!",self)
        self.fo.clicked.connect(self.fileopen)
        self.setButton(self.fo)
        self.fo.move(830, 40)
            

        self.help = QPushButton("What is Manipulation?",self)
        self.help.clicked.connect(self.modehelp)
        self.setButton(self.help)
        self.help.move(580, 180)

        self.read = QPushButton("Read!",self)
        self.setButton(self.read)
        self.read.move(833, 180)       
        self.read.clicked.connect(self.fileread) 
        
        self.config = QGroupBox("                                        ",self)
        self.config.setFont(QFont(QFontDatabase.applicationFontFamilies(self.fontid1)[0],18))
        self.config.move(60, 130)
        self.config.resize(303,260)
        self.config.setStyleSheet(
                              "border-style: solid;"
                              "spacing: 10;"
                              "border-width: 2px;"
                              "font-weight: Bold;"
                              "border-color: White;"
                              "padding: 8px;"
                              "color: White")

        self.configl = QLabel("Configuration", self)
        self.configl.move(115,114)
        self.setbigFont(self.configl)

        self.conl1 = QLabel("Part", self)
        self.setsmallFont(self.conl1)
        self.conl1.move(80,155)
        self.conl2 = QLabel("Time", self)
        self.setsmallFont(self.conl2)
        self.conl2.move(80,195)
        self.conl3 = QLabel("~", self)
        self.setsmallFont(self.conl3)
        self.conl3.move(240,195)
        self.conl4 = QLabel("Snap      1/", self)
        self.setsmallFont(self.conl4)
        self.conl4.move(80,235)
        self.conl5 = QLabel("Manip mode", self)
        self.setsmallFont(self.conl5)
        self.conl5.move(80,315)

        self.conlb = QComboBox(self)
        self.conlb.setFont(QFont(QFontDatabase.applicationFontFamilies(self.fontid1)[0],12))
        self.conlb.addItem(" Part 1")
        self.conlb.addItem(" Add part...")
        self.conlb.addItem(" Delete part "+str(self.fparts)+"...")
        self.conlb.setStyleSheet("background-color: #444444;"
                                 "border-style: solid;"
                                 "border-width: 2px;"
                                 "border-color: White;"
                                 "color: White;"
                                 "selection-color: White;"
                                 "selection-background-color: #444444")
        self.conlb.move(182,158)
        self.conl1ei = QLineEdit(self)
        self.conl1ei.setValidator(QIntValidator(0,2147483647,self))
        self.setsmallline(self.conl1ei)
        self.conl1ei.move(140,198)
        self.conl1ei.resize(90,26)
        self.conl1ei.setPlaceholderText("0")
        self.conl1ef = QLineEdit(self)
        self.conl1ef.setPlaceholderText("2147483647")
        self.conl1ef.setValidator(QIntValidator(0,2147483647,self))
        self.setsmallline(self.conl1ef)
        self.conl1ef.move(259,198)
        self.conl1ef.resize(90,26)
        self.conl2ei = QLineEdit(self)
        self.conl2ei.setPlaceholderText("4")
        dv = QDoubleValidator(0.0,2147483647.0,1000)
        dv.setNotation(QDoubleValidator.StandardNotation)
        self.conl2ei.setValidator(dv)
        self.setsmallline(self.conl2ei)
        self.conl2ei.move(199,238)
        self.conl2ei.resize(90,26)

        self.conlf1 = QRadioButton("Default",self)
        self.conlf2 = QRadioButton("Left Hand Trill",self)
        self.conlf3 = QRadioButton("Right Hand Trill",self)
        self.settinyFont(self.conlf1)
        self.settinyFont(self.conlf2)
        self.settinyFont(self.conlf3)
        self.conlf1.move(225,290)
        self.conlf2.move(225,320)
        self.conlf3.move(225,350)
        self.conlf1.setChecked(True)
         


        self.conlf1.toggled.connect(self.mode_changed1)
        self.conlf2.toggled.connect(self.mode_changed2)
        self.conlf3.toggled.connect(self.mode_changed3)
        self.conlb.activated.connect(self.part_changed)
        self.conl1ei.textChanged[str].connect(self.timechange1)
        self.conl1ef.textChanged[str].connect(self.timechange2)
        self.conl2ei.textChanged[str].connect(self.snapchange1)
       
        self.resize(960, 420)
        self.setMinimumSize(960,420)
        self.setMaximumSize(960,420)
        self.setWindowTitle("Osu! mania Manipulation Generator by Transcendence(Nausicaa)")
        self.center()
        self.show()

    def modehelp(self):
        self.helper = QMessageBox(self)
        self.helper.setWindowTitle("What is manipulation?")
        self.helper.setIconPixmap(QPixmap("help.png"))
        self.helper.show()

    def setButton(self, target):
        target.setStyleSheet("color: White;"
                             "background-color: #555555;"
                             "font-weight: Bold;"
                             "border-style: solid;"
                             "border-width: 2px;"
                             "border-color: White;"
                             "padding: 6px;")
        target.setFont(QFont(QFontDatabase.applicationFontFamilies(self.fontid1)[0],14))

    def setbigFont(self, target):
        target.setFont(QFont(QFontDatabase.applicationFontFamilies(self.fontid1)[0],20))
        target.setStyleSheet("color: White;"
                                  "font-weight: Bold")
    def setsmallFont(self, target):
        target.setFont(QFont(QFontDatabase.applicationFontFamilies(self.fontid1)[0],15))
        target.setStyleSheet("color: White")

    def settinyFont(self, target):
        target.setFont(QFont(QFontDatabase.applicationFontFamilies(self.fontid1)[0],12))
        target.setStyleSheet("color: White")
    
    def setsmallline(self, target):
        target.setFont(QFont(QFontDatabase.applicationFontFamilies(self.fontid1)[0],14))        
        target.setStyleSheet("background-color: #444444;"
                              "border-style: solid;"
                              "border-width: 2px;"
                              "border-color: White;"
                              "color: White;"
                              "selection-color: White;"
                              "selection-background-color: #444444;"
                              "font-size: 14px;")
    def timechange1(self,text):
        if text != "":
            self.desired[2*self.parts]=int(text)
        else:
            self.desired[2*self.parts]=0
    def timechange2(self,text):
        if text != "":
            self.desired[2*self.parts+1]=int(text)
        else:
            self.desired[2*self.parts+1]=2147483647
    def snapchange1(self,text):
        if text != "" and float(text) ==0:
            self.snap[self.parts]=2147483647
        elif text != "":
            self.snap[self.parts]=float(text)
        else:
            self.snap[self.parts]=4

    def dEdited(self, text):
        self.fd.setStyleSheet("background-color: Black;"
                              "border-style: solid;"
                              "border-width: 2px;"
                              "border-color: White;"
                              "padding: 8px;"
                              "color: White;"
                              "selection-color: White;"
                              "selection-background-color: Black;"
                              "font-size: 16px;")        

    def fEdited(self):
        self.fd.setStyleSheet("background-color: #444444;"
                              "border-style: solid;"
                              "border-width: 2px;"
                              "border-color: White;"
                              "padding: 8px;"
                              "color: White;"
                              "selection-color: White;"
                              "selection-background-color: #444444;"
                              "font-size: 16px;")  
            
    def mode_changed1(self, checked):
        if checked:
            self.mashmode[self.parts] = 0

    def mode_changed2(self, checked):
        if checked:
            self.mashmode[self.parts] = 1
    def mode_changed3(self, checked):
        if checked:
            self.mashmode[self.parts] = 2         

    def part_changed(self, index):
        if index == self.fparts+1:
            if self.fparts == 1:
                QMessageBox.critical(self, "Error", "Can't delete Part 1!")
                self.conlb.setCurrentIndex(0)
                self.conl1ei.setText(str(self.desired[0]))
                self.conl1ef.setText(str(self.desired[1]))
                self.conl2ei.setText(str(self.snap[0]))

                if self.mashmode[0] == 0:
                    self.conlf1.setChecked(True)
                elif self.mashmode[0] == 1:
                    self.conlf2.setChecked(True)
                elif self.mashmode[0] == 2:
                    self.conlf3.setChecked(True)
            else:
                self.conlb.removeItem(self.fparts-1)
                self.conlb.setCurrentIndex(self.fparts-2)
                self.fparts -= 1
                self.conlb.setItemText(self.fparts+1," Delete part "+str(self.fparts)+"...")
                self.parts=self.fparts-1

                del self.desired[-1]
                del self.desired[-1]
                del self.snap[-1]
                del self.mashmode[-1]

                self.conl1ei.setText(str(self.desired[2*(self.fparts-1)]))
                self.conl1ef.setText(str(self.desired[2*(self.fparts-1)+1]))
                self.conl2ei.setText(str(self.snap[self.fparts-1]))
                if self.mashmode[self.fparts-1] == 0:
                    self.conlf1.setChecked(True)
                elif self.mashmode[self.fparts-1] == 1:
                    self.conlf2.setChecked(True)
                elif self.mashmode[self.fparts-1] == 2:
                    self.conlf3.setChecked(True)
        else:
            self.parts=index 
                
            if index == self.fparts:
                self.conlb.setItemText(self.fparts," Part "+str(self.fparts+1))
                self.conlb.setItemText(self.fparts+1," Add part...")
                self.fparts +=1
                self.conlb.addItem(" Delete part "+str(self.fparts)+"...")
                self.desired += [0,2147483647]
                self.snap += [4]
                self.mashmode += [0]
                self.conl1ei.setText("")
                self.conl1ef.setText("")
                self.conl2ei.setText("")
                self.conlf1.setChecked(True)
                
            else:
                self.conl1ei.setText(str(self.desired[2*self.parts]))
                self.conl1ef.setText(str(self.desired[2*self.parts+1]))
                self.conl2ei.setText(str(self.snap[self.parts]))
                if self.mashmode[self.parts] == 0:
                    self.conlf1.setChecked(True)
                elif self.mashmode[self.parts] == 1:
                    self.conlf2.setChecked(True)
                elif self.mashmode[self.parts] == 2:
                    self.conlf3.setChecked(True)
                
    def onChanged(self,text):
        self.fname = text

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def fileread(self):
        self.setWindowTitle("Osu! mania Manipulation Generator by Transcendence(Nausicaa) - Working...")
        try:
            if not self.fname:
                raise fileerror()
            self.targetfile = open(self.fname,"r",encoding="UTF8")
            self.bracket = re.compile(r"(.*\[.*)\]\.osu$")
            self.nobracket = re.compile(r"(.*)\.osu$")
            self.matching = self.bracket.match(self.fname)
            self.matching2 = self.nobracket.match(self.fname)
            if not self.matching and not self.matching2:
                raise fileerror()           
        except Exception:
            if not self.fname:                
                QMessageBox.critical(self, "Error", "Target file is invalid osu! file!")
            elif self.targetfile:
                self.targetfile.close()
                QMessageBox.critical(self, "Error", "Target file is invalid osu! file!")
                self.setWindowTitle("Osu! mania Anmitsu Program by Transcendence(Nausicaa)")
            else:
                QMessageBox.critical(self, "Error", "Target file is invalid osu! file!")
                self.setWindowTitle("Osu! mania Anmitsu Program by Transcendence(Nausicaa)")
                
            return -1
        if self.desired != sorted(self.desired):
            QMessageBox.critical(self, "Error", "Timing points of parts are overlapped!")
            self.setWindowTitle("Osu! mania Anmitsu Program by Transcendence(Nausicaa)")
            return -1
        copier = cp.deepcopy(self.snap)
        for i in range(len(copier)):
            copier[i]=1/copier[i]
        try:
            Mashgenerator(self.matching,self.matching2,self.desired,copier,self.mashmode,self.targetfile)
            result = QMessageBox.information(self, "Information", "Success!")
            if self.targetfile:
                self.targetfile.close()
            if result == QMessageBox.Ok:
                for i in range(self.fparts+2): 
                    self.conlb.removeItem(0)
                self.conlb.setCurrentIndex(0)
                self.conlb.addItem("Part 1")
                self.conlb.addItem("Add part...")
                self.conlb.addItem("Delete Part"+str(self.fparts))
                self.setWindowTitle("Osu! mania Manipulation Generator by Transcendence(Nausicaa)")
                self.fname=""
                self.parts=0
                self.fparts=1      
                self.desired = [0,2147483647] #정렬됨
                self.snap = [4]
                self.mashmode = [0]
                self.conl1ei.setText("")
                self.conl1ef.setText("")
                self.conl2ei.setText("")
                self.fd.setText("")
                self.conlf1.setChecked(True)
                          
        except fileerror:
            if self.targetfile:
                self.targetfile.close()
            QMessageBox.critical(self, "Error", "Target file is invalid osu! file!")
            self.setWindowTitle("Osu! mania Anmitsu Program by Transcendence(Nausicaa)")
            return -1
        except bpmerror:
            if self.targetfile:
                self.targetfile.close()
            QMessageBox.critical(self, "Error", "Target file has no bpm information!")
            self.setWindowTitle("Osu! mania Anmitsu Program by Transcendence(Nausicaa)")
            return -1            
        except modeerror:
            if self.targetfile:
                self.targetfile.close()
            QMessageBox.critical(self, "Error", "Target file is not mania map!")
            self.setWindowTitle("Osu! mania Anmitsu Program by Transcendence(Nausicaa)")
            return -1            
    def fileopen(self):
        self.fo.setStyleSheet("color: White;"
                              "background-color: #777777;"
                              "font-weight: Bold;"
                              "border-style: solid;"
                              "border-width: 2px;"
                              "border-color: White;"
                              "padding: 6px;")
        try:
            self.whereitis = open("whereitis.txt","r",encoding="UTF8")
            self.thereitis = self.whereitis.readline()
            self.whereitis.close()
            if not self.thereitis:
                self.thereitis = "./"
        except Exception:
            self.thereitis = "./"
        self.fname = QFileDialog.getOpenFileName(self,"Open File",self.thereitis,"Osu! Files(*.osu);; All Files(*)")[0]
        self.fo.setStyleSheet("color: White;"
                              "background-color: #555555;"
                              "font-weight: Bold;"
                              "border-style: solid;"
                              "border-width: 2px;"
                              "border-color: White;"
                              "padding: 6px;")
        self.fd.setText(self.fname)
        if self.fname != "":
            self.whereitis = open("whereitis.txt","w",encoding="UTF8")
            isit = re.match(r"(.*)/.*\.osu",self.fname)
            if isit:
                self.whereitis.write(isit.group(1))
                self.whereitis.close()
app = QApplication(sys.argv)
GUI = SETGUI()
sys.exit(app.exec_())