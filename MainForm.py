# -*- coding: utf-8 -*-
# Mainform.py
# Build the main form.
# This is the topleel of the GUI tree.
#
# 20191112: KDT = Original issue

import tkinter as tk
from tkinter import Tk, ttk, Frame, Menu, Menubutton, Button, Label, StringVar, OptionMenu, filedialog
import sys
from datetime import datetime
import CtrlSetup
import CtrlMon
import CtrlMon2
import global_tech_var as g_tech_instance
import CtrlTerm
import CtrlCfg
import serial
import time
import Calib
#import TADAQ
import Data_coord
import json
import difflib

class MainForm(Tk) :
    
    def __init__(self, g_sys_instance, cons, *args, **kwargs) :
        

        tk.Tk.__init__(self, *args, **kwargs) 


        tk.Tk.wm_title(self, 'Main Window') #window title

        self.grid_rowconfigure(0, weight=1)  #Let the window fill out when resizing
        self.grid_columnconfigure(0, weight=1)  #Let the window fill out when resizing

        container = tk.Frame(self) #main frame
        
        container.grid(row=0, column=0, sticky=tk.E+tk.W+tk.S+tk.N) # Let the main frame fill out the entire window

        container.grid_rowconfigure(1, weight=1) # Notebook sits in row 1 and it should occupy any empty space left
        container.grid_columnconfigure(0, weight=1) # Makes sure there is no empty space in the horizontal direction

        self.g_sys_instance = g_sys_instance
        self.cons = cons

        self.minsize(height = 700, width = 1024) # setting window size
        self.protocol("WM_DELETE_WINDOW", self.onClosing) 
        self.connect_btn_text = StringVar()
        self.buildMenuBar(container)
        self.buildserialBar(container)
        self.buildCtrlTab(container)
        self.buildStatusBar(container)
        self.ctrlTab.select(self.tabSetup)
        self.dat_buf = []

        #self.dcoord = DCoord(Rec_num) # This is renaming the consumer class 

        #self.cmd = ''

        #self.parm = ''

    def buildMenuBar(self, container) :
        # Menu
        menuBar = tk.Menu(container)
        fileMenu = tk.Menu(menuBar, tearoff=0)
        fileMenu.add_command(label='New', command=self.onFileNew)
        fileMenu.add_command(label='Open...', command=self.onFileOpen)
        fileMenu.add_separator()
        fileMenu.add_command(label='Save', command=self.onFileNew)
        fileMenu.add_command(label='Save as', command=self.onFileOpen)
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit', command=self.onFileExit)
        menuBar.add_cascade(label='File', menu=fileMenu)
        tk.Tk.config(self, menu = menuBar)

    #Build serial bar - lets the user choose the serial port, baud rate and establish connection through a "connect" button


    def buildserialBar(self, container):

        serial_port = StringVar()

        baud_rate = StringVar()

        self.serialBar = tk.Frame(container, relief=tk.SUNKEN)

        self.serialBar.grid(row=0, column=0) # Serial bar is positioned at the top row of the frame

        choose_mode_list = ["TA Experiment", "TA Simulation"]

        self.choose_mode_label = Label(self.serialBar, text="Mode") 

        self.choose_mode_label.grid(row=0, column=0)

        self.choose_mode_variable = StringVar()

        self.choose_mode_widget = OptionMenu(self.serialBar, self.choose_mode_variable, *choose_mode_list, command=self.set_mode)

        self.choose_mode_widget.grid(row=0, column=1)

        self.choose_mode_variable.set("TA Simulation")

        self.serial_port_label = Label(self.serialBar, text="Port") 

        self.serial_port_label.grid(row=0, column=2)

        tty_list = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/tty.usbserial-FTY3UOSS"]

        self.tty_variable = StringVar()

        self.tty_variable.set(g_tech_instance.tty)

        self.serial_port_widget = OptionMenu(self.serialBar, self.tty_variable, *tty_list, command=self.update_json_file)

        self.serial_port_widget.grid(row=0, column=3)

        self.baud_rate_label = Label(self.serialBar, text="Baud")

        self.baud_rate_label.grid(row=0, column=4)

        baud_rate_list = ["9600", "19200", "115200"]

        self.baud_rate_variable = StringVar()

        self.baud_rate_variable.set(g_tech_instance.baud_rate)

        self.baud_rate_list = OptionMenu(self.serialBar, self.baud_rate_variable, *baud_rate_list, command=self.update_json_file)

        self.baud_rate_list.grid(row=0, column=5)        

        self.button = Button(self.serialBar, textvariable=self.connect_btn_text, command=self.connect)
        
        self.connect_btn_text.set("Connect")

        self.button.grid(row=0, column=6)

        #self.button = Button(self.serialBar, textvariable=self.log_btn_text, command=self.log_data)

        #self.log_btn_text.set("log data")

        #self.button.grid(row=0, column=5)

        #print(self.connect_btn_text.get())

    # buildStatusBar
    # Make the status bar on the bottom of the screen.  This has
    # a text status message on the left and the experiment time on
    # the right.  The time is not being updated in this prototype code.


    def buildStatusBar(self, container):

        self.status_label_text = StringVar()

        self.status_time_text = StringVar()

        statusBar = tk.Frame(container, relief=tk.SUNKEN, bd=2)

        statusBar.grid(row=2, column=0, sticky=tk.E+tk.W) #Status bar is positioned at the bottom and extends fully horizontally
 
        self.status_label =  Label(statusBar, textvariable=self.status_label_text)

        self.status_label_text.set('Idle')

        self.status_label.pack(side=tk.LEFT)

        self.status_time = Label(statusBar, textvariable=self.status_time_text)

        self.status_time_text.set('Run time: NA')

        self.status_time.pack(side=tk.RIGHT)


    def buildCtrlTab(self, container) :
        
        ################# Hosts the different tabs such as SetUp, Monitor, Terminal, and Config #################
        
        self.ctrlTab = ttk.Notebook(container)
        self.tabSetup = CtrlSetup.CtrlSetup(self.ctrlTab, self.cons, self.g_sys_instance)
        self.ctrlTab.add(self.tabSetup, text = 'Setup')
        self.tabMon = CtrlMon.CtrlMon(self.ctrlTab, self.g_sys_instance, self.cons, self)
        self.tabMon2 = CtrlMon2.CtrlMon2(self.ctrlTab, self.g_sys_instance)

        self.ctrlTab.add(self.tabMon, text = 'Monitor')

        #self.ctrlTab.add(self.tabMon2, text = 'Monitor 2')

        self.tabTerm = CtrlTerm.CtrlTerm(self.ctrlTab, self.g_sys_instance, self.cons)
        self.ctrlTab.add(self.tabTerm, text = 'Terminal')
        self.tabCfg = CtrlCfg.CtrlCfg(self.ctrlTab)
        self.calibTab = Calib.Calib(self.ctrlTab,  self.g_sys_instance, self.cons)
        self.ctrlTab.add(self.calibTab, text = 'Calibration')
        self.ctrlTab.grid(row=1, column=0, sticky=tk.E+tk.W+tk.S+tk.N)

    def set_mode(self, event):

        #print('\n'.join(difflib.Differ().compare("TA Experiment", self.choose_mode_variable.get())))

        if self.choose_mode_variable.get() == "TA Experiment":

            self.g_sys_instance.bsimulation = False

        elif self.choose_mode_variable.get() == "TA Simulation":

            self.g_sys_instance.bsimulation = True

    def update_json_file(self, event):

        #### Gets the updated serial port and baud rate and alls the function to update the json file with the latest parameters ####

        g_tech_instance.baud_rate = self.baud_rate_variable.get()

        g_tech_instance.tty = self.tty_variable.get()

        g_tech_instance.update()

    def connect(self):

        time_out = 3

        if str(self.connect_btn_text.get()) == "Connect":

            self.cons.Connect(self, self.tabMon, self.tty_variable.get(), self.baud_rate_variable.get(), str(time_out)) #Send all variables regardless of operation mode

        elif str(self.connect_btn_text.get()) == "Disconnect":

            self.cons.Disconnect(self, self.tabMon)

            self.connect_btn_text.set("Connect")

        time.sleep(4)

    def onFileNew(self):
        
        filename  = filedialog.asksaveasfilename(initialdir = "./",title = "Select file",filetypes = (("xml files","*.xml"), ("csv files","*.csv"), ("all files","*.*")))

        if filename != '':

            self.cons.f = open(filename, "w+")


    def onFileOpen(self) :

        ftypes = [('xml files', '*.xml'), ("csv files","*.csv"), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes = ftypes)
        filename = dlg.show()

        if filename != '':

            self.cons.f = open(filename, "a")


        #popupmsg("Not Implemented")

    def onFileExit(self) :
        # Need to do cleanup here, save files, etc. before quitting.
        # quit()
        self.destroy()

    def onClosing(self) :
        self.onFileExit()

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Information")
    label = ttk.Label(popup, text=msg)
    #label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    #B1.pack()
    popup.mainloop()

