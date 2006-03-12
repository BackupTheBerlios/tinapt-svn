# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confUpgrade.ui'
#
# Created: søn mar 12 08:56:51 2006
#      by: The PyQt User Interface Compiler (pyuic) 3.15
#
# WARNING! All changes made in this file will be lost!


from qt import *

image0_data = [
"40 40 6 1",
"d c #000000",
". c #6e6e6e",
"# c #bebebe",
"a c #cba0a0",
"b c #fc0000",
"c c #ff0000",
"........................................",
".######################################.",
".######################################.",
".######################################.",
".######################################.",
".#################aaa##################.",
".################abbba#################.",
".###############abbcbca################.",
".###############abaaaba################.",
".##############abba#abca###############.",
".##############aba###aba###############.",
".#############abba###abca##############.",
".#############aba##d##aba##############.",
".############abba#ddd#abca#############.",
".############aba##ddd##aba#############.",
".###########abba##ddd##abca############.",
".###########aba###ddd###aba############.",
".##########abba###ddd###abca###########.",
".##########aba####ddd####aba###########.",
".#########abba####ddd####abca##########.",
".#########aba#####ddd#####aba##########.",
".########abba#####ddd#####abca#########.",
".########aba######ddd######aba#########.",
".#######abba######ddd######abca########.",
".#######aba########d########aba########.",
".######abba#################abca#######.",
".######aba#########d#########aba#######.",
".#####abba########ddd########abca######.",
".#####aba########ddddd########aba######.",
".####abba#########ddd#########abca#####.",
".####aba###########d###########aba#####.",
".###abbaaaaaaaaaaaaaaaaaaaaaaaaabba####.",
".###abbbbbbbbbbbbbbbbbbbbbbbbbbbbba####.",
".####abbbbbbbbbbbbbbbbbbbbbbbbbbba#####.",
".#####aaaaaaaaaaaaaaaaaaaaaaaaaaa######.",
".######################################.",
".######################################.",
".######################################.",
".######################################.",
"........................................"
]

class confUpgrade(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        self.image0 = QPixmap(image0_data)

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

        self.pixmapLabel2 = QLabel(self,"pixmapLabel2")
        self.pixmapLabel2.setGeometry(QRect(140,10,60,50))
        self.pixmapLabel2.setPixmap(self.image0)
        self.pixmapLabel2.setScaledContents(1)

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
        self.textLabel1.setText(self.__tr("<font face=\"Arial\"><font size=\"+1\"><p align=\"center\">Upgrade these packages?</p></font></font>"))


    def __tr(self,s,c = None):
        return qApp.translate("confUpgrade",s,c)
