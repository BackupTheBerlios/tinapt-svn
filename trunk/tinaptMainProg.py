#!/usr/bin/python2.4
### -*- coding: latin1 -*-
#
## ###### Tinapt ########
##
## Copyright (c) 2005 Tina Isaksen
## tina@bestemselv.com
##
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

import sys
import os
import commands
import popen2
from qt import *
from  tinaptGUI import tinaptMain

__version__ = '0.1a'

class tinaptMainClass(tinaptMain):
    def __init__(self):
        tinaptMain.__init__(self )
        # Main buttons
        self.connect(self.pbSaveMain, SIGNAL("clicked()"), self.doSaveMain)
        self.connect(self.pbClearMain, SIGNAL("clicked()"), self.doClearMain)
        self.connect(self.mainTextWindow, SIGNAL("textChanged()"), self.doEnableSavePb)
        
        # Sources tab buttons
        self.connect(self.pbUpdatePackages, SIGNAL("clicked()"), self.doUpdateSources)
        self.connect(self.pbEditSources, SIGNAL("clicked()"), self.doEditSources)
        
        # Upgrade tab buttons
        self.connect(self.pbUpgrade, SIGNAL("clicked()"), self.doUpgrade)
##        self.connect(self.pbDistUpgrade, SIGNAL("clicked()"), self.doDistUpgrade)
##        self.connect(self.pbSecUpgrade, SIGNAL("clicked()"), self.doSecUpgrade)
        
        # Set defaults
        self.pbSaveMain.setEnabled(0)
        self.mainTextWindow.setEnabled(0)
        self.sourcesMessage.setEnabled(0)
        self.upgradeMessage.setEnabled(0)
        
    
    def doSaveMain(self):
        # Save sources.list
        if self.mainTabWidget.currentPage() == self.sources:
            writefile = open("sources.list" , "w")
            writefile.write(str(self.mainTextWindow.text()))
            writefile.close()
            
    def doClearMain(self):
        self.mainTextWindow.clear()
        self.mainTextWindow.setFocus()
        self.mainTextWindow.setCursorPosition(0, 0)
        self.pbSaveMain.setEnabled(0)
        
    def doEnableSavePb(self):
        if not self.pbSaveMain.isEnabled():
            self.pbSaveMain.setEnabled(1)

    # Sources tab 
    def doUpdateSources(self):
        # Prepare widgets #
        self.mainTextWindow.setEnabled(1)
        self.sourcesMessage.setEnabled(1)
        
        self.sourcesMessage.setText("Updating your sources, please wait...")
        qApp.processEvents()
        
        self.updateProcess = QProcess()
        self.connect(self.updateProcess, SIGNAL("readyReadStdout()"), self.readUpdateOutput)
        self.connect(self.updateProcess, SIGNAL("processExited()"), self.updateProcessExit)
        self.updateProcess.setArguments((QStringList.split(" ", "apt-get update")))
        self.updateProcess.start()
        
        
    def readUpdateOutput(self):
        self.mainTextWindow.append(QString(self.updateProcess.readStdout()))
        
    def updateProcessExit(self):
        self.mainTextWindow.append("Done")
        # Return widgets to defaults (foolproofing) #
        self.sourcesMessage.setText(" ")
        self.sourcesMessage.setEnabled(0)
        self.pbSaveMain.setEnabled(0)
        self.mainTextWindow.setReadOnly(1)        

        
    def doEditSources(self):
        # Prepare widgets and variables #
        self.mainTextWindow.setEnabled(1)
        self.mainTextWindow.setReadOnly(0)
        self.pbSaveMain.setEnabled(1)
        
        
        full = " " 
        os.chdir("/etc/apt/")
        tekst = open("sources.list" , "r")
        backup = open("sources.list.bak" , "w")
        
        for pos in tekst:
            full= full + pos
            backup.write(pos)
        tekst.close()
        backup.close()
        self.mainTextWindow.setText(full)
        self.mainTextWindow.scrollToBottom()
        
        # Upgrade tab
    def doUpgrade(self):
    # Prepare widgets #
        self.mainTextWindow.setEnabled(1)
        self.mainTextWindow.setReadOnly(0)
        self.upgradeMessage.setEnabled(1)
        self.upgradeMessage.setReadOnly(0)
        self.mainTextWindow.clear()
        self.pbSaveMain.setEnabled(0)
        
        self.upgradeMessage.setText("Upgrading packages, please wait...")
        
        self.upgradeProcess = QProcess()
        self.connect(self.upgradeProcess, SIGNAL("readyReadStdout()"), self.readOutput)
        self.connect(self.upgradeProcess, SIGNAL("processExited()"), self.upgradeProcessExit)
        self.connect(self.upgradeProcess, SIGNAL("readyReadStderr()"), self.readUpgradeErrors)
        self.upgradeProcess.setArguments((QStringList.split(" ", "apt-get upgrade")))
        self.upgradeProcess.start()



        
    def readOutput(self):
      self.mainTextWindow.append(QString(self.upgradeProcess.readStdout()))
    
    def upgradeProcessExit(self):
        self.mainTextWindow.append("Done!")
        # Return widgets to defaults (foolproofing) #
        self.upgradeMessage.setText(" ")
        self.upgradeMessage.setEnabled(0)
        self.pbSaveMain.setEnabled(0)
        self.mainTextWindow.setReadOnly(1) 
        
    def readUpgradeErrors(self):
        self.mainTextWindow.append(QString(self.upgradeProcess.readStderr()))
      
##        
##    def doTest(self):
##        print "It works"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = tinaptMainClass()
    f.show()
    app.setMainWidget(f)
    app.exec_loop()




