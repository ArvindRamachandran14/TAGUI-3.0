from tkinter import Frame, LabelFrame, Label, Spinbox, Button, Text, StringVar, Radiobutton, OptionMenu, Entry, Scale, HORIZONTAL, Checkbutton, IntVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from datetime import datetime
import time

class Calib(Frame) :

    def __init__(self, parent, g_sys_instance, g_cal_instance, cons, *args, **kwargs) :
        Frame.__init__(self, *args, **kwargs)

        self.Table_Frame = Frame(self)

        self.Table_Frame.grid(row=0, column=0, sticky='N')

        self.Middle_Frame = Frame(self)

        self.Middle_Frame.grid(row=0, column=1, sticky='N')

        self.Graph_Frame = Frame(self)

        self.Graph_Frame.grid(row=0, column=2, columnspan=3, sticky='N')

        self.g_sys_instance = g_sys_instance
        self.g_cal_instance = g_cal_instance
        self.cons = cons
        self.plot_density = 7
        self.slider_list = [0,1,2,3,4]
        self.slider_list_value = [0.5,1,15,30,60]
        #self.parent = parent

        self.MODES = ['OFF', 'ON']

        self.build_calib_table()

        self.buildFigure()

        #self.build_SC_table()
        #self.build_CC_table()
        #self.build_DPG_table()
       

    def buildFigure(self) :

        for i in range(12):

            Label(self.Middle_Frame, text="",width=6).grid(row=i,column=0)

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

        self.check_button_frame = Frame(self.Table_Frame)
        self.check_button_frame.grid(row=0,column=0,columnspan=4)

        self.calib_check_var = IntVar()
        Checkbutton(self.check_button_frame, text="Calibration mode", variable=self.calib_check_var, command=self.set_bcalibration).grid(row=0, column=0, sticky='EW')

        var_names = ["Var name", "Measured T", "Output", "Power", "P", "I", "D", "", "Set Point", ""]

        colors = ["gray", "light gray", "light gray", "light gray", "gray", "gray", "gray",  "gray", "light gray", "light gray"]

        var_names_dummy = [""]*11

        #################################### Frame 1 ####################################

        self.frame_1 = Frame(self.Table_Frame)
        self.frame_1.grid(row=1,column=0,columnspan=4, sticky='NW')

        for i in range(0,3):

            label = Label(self.frame_1,text=var_names[i],bg="light gray", fg="black", width=15, relief="solid")#, padx=1, pady=1)

            label.grid(row=i,column=0,padx=1,pady=1,sticky='N')

            label.config(highlightbackground="black") 

        label_SC =  Label(self.frame_1,text="SC", bg="light gray",fg="black", width=12, relief="solid")

        label_SC.grid(row=0,column=1, sticky="ew", padx=1, pady=1)

        label_SC.config(highlightbackground="black") 

        label_CC =  Label(self.frame_1,text="CC", bg="light gray",fg="black", width=12, relief="solid")

        label_CC.grid(row=0,column=2, sticky="ew", padx=1, pady=1)

        label_CC.config(highlightbackground="black") 

        label_DPG =  Label(self.frame_1,text="DPG", bg="light gray",fg="black", width=12, relief="solid")

        label_DPG.grid(row=0,column=3, sticky="ew", padx=1, pady=1)

        label_DPG.config(highlightbackground="black") 

        self.TSC = StringVar()

        self.TCC = StringVar()

        self.TDPG = StringVar()
 
        self.TSC_entry = Entry(self.frame_1, bg="light gray", fg="black", width=13, textvariable=self.TSC)

        self.TSC_entry.grid(row=1,column=1, sticky="ew", padx=1, pady=1)

        self.TSC_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.TCC_entry = Entry(self.frame_1, bg="light gray", fg="black", width=13, textvariable=self.TCC)

        self.TCC_entry.grid(row=1,column=2, sticky="ew", padx=1, pady=1)

        self.TCC_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.TDPG_entry = Entry(self.frame_1, bg="light gray", fg="black", width=13, textvariable=self.TDPG)

        self.TDPG_entry.grid(row=1,column=3, sticky="ew", padx=1, pady=1)

        self.TDPG_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.SC_output = Entry(self.frame_1, bg="light gray", fg="black", width=13)

        self.SC_output.grid(row=2,column=1, sticky="ew", padx=1, pady=1)

        self.SC_output.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.CC_output = Entry(self.frame_1, bg="light gray", fg="black", width=13)

        self.CC_output.grid(row=2,column=2, sticky="ew", padx=1, pady=1)

        self.CC_output.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.DPG_output = Entry(self.frame_1, bg="light gray", fg="black", width=13)

        self.DPG_output.grid(row=2,column=3, sticky="ew", padx=1, pady=1)

        self.DPG_output.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        #################################### Frame 2 ####################################

        self.frame_2 = Frame(self.Table_Frame)
        self.frame_2.grid(row=2,column=0,columnspan=4, sticky='NW')

        for i in range(0,4):

            Label(self.frame_2, text="",height=1).grid(row=0, column=i,sticky='N')

        #################################### Frame 3 ####################################

        self.frame_3 = Frame(self.Table_Frame)
        self.frame_3.grid(row=3,column=0,columnspan=4, sticky='NSEW')

        self.power_label = Label(self.frame_3,text="Power",bg="light gray", fg="black", width=15, relief="solid")#, padx=1, pady=1)
        self.power_label.grid(row=0,column=0,padx=1,pady=1,sticky='NSEW')

        self.SC_power_outer_frame =  Label(self.frame_3, text="", bg="white", fg="black", width=13, relief="solid")
        self.SC_power_outer_frame.grid(row=0, column=1, sticky="ew", padx=1, pady=1)

        #self.SC_power_outer_frame = Label(self.frame_3, text="", bg="white", fg="black", relief="solid", width=12)#, padx=1, pady=1)
        #self.SC_power_outer_frame.grid(row=0, column=1, padx=1, pady=1, sticky='NSEW')

        self.SC_power_frame = Frame(self.frame_3)
        self.SC_power_frame.grid(row=0, column=1)

        self.SC_power = StringVar()
        self.SC_power.set("0") # initialize


        self.SC_power_scale = Scale(self.SC_power_frame, from_=0, to=1, showvalue=0, length=50, orient=HORIZONTAL, command=self.SC_power_switch)#, command=set_plot_range(1))
        self.SC_power_scale.grid(row=0, column=0, sticky='NW')
        self.SC_power_scale.config(highlightthickness=1, width=14)
        self.SC_power_label = Label(self.SC_power_frame, textvariable=self.SC_power, height=1, font=("TkDefaultFont", 11))
        self.SC_power.set(self.MODES[0])
        self.SC_power_label.grid(row=0, column=1)

        self.CC_power_outer_frame = Label(self.frame_3, text="", bg="white", fg="black", width=13, relief="solid")#, padx=1, pady=1)
        self.CC_power_outer_frame.grid(row=0, column=2, padx=1, pady=1, sticky='ew')

        self.CC_power_frame = Frame(self.frame_3)
        self.CC_power_frame.grid(row=0, column=2)

        self.CC_power = StringVar()
        self.CC_power.set("0") # initialize
        self.CC_power_scale = Scale(self.CC_power_frame, from_=0, to=1, showvalue=0, length=50, orient=HORIZONTAL, command=self.CC_power_switch)#, command=set_plot_range(1))
        self.CC_power_scale.grid(row=0, column=0)
        self.CC_power_scale.config(highlightthickness=1, width=14)
        self.CC_power_label = Label(self.CC_power_frame, textvariable=self.CC_power, height=1, font=("TkDefaultFont", 11))
        self.CC_power.set(self.MODES[0])
        self.CC_power_label.grid(row=0, column=1)

        self.DPG_power_outer_frame = Label(self.frame_3, text="", bg="white", fg="black", relief="solid", width=13)#, padx=1, pady=1)
        self.DPG_power_outer_frame.grid(row=0, column=3, padx=1, pady=1, sticky='ew')

        self.DPG_power_frame = Frame(self.frame_3)
        self.DPG_power_frame.grid(row=0, column=3)

        self.DPG_power = StringVar()
        self.DPG_power.set("0") # initialize
        self.DPG_power_scale = Scale(self.DPG_power_frame, from_=0, to=1, showvalue=0, length=50, orient=HORIZONTAL, command=self.DPG_power_switch)#, command=set_plot_range(1))
        self.DPG_power_scale.grid(row=0, column=0)
        self.DPG_power_scale.config(highlightthickness=1, width=14)
        self.DPG_power_label = Label(self.DPG_power_frame, textvariable=self.DPG_power, height=1, font=("TkDefaultFont", 11))
        self.DPG_power.set(self.MODES[0])
        self.DPG_power_label.grid(row=0, column=1)

        #################################### Frame 4 ####################################

        self.frame_4 = Frame(self.Table_Frame)
        self.frame_4.grid(row=4,column=0,columnspan=4)

        for i in range(0,4):

            Label(self.frame_4, text="", height=1).grid(row=0, column=i)

        #################################### Frame 5 ####################################

        self.frame_5 = Frame(self.Table_Frame)
        self.frame_5.grid(row=5,column=0,columnspan=4)

        self.P_label = Label(self.frame_5,text="P",bg="light gray", fg="black", width=15, relief="solid")#, padx=1, pady=1)
        self.P_label.grid(row=0,column=0,padx=1,pady=1,sticky='N')

        self.I_label = Label(self.frame_5,text="I",bg="light gray", fg="black", width=15, relief="solid")#, padx=1, pady=1)
        self.I_label.grid(row=1,column=0,padx=1,pady=1,sticky='N')

        self.D_label = Label(self.frame_5,text="D",bg="light gray", fg="black", width=15, relief="solid")#, padx=1, pady=1)
        self.D_label.grid(row=2,column=0,padx=1,pady=1,sticky='N')

        self.SC_P = Entry(self.frame_5, bg="gray", fg="white", width=13)

        self.SC_P.grid(row=0,column=1, sticky="ew", padx=1, pady=1)

        self.SC_P.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.CC_P = Entry(self.frame_5, bg="gray", fg="white", width=13)

        self.CC_P.grid(row=0,column=2, sticky="ew", padx=1, pady=1)

        self.CC_P.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.DPG_P = Entry(self.frame_5, bg="gray", fg="white", width=13)

        self.DPG_P.grid(row=0,column=3, sticky="ew", padx=1, pady=1)

        self.DPG_P.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.SC_I = Entry(self.frame_5, bg="gray", fg="white", width=13)

        self.SC_I.grid(row=1,column=1, sticky="ew", padx=1, pady=1)

        self.SC_I.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.CC_I = Entry(self.frame_5, bg="gray", fg="white", width=13)

        self.CC_I.grid(row=1,column=2, sticky="ew", padx=1, pady=1)

        self.CC_I.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.DPG_I = Entry(self.frame_5, bg="gray", fg="white", width=13)

        self.DPG_I.grid(row=1,column=3, sticky="ew", padx=1, pady=1)

        self.DPG_I.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.SC_D = Entry(self.frame_5, bg="gray", fg="white", width=13)

        self.SC_D.grid(row=2,column=1, sticky="ew", padx=1, pady=1)

        self.SC_D.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.CC_D = Entry(self.frame_5, bg="gray", fg="white", width=13)

        self.CC_D.grid(row=2,column=2, sticky="ew", padx=1, pady=1)

        self.CC_D.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.DPG_D = Entry(self.frame_5, bg="gray", fg="white", width=13)

        self.DPG_D.grid(row=2,column=3, sticky="ew", padx=1, pady=1)

        self.DPG_D.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.PID_apply_label =  Label(self.frame_5,text="",bg="light gray", fg="black", width=15, relief="solid")

        self.PID_apply_label.grid(row=3, column=0)

        self.SC_PID_apply_outer_frame = Label(self.frame_5, text="", bg="white", fg="black", width=13, relief="solid")

        self.SC_PID_apply_outer_frame.grid(row=3,column=1)

        self.CC_PID_apply_outer_frame = Label(self.frame_5, text="", bg="white", fg="black", width=13, relief="solid")

        self.CC_PID_apply_outer_frame.grid(row=3,column=2)

        self.DPG_PID_apply_outer_frame = Label(self.frame_5, text="", bg="white", fg="black", width=13, relief="solid")

        self.DPG_PID_apply_outer_frame.grid(row=3,column=3)

        self.SC_PID_apply_var = StringVar()

        self.SC_PID_apply = Button(self.frame_5, textvariable=self.SC_PID_apply_var, bg="white", fg="black", command=self.SC_PID_start_stop)

        self.SC_PID_apply.grid(row=3, column=1, padx=1, pady=1)

        self.SC_PID_apply.config(width=8, bd=0, height=1, relief='flat')

        self.SC_PID_apply_var.set("Apply")

        self.CC_PID_apply_var = StringVar()

        self.CC_PID_apply = Button(self.frame_5, textvariable=self.CC_PID_apply_var, bg="white", fg="black", command=self.CC_PID_start_stop)

        self.CC_PID_apply.grid(row=3, column=2, padx=1, pady=1)

        self.CC_PID_apply.config(width=8, bd=0, height=1, relief='flat')

        self.CC_PID_apply_var.set("Apply")

        self.DPG_PID_apply_var = StringVar()

        self.DPG_PID_apply = Button(self.frame_5, textvariable=self.DPG_PID_apply_var, bg="white", fg="black", command=self.DPG_PID_start_stop)

        self.DPG_PID_apply.config(width=8, bd=0, height=1, relief='flat')
        
        self.DPG_PID_apply.grid(row=3, column=3, padx=1, pady=1)

        self.DPG_PID_apply_var.set("Apply")


        #################################### Frame 6 ####################################

        self.frame_6 = Frame(self.Table_Frame)
        self.frame_6.grid(row=6,column=0,columnspan=4)

        for i in range(0,4):

            Label(self.frame_6, text="", height=1).grid(row=0, column=i)

        #################################### Frame 7 ####################################

        self.frame_7 = Frame(self.Table_Frame)
        self.frame_7.grid(row=7,column=0,columnspan=4)

        self.Set_label = Label(self.frame_7,text="Set",bg="light gray", fg="black", width=15, relief="solid")#, padx=1, pady=1)
        self.Set_label.grid(row=0,column=0,padx=1,pady=1,sticky='N')

        self.SC_Set = Entry(self.frame_7, bg="gray", fg="white", width=13)

        self.SC_Set.grid(row=0,column=1, sticky="ew", padx=1, pady=1)

        self.SC_Set.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.CC_Set = Entry(self.frame_7, bg="gray", fg="white", width=13)

        self.CC_Set.grid(row=0,column=2, sticky="ew", padx=1, pady=1)

        self.CC_Set.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.DPG_Set = Entry(self.frame_7, bg="gray", fg="white", width=13)

        self.DPG_Set.grid(row=0,column=3, sticky="ew", padx=1, pady=1)

        self.DPG_Set.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.SC_SetPoint_apply = Button(self.frame_7, text="Apply")

        self.SC_SetPoint_apply.grid(row=1, column=1)#, sticky='w')

        self.SC_SetPoint_apply.config(bd=0, height=1, relief='flat')

        self.CC_SetPoint_apply = Button(self.frame_7, text="Apply")

        self.CC_SetPoint_apply.grid(row=1, column=2)#, sticky='w')

        self.CC_SetPoint_apply.config(bd=0, height=1, relief='flat')

        self.DPG_SetPoint_apply = Button(self.frame_7, text="Apply")

        self.DPG_SetPoint_apply.grid(row=1, column=3)#, sticky='w')

        self.DPG_SetPoint_apply.config(bd=0, height=1, relief='flat')



        self.Set_apply_label =  Label(self.frame_7,text="",bg="light gray", fg="black", width=15, relief="solid")

        self.Set_apply_label.grid(row=1, column=0)

        self.SC_Set_apply_outer_frame = Label(self.frame_7, text="", bg="white", fg="black", width=13, relief="solid")

        self.SC_Set_apply_outer_frame.grid(row=1,column=1)

        self.CC_Set_apply_outer_frame = Label(self.frame_7, text="", bg="white", fg="black", width=13, relief="solid")

        self.CC_Set_apply_outer_frame.grid(row=1,column=2)

        self.DPG_Set_apply_outer_frame = Label(self.frame_7, text="", bg="white", fg="black", width=13, relief="solid")

        self.DPG_Set_apply_outer_frame.grid(row=1,column=3)

        self.SC_Set_apply_var = StringVar()

        self.SC_Set_apply = Button(self.frame_7, textvariable=self.SC_Set_apply_var, bg="white", fg="black", command=self.SC_Set_start_stop)

        self.SC_Set_apply.grid(row=1, column=1, padx=1, pady=1)

        self.SC_Set_apply.config(width=8, bd=0, height=1, relief='flat')

        self.SC_Set_apply_var.set("Apply")

        self.CC_Set_apply_var = StringVar()

        self.CC_Set_apply = Button(self.frame_7, textvariable=self.CC_Set_apply_var, bg="white", fg="black", command=self.CC_Set_start_stop)

        self.CC_Set_apply.grid(row=1, column=2, padx=1, pady=1)

        self.CC_Set_apply.config(width=8, bd=0, height=1, relief='flat')

        self.CC_Set_apply_var.set("Apply")

        self.DPG_Set_apply_var = StringVar()

        self.DPG_Set_apply = Button(self.frame_7, textvariable=self.DPG_Set_apply_var, bg="white", fg="black", command=self.DPG_Set_start_stop)

        self.DPG_Set_apply.config(width=8, bd=0, height=1, relief='flat')
        
        self.DPG_Set_apply.grid(row=1, column=3, padx=1, pady=1)

        self.DPG_Set_apply_var.set("Apply")


        ''' 
        for i in [8, 10]:

            label = Label(self.Table_Frame,text=var_names_dummy[i],bg=colors[i-1],fg="black", width=12, relief="solid")#, padx=1, pady=1)

            label.grid(row=i,column=1, padx=1,pady=1, sticky='ew')

            label.config(highlightbackground="black") 

            label = Label(self.Table_Frame,text=var_names_dummy[i],bg=colors[i-1],fg="black", width=12, relief="solid")#, padx=1, pady=1)

            label.grid(row=i,column=2, padx=1,pady=1, sticky='ew')

            label.config(highlightbackground="black") 

            label = Label(self.Table_Frame,text=var_names_dummy[i],bg=colors[i-1],fg="black", width=12, relief="solid")#, padx=1, pady=1)

            label.grid(row=i,column=3, padx=1,pady=1, sticky='ew')

            label.config(highlightbackground="black") 


        self.SC_power = StringVar()
        self.SC_power.set("0") # initialize

        sticky_list = ['e','w']

       

        '''

    def SC_power_switch(self, value):

        self.SC_power.set(self.MODES[self.SC_power_scale.get()])

        if self.SC_power_scale.get():

            self.SC_power_label.grid(row=0, column=1, sticky='E')

        else:

             self.SC_power_label.grid(row=0, column=1, sticky='E')

    def CC_power_switch(self, value):

        self.CC_power.set(self.MODES[self.CC_power_scale.get()])

        if self.CC_power_scale.get():

            self.CC_power_label.grid(row=0, column=2, sticky='E')

        else:

             self.CC_power_label.grid(row=0, column=2, sticky='E')


    def DPG_power_switch(self, value):

        self.DPG_power.set(self.MODES[self.DPG_power_scale.get()])

        if self.DPG_power_scale.get():

            self.DPG_power_label.grid(row=0, column=3, sticky='E')

        else:

             self.DPG_power_label.grid(row=0, column=3, sticky='E')

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

        outputstring= ""

        if self.calib_check_var.get():

            self.TSC.set(str(self.g_sys_instance.Temperatures_SC[-1]))

            self.TCC.set(str(self.g_sys_instance.Temperatures_CC[-1]))

            self.TDPG.set(str(self.g_sys_instance.Temperatures_DPG[-1]))

            if self.check_var1.get():

                self.ax1.plot(self.g_sys_instance.time_list[(25000-self.plot_density*index):], self.g_sys_instance.Temperatures_SC[(25000-self.plot_density*index):], 'k', label="TSC")
                
                self.ax1.legend()
                
                #self.plot_label_variable.set("  Sample Chamber Temperature")

            if self.check_var2.get():

                self.ax1.plot(self.g_sys_instance.time_list[(25000-self.plot_density*index):], self.g_sys_instance.Temperatures_CC[(25000-self.plot_density*index):], 'b', label="TCC")

                self.ax1.legend()

                #self.plot_label_variable.set("  Conditioning Chamber Temperature")

            if self.check_var3.get():
                
                self.ax1.plot(self.g_sys_instance.time_list[(25000-self.plot_density*index):], self.g_sys_instance.Temperatures_DPG[(25000-self.plot_density*index):], 'r', label="TDPG")

                self.ax1.legend()

                #self.plot_label_variable.set("  Dew Point Generator Temperature")

            outputstring=""


    def SC_PID_start_stop(self):

        if self.SC_PID_apply_var.get() == "Apply":

            self.SC_PID_apply_var.set("Stop")

            self.SC_P.config(bg='light gray', fg='black')

            self.SC_I.config(bg='light gray', fg='black')

            self.SC_D.config(bg='light gray', fg='black')

        else:

            self.SC_PID_apply_var.set("Apply")

            self.SC_P.config(bg='gray', fg = "white")

            self.SC_I.config(bg='gray', fg = "white")

            self.SC_D.config(bg='gray', fg = "white")


    def CC_PID_start_stop(self):

        if self.CC_PID_apply_var.get() == "Apply":

            self.CC_PID_apply_var.set("Stop")

            self.CC_P.config(bg='light gray', fg='black')

            self.CC_I.config(bg='light gray', fg='black')

            self.CC_D.config(bg='light gray', fg='black')

        else:

            self.CC_PID_apply_var.set("Apply")

            self.CC_P.config(bg='gray', fg = "white")

            self.CC_I.config(bg='gray', fg = "white")

            self.CC_D.config(bg='gray', fg = "white")

    def DPG_PID_start_stop(self):

        if self.DPG_PID_apply_var.get() == "Apply":

            self.DPG_PID_apply_var.set("Stop")

            self.DPG_P.config(bg='light gray', fg='black')

            self.DPG_I.config(bg='light gray', fg='black')

            self.DPG_D.config(bg='light gray', fg='black')

        else:

            self.DPG_PID_apply_var.set("Apply")

            self.DPG_P.config(bg='gray', fg = "white")

            self.DPG_I.config(bg='gray', fg = "white")

            self.DPG_D.config(bg='gray', fg = "white")

    def SC_Set_start_stop(self):

        if self.SC_Set_apply_var.get() == "Apply":

            self.SC_Set_apply_var.set("Stop")

            self.SC_Set.config(bg='light gray', fg='black')

        else:

            self.SC_Set_apply_var.set("Apply")

            self.SC_Set.config(bg='gray', fg = "white")


    def CC_Set_start_stop(self):

        if self.CC_Set_apply_var.get() == "Apply":

            self.CC_Set_apply_var.set("Stop")

            self.CC_Set.config(bg='light gray', fg='black')

        else:

            self.CC_Set_apply_var.set("Apply")

            self.CC_Set.config(bg='gray', fg = "white")

    def DPG_Set_start_stop(self):

        if self.DPG_Set_apply_var.get() == "Apply":

            self.DPG_Set_apply_var.set("Stop")

            self.DPG_Set.config(bg='light gray', fg='black')

        else:

            self.DPG_Set_apply_var.set("Apply")

            self.DPG_Set.config(bg='gray', fg = "white")