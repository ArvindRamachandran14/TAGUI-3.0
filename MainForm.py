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
import ctrl_setup
import ctrl_mon
import global_tech_var as g_tech_instance
import ctrl_term
import serial
import time
import calib
#import TADAQ
import data_coord
import json
import difflib
import xml.etree.ElementTree as ET 


class MainForm(Tk) :

    """class to build and add functionality to the main page of TAGUI"""

    def __init__(self, g_sys_instance, g_cal_instance, cons, *args, **kwargs) :
        tk.Tk.__init__(self, *args, **kwargs) 
        tk.Tk.wm_title(self, 'Main Window') #window title
        self.grid_rowconfigure(0, weight=1)  #Let the window fill out when resizing
        self.grid_columnconfigure(0, weight=1)  #Let the window fill out when resizing

        container = tk.Frame(self) #main frame
        container.grid(row=0, column=0, sticky=tk.E+tk.W+tk.S+tk.N) # Let the main frame fill out the entire window
        container.grid_rowconfigure(1, weight=1) # Notebook sits in row 1 and it should occupy any empty space left
        container.grid_columnconfigure(0, weight=1) # Makes sure there is no empty space in the horizontal direction

        self.g_sys_instance = g_sys_instance
        self.g_cal_instance = g_cal_instance
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
        self.filename = ''

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

    # Serial bar is at the top of the window and lets the user choose between experiment/simulation mode, the serial port, the baud rate and connect/disconnect to the ThermoAnalyzer
    def buildserialBar(self, container):

        serial_port = StringVar()
        baud_rate = StringVar()
        self.serialBar = tk.Frame(container, relief=tk.SUNKEN)
        self.serialBar.grid(row=0, column=0, sticky='w') # Serial bar is positioned at the top row of the frame
        choose_mode_list = ["TA Experiment", "TA Simulation"]
        self.choose_mode_label = Label(self.serialBar, text="Mode") 
        self.choose_mode_label.grid(row=0, column=0)
        self.choose_mode_variable = StringVar()
        self.choose_mode_widget = OptionMenu(self.serialBar, self.choose_mode_variable, *choose_mode_list, command=self.set_mode)
        self.choose_mode_widget.config(width=11)#, direction='left')
        self.choose_mode_widget.grid(row=0, column=1, sticky='w')
        self.choose_mode_variable.set("TA Experiment")
        self.g_sys_instance.bsimulation = False
        self.serial_port_label = Label(self.serialBar, text="Port") 
        self.serial_port_label.grid(row=0, column=2)

        tty_list = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/tty.usbserial-FTY3UOSS"]
        self.tty_variable = StringVar()
        self.tty_variable.set(g_tech_instance.tty)
        self.serial_port_widget = OptionMenu(self.serialBar, self.tty_variable, *tty_list, command=self.update_json_file)
        self.serial_port_widget.config(width=21)#, justify='left')
        self.serial_port_widget.grid(row=0, column=3)
        self.baud_rate_label = Label(self.serialBar, text="Baud")
        self.baud_rate_label.grid(row=0, column=4)
        baud_rate_list = ["9600", "19200", "115200"]
        self.baud_rate_variable = StringVar()
        self.baud_rate_variable.set(g_tech_instance.baud_rate)
        self.baud_rate_list = OptionMenu(self.serialBar, self.baud_rate_variable, *baud_rate_list, command=self.update_json_file)
        self.baud_rate_list.config(width=6)
        self.baud_rate_list.grid(row=0, column=5)        
        self.button = Button(self.serialBar, textvariable=self.connect_btn_text, command=self.connect)
        self.connect_btn_text.set("Connect")
        self.button.grid(row=0, column=6)

    #Status bar is at the bottom of the window and text status message on the left and the experiment time on the right

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

    # CtrlTab hosts the different tabs such as SetUp, Monitor, Terminal, and Config 

    def buildCtrlTab(self, container) :

        s = ttk.Style()
        s.configure('TNotebook', tabposition='nw')

        self.ctrlTab = ttk.Notebook(container)
        self.ctrlTab.grid(row=1, column=0)#tk.E+tk.W+tk.S+tk.N)
        self.ctrlTab.bind("<<NotebookTabChanged>>", self.display_tab_selected)
        self.tabSetup = ctrl_setup.CtrlSetup(self.ctrlTab, self.cons, self.g_sys_instance, self.g_cal_instance)
        self.ctrlTab.add(self.tabSetup, text = 'Setup')
        self.tabMon = ctrl_mon.CtrlMon(self.ctrlTab, self.g_sys_instance, self.cons, self)
        self.ctrlTab.add(self.tabMon, text = 'Monitor')
        self.tabTerm = ctrl_term.CtrlTerm(self.ctrlTab, self.g_sys_instance, self.cons)
        self.ctrlTab.add(self.tabTerm, text = 'Terminal')
        self.calibTab = calib.Calib(self.ctrlTab,  self.g_sys_instance, self.g_cal_instance, self.cons)
        self.ctrlTab.add(self.calibTab, text = 'Calibration')
    
    #Function to update the tables in the tab selected by the user
    def display_tab_selected(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if tab_text == "Calibration":
            self.calibTab.update_calibration_table()

        elif tab_text == "Setup":
            self.tabSetup.update_setup_table()

    def set_mode(self, event):

        if self.choose_mode_variable.get() == "TA Experiment":
            self.g_sys_instance.bsimulation = False

        elif self.choose_mode_variable.get() == "TA Simulation":
            self.g_sys_instance.bsimulation = True

    #Function to get the updated serial port and baud rate and call the function to update the json file with the latest parameters
    def update_json_file(self, event):
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
        
        self.filename  = filedialog.asksaveasfilename(initialdir = "./",title = "Select file",filetypes = (("xml files","*.xml"), ("csv files","*.csv"), ("all files","*.*")))
        if self.filename != '':
            self.cons.f = open(self.filename, "wb")
            self.cons.f_TAdata = open(self.filename[:-4] +"_TAdata.xml", "wb")
            self.cons.f_Caldata = open(self.filename[:-4] +"_Caldata.xml", "wb")
            self.cons.f_Commands_to_PC = open(self.filename[:-4] +"_Commands_to_PC.xml", "wb")

            root_main = ET.Element("TADataLog") 
            tree_main = ET.ElementTree(root_main) 
            root_TAdata = ET.Element("TAData") 
            tree_TAdata = ET.ElementTree(root_TAdata)
            m2 = ET.Element("CalData") 
            m3 = ET.Element("Commands") 
            tree_main.write(self.cons.f)
            tree_TAdata.write(self.cons.f_TAdata)

    def onFileOpen(self) :

        ftypes = [('xml files', '*.xml'), ("csv files","*.csv"), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes = ftypes)
        self.filename = dlg.show()
        if self.filename != '':
            self.cons.f = open(self.filename, "a")

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
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    popup.mainloop()