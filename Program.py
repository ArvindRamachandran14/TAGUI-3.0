# Program.py
# Program to implement the User Interface.  This is the startkup program.
# It sets up the environment and starts the main application.

import tkinter as tk 
import sys
import json
import global_tech_var as g_tech_instance
import matplotlib.animation as animation
import CtrlMon
import CtrlMon2
import global_sys_var as g_sys
import Data_coord
import datetime

from MainForm import MainForm

from Calib import Calib


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

        # Read config file
    
    #g_tech_instance = g_tech.globals_()              # Initialize the globals

    g_sys_instance = g_sys.globals_() #Create an instance of the globals class in the lobal_sys_var module

    cons = Data_coord.consumer(g_sys_instance) #consumer object created, global variable object is passed

    reset_bconnected()

    mainForm = MainForm(g_sys_instance, cons)

    def apploop():

        with open('taui.json', 'r') as fCfg : 

            #check if there is ~/.TAGUI file and modify any of the values
            
            config = json.loads(fCfg.read())

            bconnected = config["bconnected"]
    
        
        if mainForm.connect_btn_text.get() == "Disconnect":
    
            #print('Consumption in progress')

            cons.consume() #indentation removed, consume all the time

            mainForm.status_time_text.set('Run time: '+ str(datetime.timedelta(seconds=round(g_sys_instance.time_list[-1]))))

        mainForm.after(2000, apploop)

    apploop()

    ######################## To create real time plotting of system variables #######################

    ani_temperatures = animation.FuncAnimation(mainForm.tabMon.fig1, mainForm.tabMon.animate_temperatures, interval=1000)

    ani_pressures = animation.FuncAnimation(mainForm.tabMon.fig2, mainForm.tabMon.animate_pressures, interval=1000)

    animate_sw = animation.FuncAnimation(mainForm.tabMon.fig3, mainForm.tabMon.animate_sw, interval=1000)

    ani_calib_temperatures_SC = animation.FuncAnimation(mainForm.calibTab.fig1, mainForm.calibTab.animate_temperatures, interval=1000)

    #ani_calib_temperatures_CC = animation.FuncAnimation(mainForm.calibTab.fig2, mainForm.calibTab.animate_temperatures, interval=1000)

    #ani_calib_temperatures = animation.FuncAnimation(mainForm.calibTab.fig3, mainForm.calibTab.animate_temperatures, interval=1000)

    mainForm.mainloop()

# Actual main program

main(sys.argv)
