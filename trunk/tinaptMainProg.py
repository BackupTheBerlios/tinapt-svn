#!/usr/bin/python2.4
# -*- coding: utf-8 -*-

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
from qt import *
from  tinaptGUI import tinaptMain
from confUpg import  confUpgrade
from searchDialog import searchMethod



__version__ = '0.1a'

class tinaptMainClass(tinaptMain):
    def __init__(self):
        tinaptMain.__init__(self )
        ## Signals ##
        # General
##        self.connect(self.mainTabWidget,SIGNAL("packages()"),self.selectUserInput)
        # Main buttons
        self.connect(self.pbSaveMain, SIGNAL("clicked()"), self.doSaveMain)
        self.connect(self.pbClearMain, SIGNAL("clicked()"), self.doClearMain)
        self.connect(self.pbCancelMain, SIGNAL("clicked()"), self.doCancelMain)
        self.connect(self.mainTextWindow, SIGNAL("textChanged()"), self.doEnableSavePb)
        
        # Sources tab buttons
        self.connect(self.pbUpdatePackages, SIGNAL("clicked()"), self.doUpdateSources)
        self.connect(self.pbEditSources, SIGNAL("clicked()"), self.doEditSources)
        
        # Upgrade tab buttons
        self.connect(self.pbUpgrade, SIGNAL("clicked()"), self.doUpgrade)
        self.connect(self.pbDistUpgrade, SIGNAL("clicked()"), self.doDistUpgrade)
##        self.connect(self.pbSecUpgrade, SIGNAL("clicked()"), self.doSecUpgrade)

       # Packages tab buttons
        self.connect(self.pbSearch, SIGNAL("clicked()"), self.doSearch)
