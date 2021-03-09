# Program.py
# Program to implement the User Interface.  This is the startup program.
# It sets up the environment and starts the main application.
import tkinter as tk 
import sys
import json
import global_tech_var as g_tech_instance
import matplotlib.animation as animation
import global_sys_var as g_sys
import global_cal_var as g_cal
import data_coord
import datetime
from mainform import MainForm

def reset_bconnected():
    g_tech_instance.bconnected = "False"
    g_tech_instance.update()

def main(argv) :
    idx = 1
    option = None
    while idx < len(argv) :
        if argv[idx] == 'option' :
            if idx + 1 < len(argv) :
                idx += 1
                option = argv[idx]
        idx += 1

    if not option == None :
        print(option)

    g_sys_instance = g_sys.globals_() #Create an instance of the globals class in the lobal_sys_var module
    g_cal_instance = g_cal.globals_()
    cons = data_coord.consumer(g_sys_instance, g_cal_instance) #consumer object created, global variable object is passed
    reset_bconnected()
    mainForm = MainForm(g_sys_instance, g_cal_instance, cons)

    def apploop():
        if mainForm.connect_btn_text.get() == "Disconnect":
            cons.consume() #indentation removed, consume all the time
            mainForm.status_time_text.set('Run time: ' + str(datetime.timedelta(seconds=round(g_sys_instance.time_list[-1]))))
            mainForm.calibTab.animate_calibration_table()
        mainForm.after(3800, apploop)

    apploop()

    # To create real time plotting of system variables
    ani_temperatures = animation.FuncAnimation(mainForm.tabMon.fig1, mainForm.tabMon.animate_temperatures, interval=1000)
    ani_pressures = animation.FuncAnimation(mainForm.tabMon.fig2, mainForm.tabMon.animate_pressures, interval=1000)
    animate_sw = animation.FuncAnimation(mainForm.tabMon.fig3, mainForm.tabMon.animate_sw, interval=1000)
    ani_calib_temperatures = animation.FuncAnimation(mainForm.calibTab.fig1, mainForm.calibTab.animate_temperatures, interval=1000)
    ani_calib_RH = animation.FuncAnimation(mainForm.calibTab.fig2, mainForm.calibTab.animate_RH, interval=1000)
    mainForm.mainloop()

main(sys.argv)