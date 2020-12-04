import pywinauto
from pywinauto import application
import sys
import winsound
import pyttsx3

#sys.exit(0)

#engine = pyttsx3.init()

app = application.Application().connect(path=r"E:\\SC-TRADING\\SierraChart_64.exe")

#pywinauto.findwindows.enum_windows()

#get all windows titles for SC
#dialogs = app.windows()
#print(dialogs)

#dlg_spec = app.window(title_re=".*#6.*")
#dlg_spec1 = app.window(title_re=".*#4.*")

dlg_spec1 = app.window(title="SC ESZ20_FUT_CME [C][M]  1.00 Range  #1 | E-MINI S&P 500 FUTURES ES Dec 2020 (Dec20)", class_name="SCDW_FloatingChart")

dlg_spec2 = app.window(title="SC ESZ20_FUT_CME [C][M]  3.50 Range  #2 | E-MINI S&P 500 FUTURES ES Dec 2020 (Dec20)", class_name="SCDW_FloatingChart")

dlg_spec3 = app.window(title="SC ESZ20_FUT_CME [C][M]  1.00 Range  #3 | E-MINI S&P 500 FUTURES ES Dec 2020 (Dec20)", class_name="SCDW_FloatingChart")

dlg_spec4 = app.window(title="SC ESZ20_FUT_CME [C][M]  3.50 Range  #4 | E-MINI S&P 500 FUTURES ES Dec 2020 (Dec20)", class_name="SCDW_FloatingChart")

dlg_spec5 = app.window(title="SC ESZ20_FUT_CME [C][M]  1.00 Range  #5 | E-MINI S&P 500 FUTURES ES Dec 2020 (Dec20)", class_name="SCDW_FloatingChart")

dlg_spec6 = app.window(title="SC ESZ20_FUT_CME [C][M]  3.50 Range  #6 | E-MINI S&P 500 FUTURES ES Dec 2020 (Dec20)", class_name="SCDW_FloatingChart")

#dlg_spec1 = app.window(title_re=".*#4.*")

pywinauto.timings.Timings.slow()

#winsound.PlaySound("SystemExit", winsound.SND_ALIAS)



#dlg_spec1.restore()
#dlg_spec1.maximize()

dlg_spec1.set_focus()
dlg_spec1.move_window(1920, 0) # move the window to top-left corner - also for window resize



'''

#dlg_spec2.restore()
#dlg_spec2.maximize()
dlg_spec2.set_focus()

engine.say("Large Scale View  Shown")
engine.runAndWait()

#winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

#dlg_spec3.restore()
#dlg_spec3.maximize()
dlg_spec3.set_focus()

#dlg_spec4.restore()
#dlg_spec4.maximize()
dlg_spec4.set_focus()

engine.say("Small Scale View Shown")
engine.runAndWait()

#winsound.PlaySound("SystemExit", winsound.SND_ALIAS)

#dlg_spec5.restore()
#dlg_spec5.maximize()
dlg_spec5.set_focus()

#dlg_spec6.restore()
#dlg_spec6.maximize()
dlg_spec6.set_focus()

engine.say("Day Trading View Shown")
engine.runAndWait()

'''