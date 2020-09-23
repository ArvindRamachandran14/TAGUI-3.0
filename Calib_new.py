from tkinter import Frame, LabelFrame, Label, Spinbox, Button, Text, StringVar, Radiobutton, OptionMenu, Entry, Scale, HORIZONTAL, Checkbutton, IntVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from datetime import datetime
import time

class Calib(Frame) :

    def __init__(self, parent, g_sys_instance, g_cal_instance, cons, *args, **kwargs) :
        Frame.__init__(self, *args, **kwargs)

        self.Table_Frame = Frame(self)

        self.Table_Frame.grid(row=0, column=0, columnspan=4, sticky='N')

        self.Graph_Frame = Frame(self)

        self.Graph_Frame.grid(row=0, column=4, columnspan=3, sticky='N')

        self.g_sys_instance = g_sys_instance
        self.g_cal_instance = g_cal_instance
        self.cons = cons
        self.plot_density = 7
        self.slider_list = [0,1,2,3,4]
        self.slider_list_value = [0.5,1,15,30,60]
        #self.parent = parent

        self.build_calib_table()

        self.buildFigure()

        #self.build_SC_table()
        #self.build_CC_table()
        #self.build_DPG_table()
       

    def buildFigure(self) :

        self.check_var1 = IntVar()
        Checkbutton(self.Graph_Frame, text="TSC", variable=self.check_var1).grid(row=0, column=0, sticky='N')
        self.check_var2 = IntVar()
        Checkbutton(self.Graph_Frame, text="TCC", variable=self.check_var2).grid(row=0, column=1, sticky='N')
        self.check_var3 = IntVar()
        Checkbutton(self.Graph_Frame, text="TDPG", variable=self.check_var3).grid(row=0, column=2, sticky='N')

        self.output = StringVar()

        self.scale_textvariable = StringVar()

        self.fig1 = Figure(figsize=(5.7, 3.8))
        self.ax1 = self.fig1.add_subplot(111)
        self.ax1.set_xlabel('Time (sec)')
        self.ax1.set_ylabel('Temperature ($^\circ$C)')
        self.ax1.set_autoscalex_on(True)
        self.ax1.set_ybound(10, 40)
        self.ax1.set_autoscaley_on(True)
        self.ax1.grid(True, 'major', 'both')

        self.ax1_twin = self.ax1.twinx()

        self.ax1_twin.set_ylabel('Controller power output')

        self.ax1_twin.set_autoscalex_on(True)

        #self.ax1.tick_params('y', colors='b')
        #self.ax1_twin.tick_params('y', colors='r')

        self.fig1.tight_layout()
      
        self.cnvs1 = FigureCanvasTkAgg(self.fig1, self.Graph_Frame)
        
        self.cnvs1.get_tk_widget().grid(row=1, column=0, columnspan=3, sticky='NSEW')

        self.scale = Scale(self.Graph_Frame, from_=min(self.slider_list), to=max(self.slider_list), command=self.scale_value_show, showvalue=0, orient=HORIZONTAL)#, command=set_plot_range(1))
        self.scale.grid(row=2, column=1, rowspan=1)

        self.scale_textvariable.set('Plot range(m): '+ str(self.slider_list_value[0]))

        self.scale1_label = Label(self.Graph_Frame, textvariable=self.scale_textvariable)

        self.scale1_label.grid(row=3, column=1, rowspan=1)


    def build_calib_table(self):

        self.calib_check_var = IntVar()
        Checkbutton(self.Table_Frame, text="Calibration mode", variable=self.calib_check_var, command=self.set_bcalibration).grid(row=0, column=1, columnspan=2, sticky='EW')

        var_names = ["Var name", "Measured T", "Output", "Power", "", "P", "I", "D", "", "Set Point", ""]

        colors = ["gray", "slate gray", "slate gray", "light gray", "light gray", "gray", "gray", "gray",  "gray", "light gray", "light gray"]

        var_names_dummy = [""]*len(var_names)

        for i in range(len(var_names)):

            label = Label(self.Table_Frame,text=var_names[i],bg=colors[i],fg="white", width=15)#, padx=1, pady=1)

            label.grid(row=i+1,column=0,padx=1,pady=1,sticky='N')

            label = Label(self.Table_Frame,text=var_names_dummy[i],bg=colors[i],fg="white", width=15)#, padx=1, pady=1)

            label.grid(row=i+1,column=1, columnspan=2, padx=1,pady=1, sticky='N')

            label = Label(self.Table_Frame,text=var_names_dummy[i],bg=colors[i],fg="white", width=15)#, padx=1, pady=1)

            label.grid(row=i+1,column=3, columnspan=2, padx=1,pady=1, sticky='N')

            label = Label(self.Table_Frame,text=var_names_dummy[i],bg=colors[i],fg="white", width=15)#, padx=1, pady=1)

            label.grid(row=i+1,column=5, columnspan=2, padx=1,pady=1, sticky='N')

        label_SC =  Label(self.Table_Frame,text="SC", bg="gray",fg="white", width=15, padx=1, pady=1)

        label_SC.grid(row=1,column=1, columnspan=2, sticky="w", padx=1, pady=1)

        label_CC =  Label(self.Table_Frame,text="CC", bg="gray",fg="white", width=15 ,padx=1, pady=1)

        label_CC.grid(row=1,column=3, columnspan=2, sticky="w", padx=1, pady=1)

        label_DPG =  Label(self.Table_Frame,text="DPG", bg="gray",fg="white", width=15, padx=1, pady=1)

        label_DPG.grid(row=1,column=5, columnspan=2, sticky="w", padx=1, pady=1)

        self.TSC = self.TCC = self.TDPG = StringVar()
 
        self.TSC_entry = Entry(self.Table_Frame, bg="slate gray", fg="white", width=15, textvariable=self.TSC)

        self.TSC_entry.grid(row=2,column=1, columnspan=2, sticky="w", padx=1, pady=1)

        self.TCC_entry = Entry(self.Table_Frame, bg="slate gray", fg="white", width=15, textvariable=self.TCC)

        self.TCC_entry.grid(row=2,column=3, columnspan=2, sticky="w", padx=1, pady=1)

        self.TDPG_entry = Entry(self.Table_Frame, bg="slate gray", fg="white", width=15, textvariable=self.TDPG)

        self.TDPG_entry.grid(row=2,column=5, columnspan=2, sticky="ew", padx=1, pady=1)

        self.SC_output = Entry(self.Table_Frame, bg="slate gray", fg="white", width=15)

        self.SC_output.grid(row=3,column=1, columnspan=2, sticky="ew", padx=1, pady=1)

        self.CC_output = Entry(self.Table_Frame, bg="slate gray", fg="white", width=15)

        self.CC_output.grid(row=3,column=3, columnspan=2, sticky="ew")

        self.DPG_output = Entry(self.Table_Frame, bg="slate gray", fg="white", width=15)

        self.DPG_output.grid(row=3,column=5, columnspan=2, sticky="ew", padx=1, pady=1)

        self.SC_P = Entry(self.Table_Frame, bg="gray", fg="white", width=15)

        self.SC_P.grid(row=6,column=1, columnspan=2, sticky="ew", padx=1, pady=1)

        self.CC_P = Entry(self.Table_Frame, bg="gray", fg="white", width=15)

        self.CC_P.grid(row=6,column=3, columnspan=2, sticky="ew", padx=1, pady=1)

        self.DPG_P = Entry(self.Table_Frame, bg="gray", fg="white", width=15)

        self.DPG_P.grid(row=6,column=5, columnspan=2, sticky="ew", padx=1, pady=1)

        self.SC_I = Entry(self.Table_Frame, bg="gray", fg="white", width=15)

        self.SC_I.grid(row=7,column=1, columnspan=2, sticky="ew", padx=1, pady=1)

        self.CC_I = Entry(self.Table_Frame, bg="gray", fg="white", width=15)

        self.CC_I.grid(row=7,column=3, columnspan=2, sticky="ew", padx=1, pady=1)

        self.DPG_I = Entry(self.Table_Frame, bg="gray", fg="white", width=15)

        self.DPG_I.grid(row=7,column=5, columnspan=2, sticky="ew", padx=1, pady=1)

        self.SC_D = Entry(self.Table_Frame, bg="gray", fg="white", width=15)

        self.SC_D.grid(row=8,column=1, columnspan=2, sticky="ew", padx=1, pady=1)

        self.CC_D = Entry(self.Table_Frame, bg="gray", fg="white", width=15)

        self.CC_D.grid(row=8,column=3, columnspan=2, sticky="ew", padx=1, pady=1)

        self.DPG_D = Entry(self.Table_Frame, bg="gray", fg="white", width=15)

        self.DPG_D.grid(row=8,column=5, columnspan=2, sticky="ew", padx=1, pady=1)

        self.SC_set = Entry(self.Table_Frame, bg="light gray", fg="white", width=15)

        self.SC_set.grid(row=10,column=1, columnspan=2, sticky="ew", padx=1, pady=1)

        self.CC_set = Entry(self.Table_Frame, bg="light gray", fg="white", width=15)

        self.CC_set.grid(row=10,column=3, columnspan=2, sticky="ew", padx=1, pady=1)

        self.DPG_set = Entry(self.Table_Frame, bg="light gray", fg="white", width=15)

        self.DPG_set.grid(row=10,column=5, columnspan=2, sticky="ew", padx=1, pady=1)

        MODES = [("ON", "1"),("OFF", "0")]

        self.SC_power = StringVar()
        self.SC_power.set("0") # initialize

        sticky_list = ['e','w']

        for i in range(2):
            self.SC_rb1 = Radiobutton(self.Table_Frame, text=MODES[i][0], variable=self.SC_power, value=MODES[i][1])
            self.SC_rb1.grid(row=4, column=i+1, padx = 2, pady = 2, sticky=sticky_list[i])


        self.CC_power = StringVar()
        self.CC_power.set("0") # initialize

        for i in range(2):
            self.CC_rb1 = Radiobutton(self.Table_Frame, text=MODES[i][0], variable=self.CC_power, value=MODES[i][1])
            self.CC_rb1.grid(row=4, column=i+3, padx = 2, pady = 2, sticky=sticky_list[i])


        self.DPG_power = StringVar()
        self.DPG_power.set("0") # initialize

        for i in range(2):
            self.DPG_rb1 = Radiobutton(self.Table_Frame, text=MODES[i][0], variable=self.DPG_power, value=MODES[i][1])
            self.DPG_rb1.grid(row=4, column=i+5, padx = 2, pady = 2, sticky=sticky_list[i])


        self.SC_power_apply = Button(self.Table_Frame, text="Apply")

        self.SC_power_apply.grid(row=5, column=2, sticky='w')

        self.SC_PID_apply = Button(self.Table_Frame, text="Apply")

        self.SC_PID_apply.grid(row=9, column=2, sticky='w')

        self.SC_SetPoint_apply = Button(self.Table_Frame, text="Apply")

        self.SC_SetPoint_apply.grid(row=11, column=2, sticky='w')

        self.CC_power_apply = Button(self.Table_Frame, text="Apply")

        self.CC_power_apply.grid(row=5, column=4, sticky='w')

        self.CC_PID_apply = Button(self.Table_Frame, text="Apply")

        self.CC_PID_apply.grid(row=9, column=4, sticky='w')

        self.CC_SetPoint_apply = Button(self.Table_Frame, text="Apply")

        self.CC_SetPoint_apply.grid(row=11, column=4, sticky='w')

        self.DPG_power_apply = Button(self.Table_Frame, text="Apply")

        self.DPG_power_apply.grid(row=5, column=6, sticky='w')

        self.DPG_PID_apply = Button(self.Table_Frame, text="Apply")

        self.DPG_PID_apply.grid(row=9, column=6, sticky='w')

        self.DPG_SetPoint_apply = Button(self.Table_Frame, text="Apply")

        self.DPG_SetPoint_apply.grid(row=11, column=6, sticky='w')

    def set_bcalibration(self):

        if self.calib_check_var.get():

            self.g_cal_instance.bcalibration = True

        else:

            self.g_cal_instance.bcalibration = False

    def scale_value_show(self, value):
        
        self.scale_textvariable.set('Plot range(m): '+ str(self.slider_list_value[int(value)]))

    def animate_temperatures(self, i):

        self.ax1.clear()
        self.ax1.set_xlabel('Time (sec)')
        self.ax1.set_ylabel('Temperature ($^\circ$C)')
        self.ax1.set_autoscalex_on(True)
        #self.ax1.set_ybound(10, 40)
        self.ax1.set_autoscaley_on(True)
        self.ax1.grid(True, 'major', 'both')

        self.plot_range = self.slider_list_value[self.scale.get()]*60 

        #print('range type', type(range))

        index = int(self.plot_range/15.0)

        outputstring=""

        if self.calib_check_var.get():

            if self.check_var1.get():

                self.ax1.plot(self.g_sys_instance.time_list[(25000-self.plot_density*index):], self.g_sys_instance.Temperatures_SC[(25000-self.plot_density*index):], 'k', label="TSC")
                
                self.ax1.legend()

                self.TSC.set(str(self.g_sys_instance.Temperatures_SC[-1]))

                #self.plot_label_variable.set("  Sample Chamber Temperature")

            if self.check_var2.get():

                self.ax1.plot(self.g_sys_instance.time_list[(25000-self.plot_density*index):], self.g_sys_instance.Temperatures_CC[(25000-self.plot_density*index):], 'b', label="TCC")

                self.ax1.legend()

                self.TCC.set(str(self.g_sys_instance.Temperatures_CC[-1]))

                #self.plot_label_variable.set("  Conditioning Chamber Temperature")

            if self.check_var3.get():
                
                self.ax1.plot(self.g_sys_instance.time_list[(25000-self.plot_density*index):], self.g_sys_instance.Temperatures_DPG[(25000-self.plot_density*index):], 'r', label="TDPG")

                self.ax1.legend()

                self.TDPG.set(str(self.g_sys_instance.Temperatures_DPG[-1]))

                #self.plot_label_variable.set("  Dew Point Generator Temperature")

            outputstring=""

