# CtrlConfig.py
# Class to define content of the config tab.
#
# Change history:
#   20191115:KDT - Original issue

from tkinter import Frame, LabelFrame, Label, Spinbox, Button, Text, StringVar, Radiobutton
import Data_coord
from math import exp
from sympy.solvers import solve
from sympy import Symbol
import scipy.optimize as opt
import time

class CtrlSetup(Frame) :
    def __init__(self, parent, cons, *args, **kwargs) :
        Frame.__init__(self, *args, **kwargs)
        self.cons = cons
        self.parent = parent
        self.buildContent()

    def buildContent(self) :

        MODES = [("ON", "1"),("OFF", "0")]

        self.output = StringVar()

        self.grpSetpoint = LabelFrame(self, text = ' Control Variables ')
        self.grpSetpoint.grid(row=0,column=0, padx=10, pady=10)

        self.label1 = Label(self.grpSetpoint, text = 'SC power:')
        self.label1.grid(row = 0, column = 0, padx = 2, pady = 2, sticky='e')

        self.v1 = StringVar()
        self.v1.set("0") # initialize

        for i in range(2):
            self.rb1 = Radiobutton(self.grpSetpoint, text=MODES[i][0], variable=self.v1, value=MODES[i][1])
            self.rb1.grid(row=0, column=i+1, padx = 2, pady = 2, sticky='w')
       
       
        self.label2 = Label(self.grpSetpoint, text = 'CC  power:')
        self.label2.grid(row = 1, column = 0, padx = 2, pady = 2, sticky='e')

        self.v2 = StringVar()
        self.v2.set("0") # initialize

        for i in range(2):
            self.rb2 = Radiobutton(self.grpSetpoint, text=MODES[i][0], variable=self.v2, value=MODES[i][1])
            self.rb2.grid(row=1, column=i+1, padx = 2, pady = 2, sticky='w')
       
        self.label3 = Label(self.grpSetpoint, text = 'DPG power:')
        self.label3.grid(row = 2, column = 0, padx = 2, pady = 2, sticky='e')

        self.v3 = StringVar()
        self.v3.set("0") # initialize

        for i in range(2):
            self.rb3 = Radiobutton(self.grpSetpoint, text=MODES[i][0], variable=self.v3, value=MODES[i][1])
            self.rb3.grid(row=2, column=i+1, padx = 2, pady = 2, sticky='w')
        
        self.label4 = Label(self.grpSetpoint, text = 'SC T (' +chr(176) + 'C):')
        self.label4.grid(row = 3, column = 0, padx = 2, pady = 2, sticky='e')
        self.sb1 = Spinbox(self.grpSetpoint, from_ = 5, to_ = 50, width = 5)
        self.sb1.grid(row = 3, column = 1, padx = 2, pady = 2, sticky='w')
    
        self.label5 = Label(self.grpSetpoint, text = 'CC T (' +chr(176) + 'C):')
        self.label5.grid(row = 4, column = 0, padx = 2, pady = 2, sticky='e')
        self.sb2 = Spinbox(self.grpSetpoint, from_ = 5, to_ = 50, width = 5)
        self.sb2.grid(row = 4, column = 1, padx = 2, pady = 2, sticky='w')

        self.label6 = Label(self.grpSetpoint, text = 'RH (%):')
        self.label6.grid(row = 5, column = 0, padx = 2, pady = 2, sticky='e')
        self.sb3 = Spinbox(self.grpSetpoint, from_ = 1, to_ = 100, width = 5)
        self.sb3.grid(row = 5, column = 1, padx = 2, pady = 2, sticky='w')

        self.label4 = Label(self.grpSetpoint, text="SC bypass:")
        self.label4.grid(row=6,column=0, padx = 2, pady = 2, sticky='e')

        self.v4 = StringVar()
        self.v4.set("0") # initialize

        for i in range(2):
            self.rb = Radiobutton(self.grpSetpoint, text=MODES[i][0], variable=self.v4, value=MODES[i][1])
            self.rb.grid(row=6, column=i+1, padx = 2, pady = 2, sticky='w')

        self.output_text = Label(self.grpSetpoint, borderwidth=1, width=5, textvariable=self.output)
        self.output_text.grid(row = 7, column = 0, columnspan=2, padx = 2, pady = 2)

        self.box_values = Button(self.grpSetpoint, text="Apply", command=self.send_command)
        self.box_values.grid(row = 8, column = 2, columnspan=1, padx = 2, pady = 2, sticky='w')


    def send_command(self): 

        reply1 = self.cons.send_command_to_PC('s SC_power '+str(int(self.v1.get())))

        time.sleep(2)

        reply2 = self.cons.send_command_to_PC('s CC_power '+str(int(self.v2.get())))

        time.sleep(2)

        reply3 = self.cons.send_command_to_PC('s DPG_power '+str(int(self.v3.get())))

        time.sleep(2)

        reply4 = self.cons.send_command_to_PC('s SC_set '+  self.sb1.get())

        time.sleep(2)

        reply5 = self.cons.send_command_to_PC('s CC_set '+  self.sb2.get())

        time.sleep(2)

        target_pressure = (float(self.sb3.get())/100.0)*self.ph2oSat(float(self.sb1.get()))

        target_TDP = opt.brentq(lambda T: self.ph2oSat_solve(T, target_pressure), -50, 50)

        reply6 = self.cons.send_command_to_PC('s DPG_set '+  str(target_TDP))

        #print(reply2, reply5)

        print(reply1, reply2, reply3, reply4, reply5, reply6)

        #if reply1 == reply2 == reply3 == 'OK':

        #self.output.set("Ok")

        #self.output.set("")

    def ph2oSat_solve(self, T, P):
        return 610.78 * exp((T * 17.2684) / (T + 238.3)) - P

    def ph2oSat(self, T):
        return 610.78 * exp((T * 17.2684) / (T + 238.3))