##        self.connect(self.pbShow, SIGNAL("clicked()"), self.doShow)
##        self.connect(self.pbInstall, SIGNAL("clicked()"), self.doInstall)
##        self.connect(self.pbRemove, SIGNAL("clicked()"), self.doRemove)
##        self.connect(self.pbClearCache, SIGNAL("clicked()"), self.doClearCache)
        
        # Set defaults
        self.pbSaveMain.setEnabled(0)
        self.mainTextWindow.setEnabled(0)
        self.sourcesMessage.setEnabled(0)
        self.upgradeMessage.setEnabled(0)
        self.packageUserInput.selectAll()
        
        self.pbSecUpgrade.setEnabled(0) #Temporarily disabled (Need to figure out how to do just a sec upgrade)
        
    def selectUserInput(self):
        self.packageUserInput.selectAll()
        self.packageUserInput.setCursorPosition(0, 0)
    
    def doSaveMain(self):
        # Save sources.list
        if self.mainTabWidget.currentPage() == self.sources:
            writefile = open("sources.list" , "w")
            writefile.write(str(self.mainTextWindow.text()))
            writefile.close()

    def doCancelMain(self):
        
        if self.mainTabWidget.currentPage() == self.upgrade:
            self.commitUpgrade.tryTerminate()
            self.mainTextWindow.append("Canseled by user")
            
    def doClearMain(self):
        self.mainTextWindow.clear()
        self.mainTextWindow.setFocus()
        self.mainTextWindow.setCursorPosition(0, 0)
        self.pbSaveMain.setEnabled(0)
        
    def doEnableSavePb(self):
        if not self.pbSaveMain.isEnabled():
            self.pbSaveMain.setEnabled(1)


    ## Sources tab ## 
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
        self.pbCancelMain.setEnabled(0)
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

        
    ## Upgrade tab ##
    ## Upgrade button **
    def doUpgrade(self):
    # Prepare widgets #
        self.mainTextWindow.setEnabled(1)
        self.mainTextWindow.setReadOnly(0)
        self.upgradeMessage.setEnabled(1)
        self.upgradeMessage.setReadOnly(0)
        self.mainTextWindow.clear()
        self.pbCancelMain.setEnabled(1)
        self.pbSaveMain.setEnabled(0)
        
        self.upgradeMessage.setText("Looking for upgrades, please wait...")
        
        self.upgradeProcess = QProcess()
        self.connect(self.upgradeProcess, SIGNAL("readyReadStdout()"), self.readOutput)
        self.connect(self.upgradeProcess, SIGNAL("processExited()"), self.upgradeProcessExit)
        self.connect(self.upgradeProcess, SIGNAL("readyReadStderr()"), self.readUpgradeErrors)
        self.upgradeProcess.setArguments((QStringList.split(" ", "apt-get upgrade"))) 
        self.upgradeProcess.start()
        
    def readOutput(self):
        outputString = QString(self.upgradeProcess.readStdout())
        self.mainTextWindow.append(outputString)
        
        # Check if upgradeProcess ask to continue
        if outputString.endsWith("? "):
            cr = QString("\n")  # Make a QString carriage return
            qApp.processEvents()
            
            # Isolate the yes character needed for input.
            yesOptionString = outputString.right(6)
            yesOption = yesOptionString.left(1) + cr
            dialog = confUpgrade(self)
            
            # Determine action to take
            if dialog.exec_loop() == QDialog.Accepted:
                self.upgradeMessage.setText("Upgrading packages, please wait...")
                self.upgradeProcess.writeToStdin(yesOption)
            else:
                self.mainTextWindow.append("User terminated")
                self.upgradeProcess.tryTerminate()
                #Kill upgradeProcess if tryTerminate fails
                if self.upgradeProcess.isRunning() == "TRUE":
                    QTimer.singleShot(100, self.upgradeProcessKill())
                    
            ouputString = " "

    def readUpgradeErrors(self):
        self.mainTextWindow.append(QString(self.upgradeProcess.readStderr()))
        
    def upgradeProcessExit(self):
        self.mainTextWindow.append("Operation completed as requested")
        self.upgradeMessage.setText(" ")
        self.upgradeMessage.setEnabled(0)
        
    def upgradeProcessKill(self):
        self.upgradeProcess.kill()
        self.mainTextWindow.append("Operation aborted")
        self.upgradeMessage.setText(" ")
        self.upgradeMessage.setEnabled(0)
    

    ## Dist-upgarde button ##
    def doDistUpgrade(self):
    # Prepare widgets #
        self.mainTextWindow.setEnabled(1)
        self.mainTextWindow.setReadOnly(0)
        self.upgradeMessage.setEnabled(1)
        self.upgradeMessage.setReadOnly(0)
        self.mainTextWindow.clear()
        self.pbCancelMain.setEnabled(1)
        self.pbSaveMain.setEnabled(0)
        
        self.upgradeMessage.setText("Looking for upgrades, please wait...")
        
        self.distUpgradeProcess = QProcess()
        self.connect(self.distUpgradeProcess, SIGNAL("readyReadStdout()"), self.readDistOutput)
        self.connect(self.distUpgradeProcess, SIGNAL("processExited()"), self.distUpgradeProcessExit)
        self.connect(self.distUpgradeProcess, SIGNAL("readyReadStderr()"), self.readDistUpgradeErrors)
        self.distUpgradeProcess.setArguments((QStringList.split(" ", "apt-get dist-upgrade"))) 
        self.distUpgradeProcess.start()
        
    def readDistOutput(self):
        outputString = QString(self.distUpgradeProcess.readStdout())
        self.mainTextWindow.append(outputString)
        
        # Check if upgradeProcess ask to continue
        if outputString.endsWith("? "):
            cr = QString("\n")  # Make QString carriage return
            qApp.processEvents()
            
            # Isolate the yes character needed for input.
            yesOptionString = outputString.right(6)
            yesOption = yesOptionString.left(1) + cr
            dialog = confUpgrade(self)
            
            # Determine action to take
            if dialog.exec_loop() == QDialog.Accepted:
                self.upgradeMessage.setText("Upgrading distrobution, please wait...")
                self.distUpgradeProcess.writeToStdin(yesOption)
            else:
                self.distUpgradeProcess.tryTerminate()
                self.mainTextWindow.append("User terminated")
                #Kill distUpgradeProcess if tryTerminate fails
                if self.distUpgradeProcess.isRunning() == "TRUE":
                    QTimer.singleShot(100, self.distUpgradeProcessKill())
                    
            ouputString = " "

    def readDistUpgradeErrors(self):
        self.mainTextWindow.append(QString(self.distUpgradeProcess.readStderr()))
        
    def distUpgradeProcessExit(self):
        self.mainTextWindow.append("Operation completed as requested")
        self.upgradeMessage.setText(" ")
        self.upgradeMessage.setEnabled(0)
        
    def distUpgradeProcessKill(self):
        self.distUpgradeProcess.kill()
        self.mainTextWindow.append("Operation aborted")
        self.upgradeMessage.setText(" ")
        self.upgradeMessage.setEnabled(0)
    
    ## Packages tab ##
    #search button
    def doSearch(self):
        self.mainTextWindow.setEnabled(1)
        self.mainTextWindow.setReadOnly(0)
        self.pbSaveMain.setEnabled(0)
        
        # Decide search method
        dialog = searchMethod(self)
        if dialog.exec_loop() == QDialog.Accepted:
            self.generalSearch()
        else:
            self.namesOnlySearch()
        
    def generalSearch(self):
        self.mainTextWindow.clear()
        generalCommand = QString("apt-cache search ")
        searchString = generalCommand + self.packageUserInput.text()
        self.searchProcess = QProcess()
        self.connect(self.searchProcess, SIGNAL("readyReadStdout()"), self.readSearchOutput)
        self.connect(self.searchProcess, SIGNAL("processExited()"), self.searchProcessExit)
##        self.connect(self.generalSearch, SIGNAL("readyReadStderr()"), self.searchErrors)
        self.searchProcess.setArguments((QStringList.split(" ", searchString))) 
        self.searchProcess.start()
        
    def namesOnlySearch(self):
        self.mainTextWindow.clear()
        namesOnlyCommand = QString("apt-cache --names-only search ")
        searchString = namesOnlyCommand + self.packageUserInput.text()
        self.searchProcess = QProcess()
        self.connect(self.searchProcess, SIGNAL("readyReadStdout()"), self.readSearchOutput)
        self.connect(self.searchProcess, SIGNAL("processExited()"), self.searchProcessExit)
##        self.connect(self.generalSearch, SIGNAL("readyReadStderr()"), self.searchErrors)
        self.searchProcess.setArguments((QStringList.split(" ", searchString))) 
        self.searchProcess.start()
        
    def readSearchOutput(self):
        self.mainTextWindow.append(QString(self.searchProcess.readStdout()))
        
    def searchProcessExit(self):
        self.mainTextWindow.append("\n Operation completed as requested")
        self.mainTextWindow.setReadOnly(1)
        self.pbSaveMain.setEnabled(0)

    
    

##     Just to quickly test that stuff works ##
##    def doTest(self):
##        print "It works"

if __name__ == "__main__":
# Psyco disabled for testing
##    # Import Psyco if available
##    try:
##        import psyco
##        psyco.full()
##    except ImportError:
##        pass
    app = QApplication(sys.argv)
    f = tinaptMainClass()
    f.show()
    app.setMainWidget(f)
    app.exec_loop()




