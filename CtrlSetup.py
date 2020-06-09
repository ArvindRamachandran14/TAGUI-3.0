# CtrlConfig.py
# Class to define content of the config tab.
#
# Change history:
#   20191115:KDT - Original issue

from tkinter import Frame, LabelFrame, Label, Spinbox, Button, Text, StringVar, Radiobutton, messagebox
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

        PH2O_options = [("RH (%)", "0"),("pH2O (ppt)", "1")]

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

        self.v4 = StringVar()
        self.v4.set("0") # initialize


        self.label6 = Label(self.grpSetpoint, text = 'Set:')
        self.label6.grid(row = 5, column = 0, padx = 2, pady = 2, sticky='e')

        for i in range(2):

            self.rb1 = Radiobutton(self.grpSetpoint, text=PH2O_options[i][0], variable=self.v4, value=PH2O_options[i][1], command=self.pH2O_vs_RH)
            self.rb1.grid(row=5, column=i+1, padx = 2, pady = 2, sticky='w')

        self.label7 = Label(self.grpSetpoint, text = 'RH (%):')
        self.label7.grid(row = 6, column = 0, padx = 2, pady = 2, sticky='e')
        self.sb3 = Spinbox(self.grpSetpoint, from_ = 1, to_ = 100, width = 5)
        self.sb3.grid(row = 6, column = 1, padx = 2, pady = 2, sticky='w')
        self.pH2O_textvariable = StringVar()
        self.label8 = Label(self.grpSetpoint, textvariable=self.pH2O_textvariable)
        self.label8.grid(row = 6, column = 2)

        self.label9 = Label(self.grpSetpoint, text = 'pH2O (ppt):')
        self.label9.grid(row = 7, column = 0, padx = 2, pady = 2, sticky='e')
        self.sb4 = Spinbox(self.grpSetpoint, from_ = 1, to_ = 100, width = 5)
        self.sb4.grid(row = 7, column = 1, padx = 2, pady = 2, sticky='w')
        self.label9.configure(state='disabled')
        self.sb4.configure(state='disabled')
        self.RH_textvariable = StringVar()
        self.label10 = Label(self.grpSetpoint, textvariable=self.RH_textvariable)
        self.label10.grid(row = 7, column = 2)

        self.label11 = Label(self.grpSetpoint, text="SC bypass:")
        self.label11.grid(row=8,column=0, padx = 2, pady = 2, sticky='e')

        self.v5 = StringVar()
        self.v5.set("0") # initialize

        for i in range(2):
            self.rb2 = Radiobutton(self.grpSetpoint, text=MODES[i][0], variable=self.v5, value=MODES[i][1])
            self.rb2.grid(row=8, column=i+1, padx = 2, pady = 2, sticky='w')

        self.output_text = Label(self.grpSetpoint, borderwidth=1, width=5, textvariable=self.output)
        self.output_text.grid(row = 9, column = 0, columnspan=2, padx = 2, pady = 2)

        self.box_values = Button(self.grpSetpoint, text="Apply", command=self.send_command)
        self.box_values.grid(row = 10, column = 2, columnspan=1, padx = 2, pady = 2, sticky='w')

    def pH2O_vs_RH(self):

        if int(self.v4.get()):

            self.label9.configure(state='normal')

            self.sb4.configure(state='normal')

            self.label7.configure(state='disabled')

            self.sb3.configure(state='disabled')


        else:

            self.label7.configure(state='normal')

            self.sb3.configure(state='normal')

            self.label9.configure(state='disabled')

            self.sb4.configure(state='disabled')



    def send_command(self): 

        reply1 = self.cons.send_command_to_PC('s SC_power '+str(int(self.v1.get())))

        time.sleep(2)

        reply2 = self.cons.send_command_to_PC('s CC_power '+str(int(self.v2.get())))

        time.sleep(2)

        reply3 = self.cons.send_command_to_PC('s DPG_power '+str(int(self.v3.get())))

        time.sleep(2)

        if int(self.v1.get()) == 1 and reply1 == 'Done\n':

            reply4 = self.cons.send_command_to_PC('s SC_set '+  self.sb1.get())

            time.sleep(2)

        if int(self.v2.get()) == 1 and reply2 == 'Done\n':

            reply5 = self.cons.send_command_to_PC('s CC_set '+  self.sb2.get())

            time.sleep(2)

        if self.label7.cget('state') == 'normal' and self.label9.cget('state') == 'disabled': #RH input

            RH_input = float(self.sb3.get())

            print("RH_input", RH_input)

            if RH_input >=10 and RH_input <=90: #RH limits

                target_pressure = (RH_input/100.0)*self.ph2oSat(float(self.sb1.get()))

                Cell_pressure = float(self.cons.send_command_to_PC('g CellP').split('---')[0])*1000 #Convert to Pa

                self.pH2O_textvariable.set('pH2O (ppt): ' + str(round((target_pressure/Cell_pressure)*1000,2)))

                self.RH_textvariable.set('')

                target_TDP = opt.brentq(lambda T: self.ph2oSat_solve(T, target_pressure), -50, 50)

                if int(self.v3.get()) == 1 and reply3 == str('Done\n'):

                    reply6 = self.cons.send_command_to_PC('s DPG_set '+  str(target_TDP))

            elif RH_input >=90:

                messagebox.showwarning(title='RH offlimits', message="Condensation Warning")

                self.RH_textvariable.set('')

                self.pH2O_textvariable.set('')

            else:

                messagebox.showwarning(title='RH offlimits', message="Low RH Warning")

                self.RH_textvariable.set('')

                self.pH2O_textvariable.set('')


        elif self.label9.cget('state') == 'normal' and self.label7.cget('state') == 'disabled': # pH2O input

            Cell_pressure = float(self.cons.send_command_to_PC('g CellP').split('---')[0])*1000 #Convert to Pa

            target_pressure = (float(self.sb4.get())/1000.0)*Cell_pressure

            RH_input = (target_pressure/self.ph2oSat(float(self.sb1.get())))*100

            if RH_input >=10 and RH_input <=90: #RH limits

                self.RH_textvariable.set('RH (%): ' + str(round((target_pressure/self.ph2oSat(float(self.sb1.get()))*100),2)))

                self.pH2O_textvariable.set('')

                target_TDP = opt.brentq(lambda T: self.ph2oSat_solve(T, target_pressure), -50, 50)

                if int(self.v3.get()) == 1 and reply3 == str('Done\n'):

                    reply6 = self.cons.send_command_to_PC('s DPG_set '+  str(target_TDP))

            elif RH_input >=90:

                messagebox.showwarning(title='pH2O offlimits', message="Condensation Warning")

                self.RH_textvariable.set('')

                self.pH2O_textvariable.set('')

            else:

                messagebox.showwarning(title='pH2O offlimits', message="Low pH2O warning")

                self.RH_textvariable.set('')

                self.pH2O_textvariable.set('')


    def ph2oSat_solve(self, T, P):
        return 610.78 * exp((T * 17.2684) / (T + 238.3)) - P

    def ph2oSat(self, T):
        return 610.78 * exp((T * 17.2684) / (T + 238.3))
