import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui

import os
import PySide2

import pywinauto
from pywinauto import application
import sys
import winsound
import pyttsx3

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

from PySide2.QtWidgets import *

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        engine = pyttsx3.init()

        app = application.Application().connect(path=r"E:\\SC-TRADING\\SierraChart_64.exe")

        # pywinauto.findwindows.enum_windows()

        # get all windows titles for SC
        # dialogs = app.windows()
        # print(dialogs)

        # dlg_spec = app.window(title_re=".*#6.*")
        # dlg_spec1 = app.window(title_re=".*#4.*")

        dlg_spec1 = app.window(
            title="SC ESZ20_FUT_CME [C][M]  1.00 Range  #1 | E-MINI S&P 500 FUTURES ES Dec 2020 (Dec20)",
            class_name="SCDW_FloatingChart")

        dlg_spec2 = app.window(
            title="SC ESZ20_FUT_CME [C][M]  3.50 Range  #2 | E-MINI S&P 500 FUTURES ES Dec 2020 (Dec20)",
            class_name="SCDW_FloatingChart")

        dlg_spec3 = app.window(
            title="SC ESZ20_FUT_CME [C][M]  1.00 Range  #3 | E-MINI S&P 500 FUTURES ES Dec 2020 (Dec20)",
            class_name="SCDW_FloatingChart")

        dlg_spec4 = app.window(
            title="SC ESZ20_FUT_CME [C][M]  3.50 Range  #4 | E-MINI S&P 500 FUTURES ES Dec 2020 (Dec20)",
            class_name="SCDW_FloatingChart")

        dlg_spec5 = app.window(
            title="SC ESZ20_FUT_CME [C][M]  1.00 Range  #5 | E-MINI S&P 500 FUTURES ES Dec 2020 (Dec20)",
            class_name="SCDW_FloatingChart")

        dlg_spec6 = app.window(
            title="SC ESZ20_FUT_CME [C][M]  3.50 Range  #6 | E-MINI S&P 500 FUTURES ES Dec 2020 (Dec20)",
            class_name="SCDW_FloatingChart")

        # dlg_spec1 = app.window(title_re=".*#4.*")

        pywinauto.timings.Timings.slow()

        # winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

        # dlg_spec1.restore()
        # dlg_spec1.maximize()
        dlg_spec1.set_focus()
        dlg_spec1.move_window(1920, 0)



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())