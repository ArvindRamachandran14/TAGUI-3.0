
from tkinter import Frame, LabelFrame, Label, Spinbox, Button, Text, StringVar, Radiobutton, messagebox, Entry, Scale, HORIZONTAL, PhotoImage, DoubleVar
import Data_coord
from math import exp
from sympy.solvers import solve
from sympy import Symbol
import scipy.optimize as opt
import time
from tkinter import ttk
from datetime import datetime

class CtrlSetup(Frame):

    def __init__(self, parent, cons, g_sys_instance, g_cal_instance, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.cons = cons
        self.parent = parent
        self.g_sys_instance = g_sys_instance
        self.g_cal_instance = g_cal_instance
        self.Table_Frame = Frame(self)
        self.Table_Frame.grid(row=0, column=0, rowspan=9, columnspan=4, sticky='N')
        self.MODES = ['OFF', 'ON']
    
        self.SC_set = StringVar()

        self.CC_set = StringVar()

        self.pH2O_set = StringVar()

        self.RH_set = StringVar()

        self.buildContent()

    def buildContent(self):

        var_names = ["Parameter", "Power", "Temperature (C)", "ByPass", "pH2O (ppt)", "RH (%)", "Control", "IRGA pump"]

        row_span = [1, 1, 1, 1, 1, 1, 1, 1]

        column_span = [1, 1, 1, 1, 1, 1, 1, 1]

        #colors =  ["white"]*len(var_names)

        colors = ["white", "white", "gray25", "gray25", "gray25", "gray25", "white", "gray25" ]

        var_names_dummy = [""]*len(var_names)

        row_count = 0

        column_count = 0

        for i in range(len(var_names)):

            label = Label(self.Table_Frame, text=var_names[i], bg='light gray',fg="black", relief="solid", width=15)#, height=2) #, padx=1, pady=1)

            label.grid(row=row_count, column=0, rowspan=row_span[i], columnspan=column_span[0], padx=1,pady=1,sticky='EW')
 
            if i==0:

                j_list = []

            elif i==2:

                j_list = [3]

                #j_list = [7]

            elif i==3 or i==7:

                j_list = [2,3]

                #j_list = [4, 7]

            elif i==4 or i==5:

                j_list = [1,2]

                #j_list = [1, 4]

            else:

                j_list = [1,2,3]

                #j_list = [1, 4, 7]
            
            for j in j_list:

                label = Label(self.Table_Frame, text=var_names_dummy[i], bg=colors[i], fg="black", relief="solid", width=12)#, padx=1, pady=1)

                label.grid(row=row_count, column=j, rowspan=row_span[i], columnspan=column_span[i], padx=1, pady=1, sticky='NSEW')
                
                #label.config(highlightbackground="black") 
            
            row_count+=row_span[i]

            column_count+=column_span[i]

        self.SC_power_frame = Frame(self.Table_Frame)
        self.SC_power_frame.grid(row=1, column=1)
        self.SC_power = StringVar()
        self.SC_power.set("0") # initialize
        self.SC_power_scale = Scale(self.SC_power_frame, from_=0, to=1, showvalue=0, length=50, orient=HORIZONTAL, command=self.SC_power_switch)#, command=set_plot_range(1))
        self.SC_power_scale.grid(row=0, column=0)
        self.SC_power_scale.config(highlightthickness=1, width=14)
        self.SC_power_label = Label(self.SC_power_frame, textvariable=self.SC_power, height=1, font=("TkDefaultFont", 11))
        self.SC_power.set(self.MODES[0])
        self.SC_power_label.grid(row=0, column=1)

        self.CC_power_frame = Frame(self.Table_Frame)
        self.CC_power_frame.grid(row=1, column=2)
        self.CC_power = StringVar()
        self.CC_power.set("0") # initialize
        self.CC_power_scale = Scale(self.CC_power_frame, from_=0, to=1, showvalue=0, length=50, orient=HORIZONTAL, command=self.CC_power_switch)#, command=set_plot_range(1))
        self.CC_power_scale.grid(row=0, column=0)
        self.CC_power_scale.config(highlightthickness=1,  width=14)
        self.CC_power_label = Label(self.CC_power_frame, textvariable=self.CC_power, height=1, font=("TkDefaultFont", 11))
        self.CC_power.set(self.MODES[0])
        self.CC_power_label.grid(row=0, column=1)

        self.DPG_power_frame = Frame(self.Table_Frame)
        self.DPG_power_frame.grid(row=1, column=3)

        self.DPG_power = StringVar()
        self.DPG_power.set("0") # initialize
        self.DPG_power_scale = Scale(self.DPG_power_frame, from_=0, to=1, showvalue=0, length=50, orient=HORIZONTAL, command=self.DPG_power_switch)#, command=set_plot_range(1))
        self.DPG_power_scale.grid(row=0, column=0)
        self.DPG_power_scale.config(highlightthickness=1,  width=14)
        self.DPG_power_label = Label(self.DPG_power_frame, textvariable=self.DPG_power, height=1, font=("TkDefaultFont", 11))
        self.DPG_power.set(self.MODES[0])
        self.DPG_power_label.grid(row=0, column=1)

        self.SC_bypass_outerframe = Label(self.Table_Frame, text="", bg="white", fg="black", relief="solid", width=12)
        self.SC_bypass_outerframe.grid(row=3, column=1, rowspan=1, columnspan=1, padx=1, pady=1, sticky='NSEW')

        self.SC_bypass_frame = Frame(self.Table_Frame)
        self.SC_bypass_frame.grid(row=3, column=1)
        
        self.SC_bypass = StringVar()
        self.SC_bypass.set("0") # initialize
        self.SC_bypass_scale = Scale(self.SC_bypass_frame, from_=0, to=1, showvalue=0, length=50, orient=HORIZONTAL, command=self.SC_bypass_switch)#, command=set_plot_range(1))
        self.SC_bypass_scale.grid(row=0, column=0, sticky='e')
        self.SC_bypass_label = Label(self.SC_bypass_frame, textvariable=self.SC_bypass, height=1, font=("TkDefaultFont", 11))
        self.SC_bypass.set(self.MODES[0])
        self.SC_bypass_label.grid(row=0, column=1, sticky='w')

        self.IRGA_pump_outerframe = Label(self.Table_Frame, text="", bg="white", fg="black", relief="solid", width=12)
        self.IRGA_pump_outerframe.grid(row=7, column=1, rowspan=1, columnspan=1, padx=1, pady=1, sticky='NSEW')
        self.IRGA_pump_frame = Frame(self.Table_Frame)
        self.IRGA_pump_frame.grid(row=7, column=1)
        self.IRGA_pump = StringVar()
        self.IRGA_pump.set("0") # initialize
        self.IRGA_pump_scale = Scale(self.IRGA_pump_frame, from_=0, to=1, showvalue=0, length=50, orient=HORIZONTAL, command=self.IRGA_pump_switch)#, command=set_plot_range(1))
        self.IRGA_pump_scale.grid(row=0, column=0, sticky='e')
        self.IRGA_pump_label = Label(self.IRGA_pump_frame, textvariable=self.IRGA_pump, height=1, font=("TkDefaultFont", 11))
        self.IRGA_pump.set(self.MODES[0])
        self.IRGA_pump_label.grid(row=0, column=1, sticky='w')



        label_parname = Label(self.Table_Frame,text="Parameter", bg="light gray",fg="black", width=15, relief="solid", padx=1, pady=1)

        label_parname.grid(row=0,column=0, sticky="n", padx=1, pady=1)

        label_SC =  Label(self.Table_Frame,text="SC", bg="light gray",fg="black", width=12, relief="solid", padx=1, pady=1)

        label_SC.grid(row=0,column=1, columnspan=1, sticky="ew", padx=1, pady=1)

        label_SC.config(highlightbackground="black")

        label_CC =  Label(self.Table_Frame,text="CC", bg="light gray",fg="black", width=12 , relief="solid", padx=1, pady=1)

        label_CC.grid(row=0,column=2, columnspan=1, sticky="ew", padx=1, pady=1)

        label_CC.config(highlightbackground="black")

        label_DPG =  Label(self.Table_Frame,text="pH2O", bg="light gray",fg="black", width=12, relief="solid", padx=1, pady=1)

        label_DPG.grid(row=0,column=3, columnspan=1, sticky="ew", padx=1, pady=1)
        
        '''
      
        #Label(self.Table_Frame, text="  ", bg="white", fg="black", width=15, relief="solid", padx=1, pady=1).grid(row=3, column=1, columnspan=2, padx=1, pady=1, sticky='N')

        MODES = [("ON", "1"),("OFF", "0")]

        self.SC_power = StringVar()
        self.SC_power.set("0") # initialize

        sticky_list = ['e','w']

        for i in range(2):
            self.SC_rb1 = Radiobutton(self.Table_Frame, text=MODES[i][0], variable=self.SC_power, value=MODES[i][1], height=1)
            self.SC_rb1.grid(row=1, column=i+1, padx=1, pady=1, sticky=sticky_list[i])

        self.CC_power = StringVar()
        self.CC_power.set("0") # initialize

        for i in range(2):
            self.CC_rb1 = Radiobutton(self.Table_Frame, text=MODES[i][0], variable=self.CC_power, value=MODES[i][1], height=1)
            self.CC_rb1.grid(row=1, column=i+3, padx=1, pady=1, sticky=sticky_list[i])

        self.DPG_power = StringVar()
        self.DPG_power.set("0") # initialize

        for i in range(2):
            self.DPG_rb1 = Radiobutton(self.Table_Frame, text=MODES[i][0], variable=self.DPG_power, value=MODES[i][1], height=1)
            self.DPG_rb1.grid(row=1, column=i+5, padx=1, pady=1, sticky=sticky_list[i])
        '''
        self.SC_set_entry = Entry(self.Table_Frame, bg="gray", fg="white", width=13, textvariable=self.SC_set)
        self.SC_set_entry.grid(row=2, column=1, columnspan=1, sticky="ew", padx=1, pady=1)
        self.SC_set_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.CC_set_entry = Entry(self.Table_Frame, bg="gray", fg="white", width=13, textvariable=self.CC_set)
        self.CC_set_entry.grid(row=2, column=2, columnspan=1, sticky="ew", padx=1, pady=1)
        self.CC_set_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.pH2O_set_entry = Entry(self.Table_Frame, bg="gray", fg="white", width=13, textvariable=self.pH2O_set)
        self.pH2O_set_entry.grid(row=4, column=3, columnspan=1, sticky="ew", padx=1, pady=1)
        self.pH2O_set_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.RH_set_entry = Entry(self.Table_Frame, bg="gray", fg="white", width=13, textvariable=self.RH_set)
        self.RH_set_entry.grid(row=5,column=3, columnspan=1, sticky="ew", padx=1, pady=1)
        self.RH_set_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.SC_apply_var = StringVar()

        self.SC_apply = Button(self.Table_Frame, textvariable=self.SC_apply_var, bg="white", fg="black", command=self.SC_apply_func)

        self.SC_apply.grid(row=6, column=1, padx=1, pady=1)

        self.SC_apply.config(width=8, bd=0, height=1, relief='flat')

        self.SC_apply_var.set("Apply")

        self.CC_apply_var = StringVar()

        self.CC_apply = Button(self.Table_Frame, textvariable=self.CC_apply_var, bg="white", fg="black", command=lambda:[self.CC_apply_func()])

        self.CC_apply.grid(row=6, column=2, padx=1, pady=1)

        self.CC_apply.config(width=8, bd=0, height=1, relief='flat')

        self.CC_apply_var.set("Apply")

        self.DPG_apply_var = StringVar()

        self.DPG_apply = Button(self.Table_Frame, textvariable=self.DPG_apply_var, bg="white", fg="black", command=self.send_pH2O_command)

        self.DPG_apply.config(width=8, bd=0, height=1, relief='flat')
        
        self.DPG_apply.grid(row=6, column=3, padx=1, pady=1)

        self.DPG_apply_var.set("Apply")

    def update_setup_table(self):

        ################## Update power ################## 

        self.SC_power.set(self.MODES[int(float(self.g_cal_instance.SC_power))])

        self.SC_power_scale.set(int(float(self.g_cal_instance.SC_power)))

        self.CC_power.set(self.MODES[int(float(self.g_cal_instance.CC_power))])

        self.CC_power_scale.set(int(float(self.g_cal_instance.CC_power)))

        self.DPG_power.set(self.MODES[int(float(self.g_cal_instance.DPG_power))])

        self.DPG_power_scale.set(int(float(self.g_cal_instance.DPG_power)))

        ################## Update Set Points ################## 

        self.SC_set.set(str(self.g_cal_instance.SC_set))

        self.CC_set.set(str(self.g_cal_instance.CC_set))


    def SC_power_switch(self, value):

        reply = self.cons.send_command_to_PC('s SC_power '+str(self.SC_power_scale.get()))

        if reply == 'e 0\n':

            self.SC_power.set(self.MODES[self.SC_power_scale.get()])

    def CC_power_switch(self, value):

        reply = self.cons.send_command_to_PC('s CC_power '+str(self.CC_power_scale.get()))

        if reply == 'e 0\n':    

            self.CC_power.set(self.MODES[self.CC_power_scale.get()])

    def DPG_power_switch(self, value):

        reply = self.cons.send_command_to_PC('s DPG_power '+str(self.DPG_power_scale.get()))

        if reply == 'e 0\n':    

            self.DPG_power.set(self.MODES[self.DPG_power_scale.get()])

    def SC_bypass_switch(self, value):

        reply = self.cons.send_command_to_PC('s ByPass '+str(self.SC_bypass_scale.get()))

        if reply == 'e 0\n':

            self.SC_bypass.set(self.MODES[self.SC_bypass_scale.get()])

    def IRGA_pump_switch(self, value):

        reply = self.cons.send_command_to_PC('s IRGA_pump '+str(self.IRGA_pump_scale.get()))

        if reply == 'e 0\n':

            self.IRGA_pump.set(self.MODES[self.IRGA_pump_scale.get()])

    def SC_apply_func(self):

        if self.MODES.index(self.SC_power.get()):

            self.SC_set_entry.config(bg='gray', fg = "white")

            self.update()

            reply = self.cons.send_command_to_PC('s SC_set '+str(self.SC_set.get()))

            if reply == 'e 0\n':

                self.SC_set_entry.config(bg='light gray', fg='black')

                self.update()

            else:

                messagebox.showwarning(title='Command Error', message="Check entry")
        
        else:

            messagebox.showwarning(title='Power Error', message="Switch controller on")


    def CC_apply_func(self):

        if self.MODES.index(self.CC_power.get()):

            #self.validate(self.CC_set.get(), input_type, input_range, var_name)

            self.CC_set_entry.config(bg='gray', fg = "white")

            self.update()

            reply = self.cons.send_command_to_PC('s CC_set '+str(self.CC_set.get()))

            if reply == 'e 0\n':

                self.CC_set_entry.config(bg='light gray', fg='black')

                self.update()

            else:

                messagebox.showwarning(title='Command Error', message="Check entry")
        else:

            messagebox.showwarning(title='Power Error', message="Switch controller on")
        
    def send_pH2O_command(self):

        if self.MODES.index(self.DPG_power.get()):

            self.RH_set_entry.config(bg='gray', fg = "white")

            self.pH2O_set_entry.config(bg='gray', fg = "white")

            self.update()

            TSC = self.g_sys_instance.Temperatures_SC[-1]

            if len(self.RH_set.get()) == 0 and len(self.pH2O_set.get()) == 0:

                messagebox.showwarning(title='Input Error', message="No entry for RH or pH2O")

            elif len(self.RH_set.get()) > 0 and len(self.pH2O_set.get()) == 0: #RH entry

                RH_input = float(self.RH_set.get())

                if RH_input >=10 and RH_input <=90: #RH limits

                    target_pressure = (RH_input/100.0)*self.ph2oSat(TSC)

                    Cell_pressure_output = self.cons.send_command_to_PC('g CellP')

                    print('Cell_pressure_output', Cell_pressure_output)

                    Cell_pressure_string_list = Cell_pressure_output.split('\n')  #Convert to Pa

                    Cell_pressure_string = Cell_pressure_string_list[0].split('---')[0]

                    Cell_pressure = float(Cell_pressure_string)*1000

                    #self.pH2O_set.set((target_pressure/Cell_pressure)*1000,2)

                    self.pH2O_set.insert(0, str(round((target_pressure/Cell_pressure)*1000,2)))

                    target_TDP = opt.brentq(lambda T: self.ph2oSat_solve(T, target_pressure), -50, 50)

                    reply_DPG_set = self.cons.send_command_to_PC('s DPG_set '+  str(target_TDP))

                    if reply_DPG_set == 'e 0\n':

                        print('Command success')

                        self.pH2O_set.config(bg='light gray', fg='black')

                        self.RH_set.config(bg='light gray', fg='black')

                        self.update()

                    reply_DPG_set = self.cons.send_command_to_PC('s DPG_set '+  str(target_TDP))
                        
                    #print('reply_DPG_set', reply_DPG_set)

                elif RH_input >=90:

                    messagebox.showwarning(title='RH offlimits', message="Condensation Warning")

                else:

                    messagebox.showwarning(title='RH offlimits', message="Low RH Warning")

            elif len(self.RH_set.get()) == 0 and len(self.pH2O_set.get()) > 0: # pH2O entry

                Cell_pressure_output = self.cons.send_command_to_PC('g CellP')

                #print(Cell_pressure_output)

                Cell_pressure_string_list = Cell_pressure_output.split('\n')  #Convert to Pa

                Cell_pressure_string = Cell_pressure_string_list[0].split('---')[0]

                Cell_pressure = float(Cell_pressure_string)*1000

                target_pressure = (float(self.pH2O_set.get())/1000.0)*Cell_pressure

                RH_input = (target_pressure/self.ph2oSat(TSC))*100

                if RH_input >=10 and RH_input <=90: #RH limits

                    target_TDP = opt.brentq(lambda T: self.ph2oSat_solve(T, target_pressure), -50, 50)

                    self.RH_set.insert(0, str(round(RH_input,2)))

                    #print(target_TDP)
                
                    reply_DPG_set = self.cons.send_command_to_PC('s DPG_set '+  str(target_TDP))

                    if reply_DPG_set == 'e 0\n':

                        print('Command success')

                        self.pH2O_set.config(bg='light gray', fg='black')

                        self.RH_set.config(bg='light gray', fg='black')

                        self.update()


                elif RH_input >=90:

                    messagebox.showwarning(title='pH2O offlimits', message="Condensation Warning")

                else:

                    messagebox.showwarning(title='pH2O offlimits', message="Low pH2O warning")

            else:

                messagebox.showwarning(title='Input Error', message="Choose one entry for RH or pH2O")

        else:

            messagebox.showwarning(title='Power Error', message="Switch controller on")


    def ph2oSat_solve(self, T, P):
        return 610.78 * exp((T * 17.2684) / (T + 238.3)) - P

    def ph2oSat(self, T):
        return 610.78 * exp((T * 17.2684) / (T + 238.3))

    '''

    def validate(self):

        if 

            return string1

        elif

            return string2


        elif

            return string3

        else

            return string4
    '''


