import PyQt5.QtWidgets as qt
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QEventLoop, QTimer
from moreWidgets import CheckableComboBox
import pywinauto
from PyQt5 import uic
import sys
import json
import os

# =============================================================================
# Notes
# =============================================================================
# Please use pywinauto Version 0.6.3
# This can be insalled with the command pip install pywinauto==0.6.3

def updateJSON():
    """ Updates instances json file """
    with open("instances.json", "w") as f:
            json.dump({"Paths": paths, "Autoplay": autoSpeed, "Instances": instances}, f, indent = 5)


class Window(qt.QMainWindow):
    
    def __init__(self):
        """ Main Window """
        global instances, paths, autoSpeed
        super(Window, self).__init__()
        uic.loadUi("gui.ui", self)
        
        # Get widgets
        createAction = self.findChild(qt.QAction, "createAction") 
        createAction.triggered.connect(self.createWindow)
        openAction = self.findChild(qt.QAction, "openAction") 
        openAction.triggered.connect(self.openUseWin)
        quitAction = self.findChild(qt.QAction, "quitAction") 
        quitAction.triggered.connect(self.close)
        configAction = self.findChild(qt.QAction, "configAction") 
        configAction.triggered.connect(lambda: self.configWin("configPath"))
        locationAction = self.findChild(qt.QAction, "locationAction") 
        locationAction.triggered.connect(lambda: self.configWin("configPath"))
        autoAction = self.findChild(qt.QAction, "autoAction") 
        autoAction.triggered.connect(lambda: self.configWin("autoplaySettings"))
        
        
        # Load saved instances
        with open("instances.json", "r") as f:
            contents = json.load(f)
            instances = contents["Instances"]
            paths = contents["Paths"]
            autoSpeed = contents["Autoplay"]
            
    def createWindow(self):                                         
        self.w = CreateWindow()
        self.w.show()
        self.hide()
        
    def openUseWin(self):                                         
        self.w = openUseWin()
        self.w.show()
        self.hide()
        
    def configWin(self, option="configPath"):                               
        self.w = configWin(option)
        self.w.show()
        self.hide()
            
                    
class CreateWindow(qt.QMainWindow):
    
    def __init__(self):
        """ Window for creating instances """
        super(CreateWindow, self).__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint) # Remove ? window flag

        uic.loadUi("create.ui", self)
        self.color = "#dadada"
        self.instNo = 1
        
        # Get widgets
        self.selectBox = self.findChild(qt.QComboBox, "selectBox")
        self.symbolEdit = self.findChild(qt.QLineEdit, "symbolEdit")
        addBtn = self.findChild(qt.QPushButton, "addBtn")
        self.createInsBtn = self.findChild(qt.QPushButton, "createInsBtn")
        self.createBox = self.findChild(qt.QGroupBox, "createBox")
        colorButton = self.findChild(qt.QPushButton, "colorButton")
        self.colorLabel = self.findChild(qt.QLabel, "colorLabel")
        manSelect = self.findChild(qt.QPushButton, "manSelect")
        
        # Create Checkable ComboBox
        listBox = self.findChild(qt.QGroupBox, "listBox")
        hbox = qt.QHBoxLayout()
        self.windowsList = CheckableComboBox(self)
        self.windowsList.setEnabled(False)
        hbox.addWidget(self.windowsList)
        listBox.setLayout(hbox)
        
        # Add paths
        for path in sorted(paths):
            self.selectBox.addItem(path)
            
        if paths:
            self.browseInstance()
        
        # Bind Widgets
        self.selectBox.currentTextChanged.connect(self.browseInstance)
        addBtn.clicked.connect(self.addInstance)
        colorButton.clicked.connect(self.changeColor)
        self.createInsBtn.clicked.connect(self.createInstance)
        manSelect.clicked.connect(self.openFileDialog)
        
        self.show()
        
    def closeEvent(self, event):
        """ Run when window gets closed """
        self.w = Window()
        self.w.show()
        self.close()
        
    
    def openFileDialog(self):
        """ Opens file dialog for user to select exe file """
        fname = qt.QFileDialog.getOpenFileName(self, "Select Instance", "C:/",
                                               "EXE files (*.exe);;All files (*.*)")[0]
        self.browseInstance(fname)
        
        
    def browseInstance(self, fname=None):
        """ Open file explorer to select exe file """
        if not fname:
            fname = self.selectBox.currentText()
        self.fname = fname
        self.windowsList.clear()
        # Extract windows
        try:
            app = pywinauto.application.Application().connect(path=self.fname)
            self.dialogs = app.windows(class_name="SCDW_FloatingChart")
            
        except Exception:
            # Show error
            msg = qt.QMessageBox() # Create a message box
            msg.setWindowTitle("Error")
            msg.setText("Application selected is not currently running any additional windows.")
            msg.setIcon(qt.QMessageBox.Critical)
            msg.setStandardButtons(qt.QMessageBox.Ok)
            msg.setDefaultButton(qt.QMessageBox.Ok)
            msg.exec_()
            
        else:
            if self.dialogs:
                # Configure widgets
                self.windowsList.setEnabled(True)
                for dialog in sorted([dialog.window_text() for dialog in self.dialogs]):
                    self.windowsList.addItem(dialog)
                    
    
    def changeColor(self):
        """ Opens color picker """
        color = qt.QColorDialog.getColor() # Opens colour picker window
        if color.isValid():
            self.color = color.name()
            self.colorLabel.setStyleSheet(f"background-color:{self.color}; margin:5px; border:2px solid #000000")
                    
                    
    def addInstance(self):
        """ Checks if criteria is met and then adds instance """
        global instances
        symbol = self.symbolEdit.text()
        winNames = self.windowsList.currentData()
        instNames = [[dialog, "SCDW_FloatingChart"] for dialog in winNames]
        if symbol and winNames:
            # Add instance
            try:
                instances[symbol]
            except Exception:
                instances[symbol] = {}
            instances[symbol][self.fname] = instNames
            instances[symbol]["color"] = self.color
            self.symbolEdit.setEnabled(False)
            self.windowsList.clear()
            self.windowsList.setEnabled(False)
            
            # Enable create button
            self.createInsBtn.setEnabled(True) 
            
            self.instNo += 1
            self.createBox.setTitle(f"Instance {self.instNo}")
            if paths:
                self.browseInstance()
            
    def createInstance(self):
        """ Write JSON file """
        updateJSON()
            
        self.closeEvent(None)
        
        
