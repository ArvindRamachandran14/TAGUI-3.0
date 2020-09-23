
from tkinter import Frame, LabelFrame, Label, Spinbox, Button, Text, StringVar, Radiobutton, messagebox, Entry
import Data_coord
from math import exp
from sympy.solvers import solve
from sympy import Symbol
import scipy.optimize as opt
import time

class CtrlSetup(Frame):

    def __init__(self, parent, cons, g_sys_instance, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.cons = cons
        self.parent = parent
        self.g_sys_instance = g_sys_instance
        self.Table_Frame = Frame(self)
        self.Table_Frame.grid(row=0, column=0, columnspan=4, sticky='N')
        self.buildContent()
    

    def buildContent(self):

        var_names = ["Parameter", "Power", "Temperature (C)", "ByPass", "pH2O (ppt)", "RH (%)", ""]

        colors = ["light gray", "light gray", "gray", "gray", "gray", "gray", "light gray" ]

        var_names_dummy = [""]*len(var_names)

        for i in range(len(var_names)):

            label = Label(self.Table_Frame,text=var_names[i],bg='slate gray',fg="black", width=15)#, padx=1, pady=1)

            label.grid(row=i,column=0,padx=1,pady=1,sticky='N')

            label = Label(self.Table_Frame,text=var_names_dummy[i],bg=colors[i],fg="black", width=15)#, padx=1, pady=1)

            label.grid(row=i,column=1, columnspan=2, padx=1,pady=1, sticky='N')

            label = Label(self.Table_Frame,text=var_names_dummy[i],bg=colors[i],fg="black", width=15)#, padx=1, pady=1)

            label.grid(row=i,column=3, columnspan=2, padx=1,pady=1, sticky='N')

            label = Label(self.Table_Frame,text=var_names_dummy[i],bg=colors[i],fg="black", width=15)#, padx=1, pady=1)

            label.grid(row=i,column=5, columnspan=2, padx=1,pady=1, sticky='N')

        label_SC =  Label(self.Table_Frame,text="SC", bg="slate gray",fg="black", width=15, padx=1, pady=1)

        label_SC.grid(row=0,column=1, columnspan=2, sticky="w", padx=1, pady=1)

        label_CC =  Label(self.Table_Frame,text="CC", bg="slate gray",fg="black", width=15 ,padx=1, pady=1)

        label_CC.grid(row=0,column=3, columnspan=2, sticky="w", padx=1, pady=1)

        label_DPG =  Label(self.Table_Frame,text="pH2O", bg="slate gray",fg="black", width=15, padx=1, pady=1)

        label_DPG.grid(row=0,column=5, columnspan=2, sticky="w", padx=1, pady=1)

        Label(self.Table_Frame, text="  ", bg="slate gray", fg="black", width=15, padx=1, pady=1).grid(row=3, column=1, columnspan=2, padx = 1, pady = 1, sticky='N')

        MODES = [("ON", "1"),("OFF", "0")]

        self.SC_power = StringVar()
        self.SC_power.set("0") # initialize

        sticky_list = ['e','w']

        for i in range(2):
            self.SC_rb1 = Radiobutton(self.Table_Frame, text=MODES[i][0], variable=self.SC_power, value=MODES[i][1])
            self.SC_rb1.grid(row=1, column=i+1, padx = 2, pady = 2, sticky=sticky_list[i])

        self.CC_power = StringVar()
        self.CC_power.set("0") # initialize

        for i in range(2):
            self.CC_rb1 = Radiobutton(self.Table_Frame, text=MODES[i][0], variable=self.CC_power, value=MODES[i][1])
            self.CC_rb1.grid(row=1, column=i+3, padx = 2, pady = 2, sticky=sticky_list[i])

        self.DPG_power = StringVar()
        self.DPG_power.set("0") # initialize

        for i in range(2):
            self.DPG_rb1 = Radiobutton(self.Table_Frame, text=MODES[i][0], variable=self.DPG_power, value=MODES[i][1])
            self.DPG_rb1.grid(row=1, column=i+5, padx = 2, pady = 2, sticky=sticky_list[i])

        self.SC_set = Entry(self.Table_Frame, bg="light gray", fg="black", width=15)
        self.SC_set.grid(row=2, column=1, columnspan=2, sticky="ew", padx=1, pady=1)


        self.CC_set = Entry(self.Table_Frame, bg="light gray", fg="black", width=15)
        self.CC_set.grid(row=2, column=3, columnspan=2, sticky="ew", padx=1, pady=1)

        self.pH2O_set = Entry(self.Table_Frame, bg="light gray", fg="black", width=15)
        self.pH2O_set.grid(row=4, column=5, columnspan=2, sticky="ew", padx=1, pady=1)

        self.RH_set = Entry(self.Table_Frame, bg="light gray", fg="black", width=15)
        self.RH_set.grid(row=5 ,column=5, columnspan=2, sticky="ew", padx=1, pady=1)

        self.SC_bypass = StringVar()
        self.SC_bypass.set("0") # initialize

        for i in range(2):
            self.SC_rb2 = Radiobutton(self.Table_Frame, text=MODES[i][0], variable=self.SC_bypass, value=MODES[i][1])
            self.SC_rb2.grid(row=3, column=i+1, padx = 2, pady = 2, sticky=sticky_list[i])

        self.SC_apply = Button(self.Table_Frame, text="Apply")

        self.SC_apply.grid(row=6, column=2, sticky='w')

        self.CC_apply = Button(self.Table_Frame, text="Apply")

        self.CC_apply.grid(row=6, column=4, sticky='w')

        self.DPG_apply = Button(self.Table_Frame, text="Apply")

        self.DPG_apply.grid(row=6, column=6, sticky='w')

