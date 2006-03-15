# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'searchmethod.ui'
#
# Created: ons mar 15 07:03:50 2006
#      by: The PyQt User Interface Compiler (pyuic) 3.15
#
# WARNING! All changes made in this file will be lost!


from qt import *


class searchMethod(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("searchMethod")

        self.setSizeGripEnabled(1)


        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setGeometry(QRect(50,60,231,20))
        self.textLabel1.setPaletteBackgroundColor(QColor(255,255,255))

        self.buttonOk = QPushButton(self,"buttonOk")
        self.buttonOk.setGeometry(QRect(27,111,141,22))
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(1)

        self.buttonCancel = QPushButton(self,"buttonCancel")
        self.buttonCancel.setGeometry(QRect(174,111,141,22))
        self.buttonCancel.setAutoDefault(1)

        self.languageChange()

        self.resize(QSize(342,164).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.buttonOk,SIGNAL("clicked()"),self.accept)
        self.connect(self.buttonCancel,SIGNAL("clicked()"),self.reject)


    def languageChange(self):
        self.setCaption(self.__tr("Select search method"))
        self.textLabel1.setText(self.__tr("<font size=\"+1\"><p align=\"center\">Please select search method!</p></font>"))
        self.buttonOk.setText(self.__tr("&General"))
        self.buttonOk.setAccel(self.__tr("Alt+G"))
        self.buttonCancel.setText(self.__tr("&Names only"))
        self.buttonCancel.setAccel(self.__tr("Alt+N"))


    def __tr(self,s,c = None):
        return qApp.translate("searchMethod",s,c)