class openUseWin(qt.QMainWindow):
    
    def __init__(self):
        """ Open window to use saved Instances """
        super(openUseWin, self).__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint) # Remove ? window flag
    
        uic.loadUi("use.ui", self)
        self.isOpen = True
        
        self.useOptions = ["Focus", "Maximise", "Restore", "Auto Play", "Auto Play and Maximise"]
        
        # Get widgets
        self.scrollArea = self.findChild(qt.QScrollArea, "scrollArea")
        self.deleteBox = self.findChild(qt.QComboBox, "deleteBox")
        deleteBtn = self.findChild(qt.QPushButton, "deleteBtn")
        deleteBtn.clicked.connect(self.deleteInstance)
        self.modeBox = self.findChild(qt.QComboBox, "modeBox")
        for option in self.useOptions:
            self.modeBox.addItem(option)
        self.modeBox.currentTextChanged.connect(self.runAutoPlay)
        
        self.insertButtons()
        self.show()
        
    def closeEvent(self, event):
        """ Run when window gets closed """
        self.isOpen = False
        self.w = Window()
        self.w.show()
        
        
    def deleteInstance(self):
        """ Deletes instance """
        global instances
        for instance in instances:
            if instance == self.deleteBox.currentText():
                del instances[instance]
                break
                
        updateJSON()
            
        for button in self.scrollBox.findChildren(qt.QPushButton):
            button.deleteLater()
            
        self.deleteBox.clear()
        self.insertButtons()
    
    
    def insertButtons(self):
        """ Inserts buttons inside of groupbox """
        global instances
        
        # Create layouts
        rowLayout = qt.QHBoxLayout()
        formLayout = qt.QFormLayout()
        self.scrollBox = qt.QGroupBox()
        self.buttonList = []
        rowList, buttonList = [], []
        counter = 6
        
        for instance in instances:
            if counter == 6:
                # Add a new row
                if rowList:
                    formLayout.addRow(rowList[-1])
                rowList.append(qt.QHBoxLayout())
                counter = 0
            
            buttonList.append(qt.QPushButton(instance))
            buttonList[-1].setFont(QFont("Sanserif", 16))
            buttonList[-1].setStyleSheet(f"background-color:{instances[instance]['color']}")
            buttonList[-1].clicked.connect(self.focusWindows)
            rowList[-1].addWidget(buttonList[-1])
            self.deleteBox.addItem(instance)
            self.buttonList.append(buttonList[-1])
            
            counter += 1
        
        if rowList:
            formLayout.addRow(rowList[-1])
                
        self.scrollBox.setLayout(formLayout) # Add form layout to scroll box layout
        self.scrollArea.setWidget(self.scrollBox) # Put groupbox in scroll area
        layout = qt.QVBoxLayout() # Create box layout
        layout.addWidget(self.scrollArea) # Put scroll area in box layout
        
    def focusWindows(self, name=None):
        """ Focus windows of instances """
        global instances

        button_name = None

        if name:
            instance = instances[name]
            button_name = name
        else:
            instance = instances[self.sender().text()]
            button_name = self.sender().text()
        
        option = self.modeBox.currentText()
        for exe in instance:
            if exe != "color":
                app = pywinauto.application.Application().connect(path=exe)
            
                # For application
                for win in instance[exe]:
                    # For window
                    try:
                        a = app.window(title=win[0], class_name=win[1])
                        a.set_focus()
                        #if option in ["Maximise", "Auto Play and Maximise"]:
                        if (button_name.count("-MAX") > 0):
                            a.maximize()
                        #if option == "Restore":
                        if (button_name.count("-RES") > 0):
                            a.restore()
                    except Exception:
                        pass
                        
    def runAutoPlay(self):
        """ Automatically switches between instances """
        counter = 0
        while self.modeBox.currentText() in ["Auto Play", "Auto Play and Maximise"] and self.isOpen:
            loop = QEventLoop()
            self.focusWindows(self.buttonList[counter].text())
            counter += 1
            if counter >= len(self.buttonList):
                counter = 0
            loop = QEventLoop()
            QTimer.singleShot(autoSpeed*1000, loop.quit)
            loop.exec_()
                    
                    
