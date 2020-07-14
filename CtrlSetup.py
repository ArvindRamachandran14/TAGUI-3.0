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
    def __init__(self, parent, cons, g_sys_instance, *args, **kwargs) :
        Frame.__init__(self, *args, **kwargs)
        self.cons = cons
        self.parent = parent
        self.g_sys_instance = g_sys_instance
        self.buildContent()

    def buildContent(self) :

        MODES = [("ON", "1"),("OFF", "0")]

        PH2O_options = [("RH (%)", "0"),("pH2O (ppt)", "1")]

        self.output = StringVar()

        self.SCgrpSetpoint = LabelFrame(self, text = ' SC Control Variables ')
        self.SCgrpSetpoint.grid(row=0,column=0, padx=10, pady=10, sticky='N')

        self.label_SC_power = Label(self.SCgrpSetpoint, text = 'SC power:')
        self.label_SC_power.grid(row = 0, column = 0, padx = 2, pady = 2, sticky='e')

        self.v_SC_power = StringVar()
        self.v_SC_power.set("0") # initialize

        for i in range(2):
            self.rb_SC_power = Radiobutton(self.SCgrpSetpoint, text=MODES[i][0], variable=self.v_SC_power, value=MODES[i][1])
            self.rb_SC_power.grid(row=0, column=i+1, padx = 2, pady = 2, sticky='w')
       
        self.label_SC_set = Label(self.SCgrpSetpoint, text = 'SC T (' +chr(176) + 'C):')
        self.label_SC_set.grid(row = 1, column = 0, padx = 2, pady = 2, sticky='e')
        
        self.sb_SC_set = Spinbox(self.SCgrpSetpoint, from_ = 5, to_ = 50, width = 5)
        self.sb_SC_set.grid(row = 1, column = 1, padx = 2, pady = 2, sticky='w')

        self.label_SC_bypass = Label(self.SCgrpSetpoint, text="SC bypass:")
        self.label_SC_bypass.grid(row=2,column=0, padx = 2, pady = 2, sticky='e')

        self.v_SC_bypass = StringVar()
        self.v_SC_bypass.set("0") # initialize

        for i in range(2):
            self.rb_SC_bypass = Radiobutton(self.SCgrpSetpoint, text=MODES[i][0], variable=self.v_SC_bypass, value=MODES[i][1])
            self.rb_SC_bypass.grid(row=2, column=i+1, padx = 2, pady = 2, sticky='w')

        #self.output_text = Label(self.grpSetpoint, borderwidth=1, width=5, textvariable=self.output)
        #self.output_text.grid(row = 9, column = 0, columnspan=2, padx = 2, pady = 2)

        self.box_values_SC = Button(self.SCgrpSetpoint, text="Apply", command=self.send_SC_command)
        self.box_values_SC.grid(row = 3, column = 2, columnspan=1, padx = 2, pady = 2, sticky='w')

        self.CCgrpSetpoint = LabelFrame(self, text = ' CC Control Variables ')
        self.CCgrpSetpoint.grid(row=0,column=1, padx=10, pady=10, sticky='N')

        self.label_CC_power = Label(self.CCgrpSetpoint, text = 'CC  power:')
        self.label_CC_power.grid(row = 0, column = 0, padx = 2, pady = 2, sticky='e')

        self.v_CC_power = StringVar()
        self.v_CC_power.set("0") # initialize

        for i in range(2):
            self.rb_CC_power = Radiobutton(self.CCgrpSetpoint, text=MODES[i][0], variable=self.v_CC_power, value=MODES[i][1])
            self.rb_CC_power.grid(row=0, column=i+1, padx = 2, pady = 2, sticky='w')

        self.label_CC_set = Label(self.CCgrpSetpoint, text = 'CC T (' +chr(176) + 'C):')
        self.label_CC_set.grid(row = 1, column = 0, padx = 2, pady = 2, sticky='e')

        self.sb_CC_set = Spinbox(self.CCgrpSetpoint, from_ = 5, to_ = 50, width = 5)
        self.sb_CC_set.grid(row = 1, column = 1, padx = 2, pady = 2, sticky='w')

        self.box_values_SC = Button(self.CCgrpSetpoint, text="Apply", command=self.send_CC_command)
        self.box_values_SC.grid(row = 2, column = 2, columnspan=1, padx = 2, pady = 2, sticky='w')

        self.pH2OgrpSetpoint = LabelFrame(self, text = ' pH2O Control Variables ')
        self.pH2OgrpSetpoint.grid(row=0,column=2, padx=10, pady=10, sticky='N')

        self.pH2OgrpSetpoint = LabelFrame(self, text = ' pH2O Control Variables ')
        self.pH2OgrpSetpoint.grid(row=0,column=2, padx=10, pady=10)
       
        self.label_DPG_Power = Label(self.pH2OgrpSetpoint, text = 'DPG power:')
        self.label_DPG_Power.grid(row = 0, column = 0, padx = 2, pady = 2, sticky='e')

        self.v_DPG_power = StringVar()
        self.v_DPG_power.set("0") # initialize

        for i in range(2):
            self.rb_DPG_power = Radiobutton(self.pH2OgrpSetpoint, text=MODES[i][0], variable=self.v_DPG_power, value=MODES[i][1])
            self.rb_DPG_power.grid(row=0, column=i+1, padx = 2, pady = 2, sticky='w')

        self.label_pH2O_toggle = Label(self.pH2OgrpSetpoint, text = 'Set:')
        self.label_pH2O_toggle.grid(row = 1, column = 0, padx = 2, pady = 2, sticky='e')

        self.v_pH2O_toggle = StringVar()
        self.v_pH2O_toggle.set("0") # initialize

        for i in range(2):

            self.rb_pH2O_toggle = Radiobutton(self.pH2OgrpSetpoint, text=PH2O_options[i][0], variable=self.v_pH2O_toggle, value=PH2O_options[i][1], command=self.pH2O_vs_RH)
            self.rb_pH2O_toggle.grid(row=1, column=i+1, padx = 2, pady = 2, sticky='w')

        self.label_RH_set = Label(self.pH2OgrpSetpoint, text = 'RH (%):')
        self.label_RH_set.grid(row = 2, column = 0, padx = 2, pady = 2, sticky='e')

        self.sb_RH_set = Spinbox(self.pH2OgrpSetpoint, from_ = 1, to_ = 100, width = 5)
        self.sb_RH_set.grid(row = 2, column = 1, padx = 2, pady = 2, sticky='w')
        self.pH2O_textvariable = StringVar()

        self.label_converted_pH2O = Label(self.pH2OgrpSetpoint, textvariable=self.pH2O_textvariable)
        self.label_converted_pH2O.grid(row = 2, column = 2)

        self.label_pH2O_set = Label(self.pH2OgrpSetpoint, text = 'pH2O (ppt):')
        self.label_pH2O_set.grid(row = 3, column = 0, padx = 2, pady = 2, sticky='e')

        self.sb_pH2O_set = Spinbox(self.pH2OgrpSetpoint, from_ = 1, to_ = 100, width = 5)
        self.sb_pH2O_set.grid(row = 3, column = 1, padx = 2, pady = 2, sticky='w')

        self.RH_textvariable = StringVar()

        self.label_converted_RH = Label(self.pH2OgrpSetpoint, textvariable=self.RH_textvariable)
        self.label_converted_RH.grid(row = 3, column = 2)

        self.label_pH2O_set.configure(state='disabled')

        self.label_converted_pH2O.configure(state='disabled')

        self.sb_pH2O_set.configure(state='disabled')

        self.box_values_pH2O = Button(self.pH2OgrpSetpoint, text="Apply", command=self.send_pH2O_command)
        self.box_values_pH2O.grid(row = 4, column = 2, columnspan=1, padx = 2, pady = 2, sticky='w')


    def pH2O_vs_RH(self):

        if int(self.v_pH2O_toggle.get()):

            self.label_pH2O_set.configure(state='normal')

            self.sb_pH2O_set.configure(state='normal')

            self.label_RH_set.configure(state='disabled')

            self.sb_RH_set.configure(state='disabled')

        else:

            self.label_RH_set.configure(state='normal')

            self.sb_RH_set.configure(state='normal')

            self.label_pH2O_set.configure(state='disabled')

            self.sb_pH2O_set.configure(state='disabled')


    def send_SC_command(self): 

        reply_SC_power = self.cons.send_command_to_PC('s SC_power '+str(int(self.v_SC_power.get())))

        time.sleep(2)

        if int(self.v_SC_power.get()) == 1 and reply_SC_power == 'Done\n':

            reply_SC_set = self.cons.send_command_to_PC('s SC_set '+  self.sb_SC_set.get())

            print('reply_SC_set', reply_SC_set)

    def send_CC_command(self):

        reply_CC_power = self.cons.send_command_to_PC('s CC_power '+str(int(self.v_CC_power.get())))

        time.sleep(2)

        if int(self.v_CC_power.get()) == 1 and reply_CC_power == 'Done\n':

            reply_CC_set = self.cons.send_command_to_PC('s CC_set '+  self.sb_CC_set.get())

            print('reply_CC_set', reply_CC_set)

    def send_pH2O_command(self):

        reply_DPG_Power = self.cons.send_command_to_PC('s DPG_power '+str(int(self.v_DPG_power.get())))

        print(self.label_RH_set.cget('state'))

        print(self.label_pH2O_set.cget('state'))

        TSC = self.g_sys_instance.Temperatures_SC[-1]

        if self.label_RH_set.cget('state') == 'normal' and self.label_pH2O_set.cget('state') == 'disabled': #RH input

            RH_input = float(self.sb_RH_set.get())

            print("RH_input", RH_input)

            if RH_input >=10 and RH_input <=90: #RH limits

                target_pressure = (RH_input/100.0)*self.ph2oSat(TSC)

                Cell_pressure_output = self.cons.send_command_to_PC('g CellP')

                time.sleep(0.5)

                print(Cell_pressure_output)

                Cell_pressure_string_list = Cell_pressure_output.split('\n')  #Convert to Pa

                Cell_pressure_string = Cell_pressure_string_list[0].split('---')[0]

                Cell_pressure = float(Cell_pressure_string)*1000

                self.pH2O_textvariable.set('pH2O (ppt): ' + str(round((target_pressure/Cell_pressure)*1000,2)))

                self.RH_textvariable.set('')

                target_TDP = opt.brentq(lambda T: self.ph2oSat_solve(T, target_pressure), -50, 50)

                if int(self.v_DPG_power.get()) == 1 and reply_DPG_Power == str('Done\n'):

                    reply_DPG_set = self.cons.send_command_to_PC('s DPG_set '+  str(target_TDP))
                    

                    print('reply_DPG_set', reply_DPG_set)

            elif RH_input >=90:

                messagebox.showwarning(title='RH offlimits', message="Condensation Warning")

                self.RH_textvariable.set('')

                self.pH2O_textvariable.set('')

            else:

                messagebox.showwarning(title='RH offlimits', message="Low RH Warning")

                self.RH_textvariable.set('')

                self.pH2O_textvariable.set('')


        elif self.label_pH2O_set.cget('state') == 'normal' and self.label_RH_set.cget('state') == 'disabled': # pH2O input

            Cell_pressure_output = self.cons.send_command_to_PC('g CellP')

            print(Cell_pressure_output)
            
            time.sleep(0.5)

            Cell_pressure_string_list = Cell_pressure_output.split('\n')  #Convert to Pa

            Cell_pressure_string = Cell_pressure_string_list[0].split('---')[0]

            Cell_pressure = float(Cell_pressure_string)*1000

            target_pressure = (float(self.sb_pH2O_set.get())/1000.0)*Cell_pressure

            RH_input = (target_pressure/self.ph2oSat(TSC))*100

            if RH_input >=10 and RH_input <=90: #RH limits

                self.RH_textvariable.set('RH (%): ' + str(round((target_pressure/self.ph2oSat(TSC)*100),2)))

                self.pH2O_textvariable.set('')

                target_TDP = opt.brentq(lambda T: self.ph2oSat_solve(T, target_pressure), -50, 50)

                if int(self.v_DPG_power.get()) == 1 and reply_DPG_Power == str('Done\n'):

                    reply_DPG_set = self.cons.send_command_to_PC('s DPG_set '+  str(target_TDP))

                    print('reply_DPG_set', reply_DPG_set)

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
