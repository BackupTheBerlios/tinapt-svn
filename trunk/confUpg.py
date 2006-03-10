# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confUpgrade.ui'
#
# Created: fre mar 10 03:59:36 2006
#      by: The PyQt User Interface Compiler (pyuic) 3.15
#
# WARNING! All changes made in this file will be lost!


from qt import *


class confUpgrade(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("confUpgrade")

        self.setSizeGripEnabled(1)


        self.buttonOk = QPushButton(self,"buttonOk")
        self.buttonOk.setGeometry(QRect(30,100,110,22))
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(0)

        self.buttonCancel = QPushButton(self,"buttonCancel")
        self.buttonCancel.setGeometry(QRect(200,100,110,22))
        self.buttonCancel.setAutoDefault(1)
        self.buttonCancel.setDefault(1)

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setGeometry(QRect(30,60,281,20))

        self.languageChange()

        self.resize(QSize(342,159).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.buttonOk,SIGNAL("clicked()"),self.accept)
        self.connect(self.buttonCancel,SIGNAL("clicked()"),self.reject)


    def languageChange(self):
        self.setCaption(self.__tr("Confirm upgrade!"))
        self.buttonOk.setText(self.__tr("&OK"))
        self.buttonOk.setAccel(QString.null)
        self.buttonCancel.setText(self.__tr("&Cancel"))
        self.buttonCancel.setAccel(QString.null)
        self.textLabel1.setText(self.__tr("<font color=\"#aa0000\"><font size=\"+1\"><b><p align=\"center\">Upgrade these packages?</p></b></font></font>"))


    def __tr(self,s,c = None):
        return qApp.translate("confUpgrade",s,c)