class configWin(qt.QMainWindow):
    
    def __init__(self, option="configPath"):
        """ Open window to use saved Instances """
        super(configWin, self).__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint) # Remove ? window flag
        
        self.configOptions = {"Saved .exe Locations": "configPath",
                              "Autoplay Settings": "autoplaySettings"}
        self.isClose = True
        
        # Call procedure depending on the string passed in
        eval("self." + option + "()")
        
        self.show()
        
    def closeEvent(self, event):
        """ Run when window gets closed """
        if self.isClose:
            self.w = Window()
            self.w.show()
        
    def insertOptions(self, selected):
        """ Inserts config menu options into list widget """
        self.listWidget = self.findChild(qt.QListWidget, "listWidget")
        for option in reversed(self.configOptions):
            self.listWidget.insertItem(-1, option)
        self.listWidget.setCurrentRow(list(self.configOptions.keys()).index(selected))
        self.listWidget.clicked.connect(self.listWidget_clicked)
        
        
    def listWidget_clicked(self):
        """ Calls function depending on selected item """
        item = self.listWidget.currentItem().text()
        self.isClose = False
        self.close()
        self.w = configWin(self.configOptions[item])
        self.isClose = True
        
        
    def deleteItem(self):
        """ Deletes path """
        item = self.pathList.currentItem()
    
        msg = qt.QMessageBox() 
        msg.setWindowTitle("Are you Sure?")
        msg.setText(f"Are you sure you want to delete '{item.text()}' ?") 
        msg.setIcon(qt.QMessageBox.Question)
        msg.setStandardButtons(qt.QMessageBox.Yes|qt.QMessageBox.No) 
        msg.setDefaultButton(qt.QMessageBox.No) 
        msg.buttonClicked.connect(self.confirmDelete)
        x = msg.exec_()
        
        
    def confirmDelete(self, i):
        global paths
        option = i.text()[1:]
        item = self.pathList.currentItem().text()
        
        if option == "Yes":
            paths.remove(item)
            self.insertFilePaths()
            updateJSON()
            
    
    def addNewPath(self):
        global paths
        """ Adds a new exe path """
        fname = qt.QFileDialog.getOpenFileName(self, "Select Instance", "C:/",
                                               "EXE files (*.exe);;All files (*.*)")[0]
        try:
            fname
        except NameError:
            pass
        else:
            # Add path
            if fname:
                paths.append(fname)
                self.insertFilePaths()
                updateJSON()
                
    def insertFilePaths(self):
        """ Inserts filepaths into list widget """
        self.pathList.clear()
        for path in reversed(sorted(paths)):
            self.pathList.insertItem(-1, path)
            
    
    def updateAutoplay(self):
        """ Update json with new autoplay value """
        global autoSpeed
        autoSpeed = self.delayBox.value()
        updateJSON()
        
            
    def configPath(self):
        """ Opens config path selection """
        uic.loadUi("configPath.ui", self)
        self.insertOptions("Saved .exe Locations")
        
        # Load widgets
        addPath = self.findChild(qt.QPushButton, "addPath") 
        addPath.clicked.connect(self.addNewPath)
        self.pathList = self.findChild(qt.QListWidget, "pathList")
        self.pathList.clicked.connect(self.deleteItem)
        
        self.insertFilePaths()
        
    def autoplaySettings(self):
        """ Opens autoplay settings """
        uic.loadUi("configAutoplay.ui", self)
        self.insertOptions("Autoplay Settings")
        
        # Load widgets
        self.delayBox = self.findChild(qt.QSpinBox, "delayBox") 
        self.delayBox.setMinimum(0)
        self.delayBox.setValue(autoSpeed)
        self.delayBox.valueChanged.connect(self.updateAutoplay)
            

if __name__ == "__main__":
    if not os.path.isfile("instances.json"):
         with open("instances.json", "w") as f:
            json.dump({"Paths": [], "Autoplay": 5, "Instances": {}}, f)
    
    app = qt.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())