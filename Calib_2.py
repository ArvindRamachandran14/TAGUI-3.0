from tkinter import Frame, LabelFrame, Label, Spinbox, Button, Text, StringVar, Radiobutton, OptionMenu, Entry, Scale, HORIZONTAL, Checkbutton, IntVar, messagebox, VERTICAL
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from datetime import datetime
import time
from math import exp
import scipy.optimize as opt

class Calib(Frame) :

    def __init__(self, parent, g_sys_instance, g_cal_instance, cons, *args, **kwargs) :
        Frame.__init__(self, *args, **kwargs)
        self.check_button_frame = Frame(self,padx=2, pady=2)
        #self.check_button_frame.grid(row=0,column=0,sticky='NW')

        self.Table_Frame = Frame(self, padx=20)

        self.Table_Frame.grid(row=0, column=0, sticky='N')

        self.Partition_Frame = Frame(self)

        self.Partition_Frame.grid(row=0, column=1, sticky='N')

        self.Graph_Frame = Frame(self)#, padx=50)

        self.Graph_Frame.grid(row=0, column=2, sticky='NE')
 
        self.TC_Table_Frame = Frame(self.Table_Frame, highlightbackground='black', highlightthickness=2, relief='solid',padx=2, pady=2,height=300,width=400)

        self.TC_Table_Frame.grid(row=0, column=0, sticky='N')

        self.Table_space_frame =  Frame(self.Table_Frame, height=10)

        self.Table_space_frame.grid(row=1, column=0, sticky='N')

        self.Humidity_Table_Frame = Frame(self.Table_Frame, highlightbackground='black', highlightthickness=2, relief='solid',padx=2, pady=2)

        self.Humidity_Table_Frame.grid(row=2, column=0, sticky='NW')

        self.Graph_1_Frame = Frame(self.Graph_Frame)

        self.Graph_1_Frame.grid(row=0, column=0, sticky='N')

        self.Graph_2_Frame = Frame(self.Graph_Frame)

        self.Graph_2_Frame.grid(row=1, column=0, sticky='N')

        self.Slider_1_Frame = Frame(self.Graph_Frame)

        self.Slider_1_Frame.grid(row=0, column=1)

        self.Slider_2_Frame = Frame(self.Graph_Frame)

        self.Slider_2_Frame.grid(row=1, column=1)

        self.g_sys_instance = g_sys_instance
        self.g_cal_instance = g_cal_instance
        self.cons = cons
        self.plot_density = 7.5
        self.slider_list = [0,1,2,3,4]
        self.slider_list_value = [0.5,1,15,30,60]

        self.TSC = StringVar()

        self.TCC = StringVar()

        self.TDPG = StringVar()

        self.SC_output = StringVar()

        self.CC_output = StringVar()

        self.DPG_output = StringVar()

        self.SC_P = StringVar()

        self.SC_I = StringVar()

        self.SC_D = StringVar()

        self.CC_P = StringVar()

        self.CC_I = StringVar()

        self.CC_D = StringVar()

        self.DPG_P = StringVar()

        self.DPG_I = StringVar()

        self.DPG_D = StringVar()

        self.pH2O_P = StringVar()

        self.pH2O_I = StringVar()

        self.pH2O_D = StringVar()

        self.SC_set = StringVar()

        self.CC_set = StringVar()

        self.DPG_set = StringVar()

        self.TDP_set = StringVar()

        self.pH2O_set = StringVar()

        self.RH_set = StringVar()

        #self.parent = parent

        self.MODES = ['OFF', 'ON']

        self.build_TC_table()

        self.build_Humidity_table()

        self.buildFigure()

    def buildFigure(self) :


        Label(self.Partition_Frame, text="").grid(row=0,column=0)

        self.check_var1 = IntVar()
        Checkbutton(self.Partition_Frame, text="TSC", variable=self.check_var1).grid(row=1, column=0, sticky='W')
        self.check_var2 = IntVar()
        Checkbutton(self.Partition_Frame, text="TCC", variable=self.check_var2).grid(row=2, column=0, sticky='W')
        self.check_var3 = IntVar()
        Checkbutton(self.Partition_Frame, text="TDPG", variable=self.check_var3).grid(row=3, column=0, sticky='W')
        self.check_var4 = IntVar()
        Checkbutton(self.Partition_Frame, text="TDP", variable=self.check_var4).grid(row=4, column=0, sticky='W')
        self.check_var5 = IntVar()
        Checkbutton(self.Partition_Frame, text="SC Output", variable=self.check_var5).grid(row=5, column=0, sticky='W')
        self.check_var6 = IntVar()
        Checkbutton(self.Partition_Frame, text="CC Output", variable=self.check_var6).grid(row=6, column=0, sticky='W')
        self.check_var7 = IntVar()
        Checkbutton(self.Partition_Frame, text="DPG Output", variable=self.check_var7).grid(row=7, column=0, sticky='W')



        self.output = StringVar()

        self.scale_1_textvariable = StringVar()
        self.scale_2_textvariable = StringVar()

        self.fig1 = Figure(figsize=(4, 3))
        self.ax1 = self.fig1.add_subplot(111)

        self.ax1.set_xlabel('Time (sec)')
        self.ax1.set_ylabel('Temperature ($^\circ$C)')

        self.ax1.set_autoscalex_on(True)
        #self.ax1.set_ybound(10, 40)
        self.ax1.set_autoscaley_on(True)
        self.ax1.grid(True, 'major', 'both')
        self.ax1_twin = self.ax1.twinx()
        self.ax1_twin.set_ylabel('Controller power output')
        self.ax1_twin.set_autoscalex_on(True)

        #self.ax1.tick_params('y', colors='b')
        #self.ax1_twin.tick_params('y', colors='r')

        self.fig1.tight_layout()
        self.cnvs1 = FigureCanvasTkAgg(self.fig1, self.Graph_1_Frame)
        self.cnvs1.get_tk_widget().grid(row=0, column=0, sticky='N')
        self.scale_1 = Scale(self.Slider_1_Frame, from_=min(self.slider_list), to=max(self.slider_list), command=self.scale_1_value_show, showvalue=0, orient=VERTICAL)#, command=set_plot_range(1))
        self.scale_1.grid(row=0, column=0)
        self.scale_1_textvariable.set('Plot range(m): '+ str(self.slider_list_value[0]))
        self.scale_1_label = Label(self.Slider_1_Frame, textvariable=self.scale_1_textvariable,width=15)
        self.scale_1_label.grid(row=0,column=1)

        self.fig2 = Figure(figsize=(4,3))
        self.ax2 = self.fig2.add_subplot(111)

        self.ax2.set_xlabel('Time (sec)')
        self.ax2.set_ylabel('RH (%)')

        self.ax2.set_autoscalex_on(True)
        #self.ax2.set_ybound(10, 40)
        self.ax2.set_autoscaley_on(True)
        self.ax2.grid(True, 'major', 'both')
        
        self.ax2_twin = self.ax2.twinx()
        self.ax2_twin.set_ylabel('pH2O (ppt)')
        self.ax2_twin.set_autoscalex_on(True)
        self.ax2.tick_params('y', colors='b')
        self.ax2_twin.tick_params('y', colors='r')



        self.fig2.tight_layout()
        self.cnvs2 = FigureCanvasTkAgg(self.fig2, self.Graph_2_Frame)
        self.cnvs2.get_tk_widget().grid(row=0, column=0, sticky='N')
        self.scale_2 = Scale(self.Slider_2_Frame, from_=min(self.slider_list), to=max(self.slider_list), command=self.scale_2_value_show, showvalue=0, orient=VERTICAL)#, command=set_plot_range(1))
        self.scale_2.grid(row=0, column=0)
        self.scale_2_textvariable.set('Plot range(m): '+ str(self.slider_list_value[0]))
        self.scale_2_label = Label(self.Slider_2_Frame, textvariable=self.scale_2_textvariable,width=15)
        self.scale_2_label.grid(row=0, column=1)

 
    def build_TC_table(self):

        self.TC_table_label = Label(self.TC_Table_Frame, text="Temperature control")

        self.TC_table_label.grid(row=0,column=0)

        self.calib_check_var = IntVar()
        Checkbutton(self.TC_Table_Frame, text="Calibration mode", variable=self.calib_check_var, command=self.set_bcalibration, relief='flat').grid(row=0, column=3, sticky='E')

        var_names = ["Var name", "Measured T", "Output", "Power", "P", "I", "D", "", "Set Point", ""]

        colors = ["gray", "light gray", "light gray", "light gray", "gray", "gray", "gray",  "gray", "light gray", "light gray"]

        var_names_dummy = [""]*11

        #################################### Frame 1 ####################################

        self.TC_frame_1 = Frame(self.TC_Table_Frame)
        self.TC_frame_1.grid(row=1,column=0,columnspan=4, sticky='NW')

        for i in range(0,3):

            label = Label(self.TC_frame_1,text=var_names[i],bg="light gray", fg="black", width=13, relief="solid")#, padx=1, pady=1)

            label.grid(row=i,column=0,padx=1,pady=1,sticky='N')

            label.config(highlightbackground="black") 

        label_SC =  Label(self.TC_frame_1,text="SC", bg="light gray",fg="black", width=10, relief="solid")

        label_SC.grid(row=0,column=1, sticky="ew", padx=1, pady=1)

        label_SC.config(highlightbackground="black") 

        label_CC =  Label(self.TC_frame_1,text="CC", bg="light gray",fg="black", width=10, relief="solid")

        label_CC.grid(row=0,column=2, sticky="ew", padx=1, pady=1)

        label_CC.config(highlightbackground="black") 

        label_DPG =  Label(self.TC_frame_1,text="DPG", bg="light gray",fg="black", width=10, relief="solid")

        label_DPG.grid(row=0,column=3, sticky="ew", padx=1, pady=1)

        label_DPG.config(highlightbackground="black") 

        #label_pH2O =  Label(self.TC_frame_1,text="pH2O", bg="light gray",fg="black", width=10, relief="solid")

        #label_pH2O.grid(row=0,column=4, sticky="ew", padx=1, pady=1)

        #label_pH2O.config(highlightbackground="black")

        self.TSC_entry = Entry(self.TC_frame_1, bg="light gray", fg="black", width=11, textvariable=self.TSC)

        self.TSC_entry.grid(row=1,column=1, sticky="ew", padx=1, pady=1)

        self.TSC_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.TCC_entry = Entry(self.TC_frame_1, bg="light gray", fg="black", width=11, textvariable=self.TCC)

        self.TCC_entry.grid(row=1,column=2, sticky="ew", padx=1, pady=1)

        self.TCC_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.TDPG_entry = Entry(self.TC_frame_1, bg="light gray", fg="black", width=11, textvariable=self.TDPG)

        self.TDPG_entry.grid(row=1,column=3, sticky="ew", padx=1, pady=1)

        self.TDPG_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.SC_output_entry = Entry(self.TC_frame_1, bg="light gray", fg="black", width=11, textvariable=self.SC_output)

        self.SC_output_entry.grid(row=2,column=1, sticky="ew", padx=1, pady=1)

        self.SC_output_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.CC_output_entry = Entry(self.TC_frame_1, bg="light gray", fg="black", width=11, textvariable=self.CC_output)

        self.CC_output_entry.grid(row=2,column=2, sticky="ew", padx=1, pady=1)

        self.CC_output_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.DPG_output_entry = Entry(self.TC_frame_1, bg="light gray", fg="black", width=11, textvariable=self.DPG_output)

        self.DPG_output_entry.grid(row=2,column=3, sticky="ew", padx=1, pady=1)

        self.DPG_output_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        #################################### Frame 2 ####################################

        self.TC_frame_2 = Frame(self.TC_Table_Frame, height=5)
        self.TC_frame_2.grid(row=2,column=0,columnspan=4, sticky='NW')

        #for i in range(0,4):

        #Label(self.TC_frame_2, text="",height=1).grid(row=0, column=i,sticky='N')

        #################################### Frame 3 ####################################

        self.TC_frame_3 = Frame(self.TC_Table_Frame)
        self.TC_frame_3.grid(row=3,column=0,columnspan=4, sticky='NSEW')

        self.power_label = Label(self.TC_frame_3,text="Power",bg="light gray", fg="black", width=13, relief="solid")#, padx=1, pady=1)
        self.power_label.grid(row=0,column=0,padx=1,pady=1,sticky='NSEW')

        self.SC_power_outer_frame =  Label(self.TC_frame_3, text="", bg="white", fg="black", width=11, relief="solid")
        self.SC_power_outer_frame.grid(row=0, column=1, sticky="ew", padx=1, pady=1)

        #self.SC_power_outer_frame = Label(self.TC_frame_3, text="", bg="white", fg="black", relief="solid", width=10)#, padx=1, pady=1)
        #self.SC_power_outer_frame.grid(row=0, column=1, padx=1, pady=1, sticky='NSEW')

        self.SC_power_frame = Frame(self.TC_frame_3)
        self.SC_power_frame.grid(row=0, column=1)

        self.SC_power = StringVar()
        self.SC_power.set("0") # initialize

        self.SC_power_scale = Scale(self.SC_power_frame, from_=0, to=1, showvalue=0, length=50, orient=HORIZONTAL, command=self.SC_power_switch)#, command=set_plot_range(1))
        self.SC_power_scale.grid(row=0, column=0, sticky='NW')
        self.SC_power_scale.config(highlightthickness=1, width=14)
        self.SC_power_label = Label(self.SC_power_frame, textvariable=self.SC_power, height=1, font=("TkDefaultFont", 11))
        self.SC_power.set(self.MODES[0])
        self.SC_power_label.grid(row=0, column=1)

        self.CC_power_outer_frame = Label(self.TC_frame_3, text="", bg="white", fg="black", width=11, relief="solid")#, padx=1, pady=1)
        self.CC_power_outer_frame.grid(row=0, column=2, padx=1, pady=1, sticky='ew')

        self.CC_power_frame = Frame(self.TC_frame_3)
        self.CC_power_frame.grid(row=0, column=2)

        self.CC_power = StringVar()
        self.CC_power.set("0") # initialize
        self.CC_power_scale = Scale(self.CC_power_frame, from_=0, to=1, showvalue=0, length=50, orient=HORIZONTAL, command=self.CC_power_switch)#, command=set_plot_range(1))
        self.CC_power_scale.grid(row=0, column=0)
        self.CC_power_scale.config(highlightthickness=1, width=14)
        self.CC_power_label = Label(self.CC_power_frame, textvariable=self.CC_power, height=1, font=("TkDefaultFont", 11))
        self.CC_power.set(self.MODES[0])
        self.CC_power_label.grid(row=0, column=1)

        self.DPG_power_outer_frame = Label(self.TC_frame_3, text="", bg="white", fg="black", relief="solid", width=11)#, padx=1, pady=1)
        self.DPG_power_outer_frame.grid(row=0, column=3, padx=1, pady=1, sticky='ew')

        self.DPG_power_frame = Frame(self.TC_frame_3)
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

        self.TC_frame_4 = Frame(self.TC_Table_Frame, height=5)
        self.TC_frame_4.grid(row=4,column=0,columnspan=4,sticky='w')

        #for i in range(0,4):

        #Label(self.TC_frame_4, text="", height=1).grid(row=0, column=i)

        #################################### Frame 5 ####################################

        self.TC_frame_5 = Frame(self.TC_Table_Frame)
        self.TC_frame_5.grid(row=5,column=0,columnspan=4,sticky='w')

        self.P_label = Label(self.TC_frame_5,text="P",bg="light gray", fg="black", width=13, relief="solid")#, padx=1, pady=1)
        self.P_label.grid(row=0,column=0,padx=1,pady=1,sticky='N')

        self.I_label = Label(self.TC_frame_5,text="I",bg="light gray", fg="black", width=13, relief="solid")#, padx=1, pady=1)
        self.I_label.grid(row=1,column=0,padx=1,pady=1,sticky='N')

        self.D_label = Label(self.TC_frame_5,text="D",bg="light gray", fg="black", width=13, relief="solid")#, padx=1, pady=1)
        self.D_label.grid(row=2,column=0,padx=1,pady=1,sticky='N')

        self.SC_P_entry = Entry(self.TC_frame_5, bg="gray", fg="white", width=11, textvariable=self.SC_P)

        self.SC_P_entry.grid(row=0,column=1, sticky="ew", padx=1, pady=1)

        self.SC_P_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.CC_P_entry = Entry(self.TC_frame_5, bg="gray", fg="white", width=11, textvariable=self.CC_P)

        self.CC_P_entry.grid(row=0,column=2, sticky="ew", padx=1, pady=1)

        self.CC_P_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.DPG_P_entry = Entry(self.TC_frame_5, bg="gray", fg="white", width=11, textvariable=self.DPG_P)

        self.DPG_P_entry.grid(row=0,column=3, sticky="ew", padx=1, pady=1)

        self.DPG_P_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')  

        self.SC_I_entry = Entry(self.TC_frame_5, bg="gray", fg="white", width=11, textvariable=self.SC_I)

        self.SC_I_entry.grid(row=1,column=1, sticky="ew", padx=1, pady=1)

        self.SC_I_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.CC_I_entry = Entry(self.TC_frame_5, bg="gray", fg="white", width=11, textvariable=self.CC_I)

        self.CC_I_entry.grid(row=1,column=2, sticky="ew", padx=1, pady=1)

        self.CC_I_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.DPG_I_entry = Entry(self.TC_frame_5, bg="gray", fg="white", width=11, textvariable=self.DPG_I)

        self.DPG_I_entry.grid(row=1,column=3, sticky="ew", padx=1, pady=1)

        self.DPG_I_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.SC_D_entry = Entry(self.TC_frame_5, bg="gray", fg="white", width=11, textvariable=self.SC_D)

        self.SC_D_entry.grid(row=2,column=1, sticky="ew", padx=1, pady=1)

        self.SC_D_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.CC_D_entry = Entry(self.TC_frame_5, bg="gray", fg="white", width=11, textvariable=self.CC_D)

        self.CC_D_entry.grid(row=2,column=2, sticky="ew", padx=1, pady=1)

        self.CC_D_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.DPG_D_entry = Entry(self.TC_frame_5, bg="gray", fg="white", width=11, textvariable=self.DPG_D)

        self.DPG_D_entry.grid(row=2,column=3, sticky="ew", padx=1, pady=1)

        self.DPG_D_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.PID_apply_label =  Label(self.TC_frame_5,text="",bg="light gray", fg="black", width=13, relief="solid")

        self.PID_apply_label.grid(row=3, column=0)

        self.SC_PID_apply_outer_frame = Label(self.TC_frame_5, text="", bg="white", fg="black", width=11, relief="solid")

        self.SC_PID_apply_outer_frame.grid(row=3,column=1)

        self.CC_PID_apply_outer_frame = Label(self.TC_frame_5, text="", bg="white", fg="black", width=11, relief="solid")

        self.CC_PID_apply_outer_frame.grid(row=3,column=2)

        self.DPG_PID_apply_outer_frame = Label(self.TC_frame_5, text="", bg="white", fg="black", width=11, relief="solid")

        self.DPG_PID_apply_outer_frame.grid(row=3,column=3)

        self.SC_PID_apply_var = StringVar()

        self.SC_PID_apply = Button(self.TC_frame_5, textvariable=self.SC_PID_apply_var, bg="white", fg="black", command=self.SC_PID_apply_func)

        self.SC_PID_apply.grid(row=3, column=1, padx=1, pady=1)

        self.SC_PID_apply.config(width=8, bd=0, height=1, relief='flat')

        self.SC_PID_apply_var.set("Apply")

        self.CC_PID_apply_var = StringVar()

        self.CC_PID_apply = Button(self.TC_frame_5, textvariable=self.CC_PID_apply_var, bg="white", fg="black", command=self.CC_PID_apply_func)

        self.CC_PID_apply.grid(row=3, column=2, padx=1, pady=1)

        self.CC_PID_apply.config(width=8, bd=0, height=1, relief='flat')

        self.CC_PID_apply_var.set("Apply")

        self.DPG_PID_apply_var = StringVar()

        self.DPG_PID_apply = Button(self.TC_frame_5, textvariable=self.DPG_PID_apply_var, bg="white", fg="black", command=self.DPG_PID_apply_func)

        self.DPG_PID_apply.config(width=8, bd=0, height=1, relief='flat')
        
        self.DPG_PID_apply.grid(row=3, column=3, padx=1, pady=1)

        self.DPG_PID_apply_var.set("Apply")

        #################################### Frame 6 ####################################

        self.TC_frame_6 = Frame(self.TC_Table_Frame, height=5)
        self.TC_frame_6.grid(row=6,column=0,columnspan=4,sticky='w')

        #for i in range(0,4):

        #Label(self.TC_frame_6, text="", height=1).grid(row=0, column=i)

        #################################### Frame 7 ####################################

        self.TC_frame_7 = Frame(self.TC_Table_Frame)
        self.TC_frame_7.grid(row=7,column=0,columnspan=4,sticky='w')

        self.Set_label = Label(self.TC_frame_7,text="Set",bg="light gray", fg="black", width=13, relief="solid")#, padx=1, pady=1)
        self.Set_label.grid(row=0,column=0,padx=1,pady=1,sticky='N')

        self.SC_set_entry = Entry(self.TC_frame_7, bg="gray", fg="white", width=11, textvariable=self.SC_set)

        self.SC_set_entry.grid(row=0,column=1, sticky="ew", padx=1, pady=1)

        self.SC_set_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.CC_set_entry = Entry(self.TC_frame_7, bg="gray", fg="white", width=11, textvariable=self.CC_set)

        self.CC_set_entry.grid(row=0,column=2, sticky="ew", padx=1, pady=1)

        self.CC_set_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.DPG_set_entry = Entry(self.TC_frame_7, bg="gray", fg="white", width=11, textvariable=self.DPG_set)

        self.DPG_set_entry.grid(row=0,column=3, sticky="ew", padx=1, pady=1)

        self.DPG_set_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')

        self.Set_apply_label =  Label(self.TC_frame_7,text="",bg="light gray", fg="black", width=13, relief="solid")

        self.Set_apply_label.grid(row=1, column=0)

        self.SC_set_apply_outer_frame = Label(self.TC_frame_7, text="", bg="white", fg="black", width=11, relief="solid")

        self.SC_set_apply_outer_frame.grid(row=1,column=1)

        self.CC_set_apply_outer_frame = Label(self.TC_frame_7, text="", bg="white", fg="black", width=11, relief="solid")

        self.CC_set_apply_outer_frame.grid(row=1,column=2)

        self.DPG_set_apply_outer_frame = Label(self.TC_frame_7, text="", bg="white", fg="black", width=11, relief="solid")

        self.DPG_set_apply_outer_frame.grid(row=1,column=3)

        self.SC_set_apply_var = StringVar()

        self.SC_set_apply = Button(self.TC_frame_7, textvariable=self.SC_set_apply_var, bg="white", fg="black", command=self.SC_set_apply_func)

        self.SC_set_apply.grid(row=1, column=1, padx=1, pady=1)

        self.SC_set_apply.config(width=8, bd=0, height=1, relief='flat')

        self.SC_set_apply_var.set("Apply")

        self.CC_set_apply_var = StringVar()

        self.CC_set_apply = Button(self.TC_frame_7, textvariable=self.CC_set_apply_var, bg="white", fg="black", command=self.CC_set_apply_func)

        self.CC_set_apply.grid(row=1, column=2, padx=1, pady=1)

        self.CC_set_apply.config(width=8, bd=0, height=1, relief='flat')

        self.CC_set_apply_var.set("Apply")

        self.DPG_set_apply_var = StringVar()

        self.DPG_set_apply = Button(self.TC_frame_7, textvariable=self.DPG_set_apply_var, bg="white", fg="black", command=self.DPG_set_apply_func)

        self.DPG_set_apply.config(width=8, bd=0, height=1, relief='flat')
        
        self.DPG_set_apply.grid(row=1, column=3, padx=1, pady=1)

        self.DPG_set_apply_var.set("Apply")

        #self.TC_frame_8 = Frame(self.TC_Table_Frame, height=10)
        #self.TC_frame_8.grid(row=8,column=0,columnspan=4,sticky='w')

    def build_Humidity_table(self):

        self.Humidity_table_label = Label(self.Humidity_Table_Frame, text="Humidity control")

        self.Humidity_table_label.grid(row=0,column=0,sticky='N')

        Humidity_table_var_names = ["TDPG", "RH (%)", "pH2O (ppt)", " ",  "P", "I", "D", ""]

        for i in range(0,len(Humidity_table_var_names)):

            label = Label(self.Humidity_Table_Frame, text=Humidity_table_var_names[i], bg="light gray", fg="black", width=13, relief="solid")#, padx=1, pady=1)

            label.grid(row=i+1, column=0, padx=1, pady=1, sticky='N')

            label.config(highlightbackground="black") 


        ###################### Set Points ########################

        self.TDP_set_entry = Entry(self.Humidity_Table_Frame, bg="gray", fg="white", width=11, textvariable=self.TDP_set)

        self.TDP_set_entry.grid(row=1, column=1, sticky="ew", padx=1, pady=1)

        self.TDP_set_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')      

        self.RH_set_entry = Entry(self.Humidity_Table_Frame, bg="gray", fg="white", width=11, textvariable=self.RH_set)

        self.RH_set_entry.grid(row=2, column=1, sticky="ew", padx=1, pady=1)

        self.RH_set_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')      

        self.pH2O_set_entry = Entry(self.Humidity_Table_Frame, bg="gray", fg="white", width=11, textvariable=self.pH2O_set)

        self.pH2O_set_entry.grid(row=3, column=1, sticky="ew", padx=1, pady=1)

        self.pH2O_set_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')      

        self.pH2O_set_apply_outer_frame = Label(self.Humidity_Table_Frame, text="", bg="white", fg="black", width=11, relief="solid")

        self.pH2O_set_apply_outer_frame.grid(row=4,column=1)

        self.pH2O_set_apply_var = StringVar()

        self.pH2O_set_apply = Button(self.Humidity_Table_Frame, textvariable=self.pH2O_set_apply_var, bg="white", fg="black", command=self.pH2O_set_apply_func)

        self.pH2O_set_apply.config(width=8, bd=0, height=1, relief='flat')
        
        self.pH2O_set_apply.grid(row=4, column=1, padx=1, pady=1)

        self.pH2O_set_apply_var.set("Apply")


        ###################### PID ########################

        self.pH2O_P_entry = Entry(self.Humidity_Table_Frame, bg="gray", fg="white", width=11, textvariable=self.pH2O_P) 

        self.pH2O_P_entry.grid(row=5, column=1, sticky="ew", padx=1, pady=1)

        self.pH2O_P_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right')      

        self.pH2O_I_entry = Entry(self.Humidity_Table_Frame, bg="gray", fg="white", width=11, textvariable=self.pH2O_I) 

        self.pH2O_I_entry.grid(row=6,column=1, sticky="ew", padx=1, pady=1)

        self.pH2O_I_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right') 

        self.pH2O_D_entry = Entry(self.Humidity_Table_Frame, bg="gray", fg="white", width=11, textvariable=self.pH2O_D) 

        self.pH2O_D_entry.grid(row=7,column=1, sticky="ew", padx=1, pady=1)

        self.pH2O_D_entry.config(highlightbackground="black", highlightthickness=0, relief='solid', justify='right') 

        self.pH2O_PID_apply_outer_frame = Label(self.Humidity_Table_Frame, text="", bg="white", fg="black", width=11, relief="solid")

        self.pH2O_PID_apply_outer_frame.grid(row=8,column=1)

        self.pH2O_PID_apply_var = StringVar()

        self.pH2O_PID_apply = Button(self.Humidity_Table_Frame, textvariable=self.pH2O_PID_apply_var, bg="white", fg="black", command=self.pH2O_PID_apply_func)

        self.pH2O_PID_apply.config(width=8, bd=0, height=1, relief='flat')
        
        self.pH2O_PID_apply.grid(row=8, column=1, padx=1, pady=1)

        self.pH2O_PID_apply_var.set("Apply")


    def SC_power_switch(self, value):

        self.g_cal_instance.SC_power = int(self.SC_power_scale.get())

        reply = self.cons.send_command_to_PC('s SC_power '+str(self.SC_power_scale.get()))

        if reply == 'e 0\n':

            self.SC_power.set(self.MODES[self.SC_power_scale.get()])

    def CC_power_switch(self, value):

        self.g_cal_instance.CC_power = int(self.SC_power_scale.get())

        reply = self.cons.send_command_to_PC('s CC_power '+str(self.CC_power_scale.get()))

        if reply == 'e 0\n':    

            self.CC_power.set(self.MODES[self.CC_power_scale.get()])

    def DPG_power_switch(self, value):

        self.g_cal_instance.DPG_power = int(self.DPG_power_scale.get())

        reply = self.cons.send_command_to_PC('s DPG_power '+str(self.DPG_power_scale.get()))

        if reply == 'e 0\n':    

            self.DPG_power.set(self.MODES[self.DPG_power_scale.get()])

    def set_bcalibration(self):

        if self.calib_check_var.get():

            self.g_cal_instance.bcalibration = True

        else:

            self.g_cal_instance.bcalibration = False

    def scale_1_value_show(self, value):
        
        self.scale_1_textvariable.set('Plot range(m): '+ str(self.slider_list_value[int(value)]))

    def scale_2_value_show(self, value):
        
        self.scale_2_textvariable.set('Plot range(m): '+ str(self.slider_list_value[int(value)]))

    def animate_temperatures(self, i):
        
        self.ax1.clear()
        self.ax1_twin.clear()
        self.ax1.set_xlabel('Time (sec)')
        self.ax1.set_ylabel('Temperature ($^\circ$C)')
        self.ax1.set_autoscalex_on(True)
        self.ax1_twin.set_autoscalex_on(True)
        #self.ax1.set_ybound(10, 40)
        self.ax1.set_autoscaley_on(True)
        self.ax1.grid(True, 'major', 'both')
        self.ax1_twin.set_ylabel('Power Output (%)')

        self.ax2.clear()
        self.ax2_twin.clear()
        self.ax2.set_xlabel('Time (sec)')
        self.ax2.set_ylabel('RH (%)')
        self.ax2.set_autoscalex_on(True)
        self.ax2_twin.set_autoscalex_on(True)
        #self.ax1.set_ybound(10, 40)
        self.ax2.set_autoscaley_on(True)
        self.ax2.grid(True, 'major', 'both')
        self.ax2_twin.set_ylabel('pH2O (ppt)')

        self.plot_1_range = self.slider_list_value[int(self.scale_1.get())]*60 

        index = int(self.plot_1_range/15.0)

        outputstring= ""

        limit = 25000 - int(self.plot_density*index)

        if self.calib_check_var.get():

            if self.check_var1.get():

                self.ax1.plot(self.g_sys_instance.time_list[limit:], self.g_sys_instance.Temperatures_SC[limit:], 'k', label="TSC")

            if self.check_var2.get():

                self.ax1.plot(self.g_sys_instance.time_list[limit:], self.g_sys_instance.Temperatures_CC[limit:], 'b', label="TCC")

            if self.check_var3.get():
                    
                self.ax1.plot(self.g_sys_instance.time_list[limit:], self.g_sys_instance.Temperatures_DPG[limit:], 'r', label="TDPG")

            if self.check_var4.get():

                self.ax1.plot(self.g_sys_instance.time_list[limit:], self.g_sys_instance.Temperatures_DP[limit:], 'y', label="TDP")

            if self.check_var5.get():

                self.ax1_twin.plot(self.g_sys_instance.time_list[limit:], self.g_cal_instance.SC_output_list[limit:], 'k--', label="SC output")

            if self.check_var6.get():

                self.ax1_twin.plot(self.g_sys_instance.time_list[limit:], self.g_cal_instance.CC_output_list[limit:], 'b--', label="CC output")

            if self.check_var7.get():

                self.ax1_twin.plot(self.g_sys_instance.time_list[limit:], self.g_cal_instance.DPG_output_list[limit:], 'r--', label="DPG output")

            self.ax1.legend()

            self.ax1_twin.legend()

    def animate_RH(self, i):

        if self.calib_check_var.get():

            self.plot_2_range = self.slider_list_value[int(self.scale_2.get())]*60 

            index = int(self.plot_2_range/15.0)

            limit = 25000 - int(self.plot_density*index)

            self.ax2.plot(self.g_sys_instance.time_list[limit:], self.g_sys_instance.RH_list[limit:], color='b', label='pCO2')

            self.ax2_twin.plot(self.g_sys_instance.time_list[limit:], self.g_sys_instance.pH2O_list[limit:], color='r', label='pH2O')

    def animate_calibration_table(self):

        ################## Measured var - temp and output ################## 

        self.TSC.set(str(self.g_sys_instance.Temperatures_SC[-1]))

        self.TCC.set(str(self.g_sys_instance.Temperatures_CC[-1]))

        self.TDPG.set(str(self.g_sys_instance.Temperatures_DPG[-1])) 

        self.SC_output.set(str(round(float(self.g_cal_instance.SC_output_list[-1]),2)))

        self.CC_output.set(str(round(float(self.g_cal_instance.CC_output_list[-1]),2)))

        self.DPG_output.set(str(round(float(self.g_cal_instance.DPG_output_list[-1]),2)))

        self.update()

    def update_calibration_table(self):

        ################## Update power ################## 
        
        self.SC_power.set(self.MODES[int(float(self.g_cal_instance.SC_power))])

        self.SC_power_scale.set(int(float(self.g_cal_instance.SC_power)))

        self.CC_power.set(self.MODES[int(float(self.g_cal_instance.CC_power))])

        self.CC_power_scale.set(int(float(self.g_cal_instance.CC_power)))

        self.DPG_power.set(self.MODES[int(float(self.g_cal_instance.DPG_power))])

        self.DPG_power_scale.set(int(float(self.g_cal_instance.DPG_power)))

        ################## Update PID ################## 

        self.SC_P.set(str(self.g_cal_instance.SC_P))

        self.SC_I.set(str(self.g_cal_instance.SC_I))

        self.SC_D.set(str(self.g_cal_instance.SC_D))

        self.CC_P.set(str(self.g_cal_instance.CC_P))

        self.CC_I.set(str(self.g_cal_instance.CC_I))

        self.CC_D.set(str(self.g_cal_instance.CC_D))

        self.DPG_P.set(str(self.g_cal_instance.DPG_P))

        self.DPG_I.set(str(self.g_cal_instance.DPG_I))

        self.DPG_D.set(str(self.g_cal_instance.DPG_D))

        ################## Update Set Points ################## 

        self.SC_set.set(str(self.g_cal_instance.SC_set))

        self.CC_set.set(str(self.g_cal_instance.CC_set))

        self.DPG_set.set(str(self.g_cal_instance.DPG_set))

        self.update()

    def SC_PID_apply_func(self):

        self.SC_P_entry.config(bg='gray', fg = "white")

        self.SC_I_entry.config(bg='gray', fg = "white")

        self.SC_D_entry.config(bg='gray', fg = "white")

        self.update()

        reply_P = self.cons.send_command_to_PC('s SC_P '+str(self.SC_P.get()))

        reply_I = self.cons.send_command_to_PC('s SC_I '+str(self.SC_I.get()))

        reply_D = self.cons.send_command_to_PC('s SC_D '+str(self.SC_D.get()))

        if reply_P == reply_I == reply_D == 'e 0\n':

            self.SC_P_entry.config(bg='light gray', fg='black')

            self.SC_I_entry.config(bg='light gray', fg='black')

            self.SC_D_entry.config(bg='light gray', fg='black')

            self.update()

    def CC_PID_apply_func(self):

        self.CC_P_entry.config(bg='gray', fg = "white")

        self.CC_I_entry.config(bg='gray', fg = "white")

        self.CC_D_entry.config(bg='gray', fg = "white")

        self.update()

        reply_P = self.cons.send_command_to_PC('s CC_P '+str(self.CC_P.get()))

        reply_I = self.cons.send_command_to_PC('s CC_I '+str(self.CC_I.get()))

        reply_D = self.cons.send_command_to_PC('s CC_D '+str(self.CC_D.get()))

        if reply_P == reply_I == reply_D == 'e 0\n':

            self.CC_P_entry.config(bg='light gray', fg='black')

            self.CC_I_entry.config(bg='light gray', fg='black')

            self.CC_D_entry.config(bg='light gray', fg='black')

            self.update()

    def DPG_PID_apply_func(self):

        self.DPG_P_entry.config(bg='gray', fg = "white")

        self.DPG_I_entry.config(bg='gray', fg = "white")

        self.DPG_D_entry.config(bg='gray', fg = "white")

        self.update()

        reply_P = self.cons.send_command_to_PC('s DPG_P '+str(self.DPG_P.get()))

        reply_I = self.cons.send_command_to_PC('s DPG_I '+str(self.DPG_I.get()))

        reply_D = self.cons.send_command_to_PC('s DPG_D '+str(self.DPG_D.get()))

        if reply_P == reply_I == reply_D == 'e 0\n':

            self.DPG_P_entry.config(bg='light gray', fg='black')

            self.DPG_I_entry.config(bg='light gray', fg='black')

            self.DPG_D_entry.config(bg='light gray', fg='black')

            self.update()


    def pH2O_PID_apply_func(self):

        self.pH2O_P_entry.config(bg='gray', fg = "white")

        self.pH2O_I_entry.config(bg='gray', fg = "white")

        self.pH2O_D_entry.config(bg='gray', fg = "white")

        self.update()

        reply_P = self.cons.send_command_to_PC('s pH2O_P '+str(self.pH2O_P.get()))

        reply_I = self.cons.send_command_to_PC('s pH2O_I '+str(self.pH2O_I.get()))

        reply_D = self.cons.send_command_to_PC('s pH2O_D '+str(self.pH2O_D.get()))

        if reply_P == reply_I == reply_D == 'e 0\n':

            self.pH2O_P_entry.config(bg='light gray', fg='black')

            self.pH2O_I_entry.config(bg='light gray', fg='black')

            self.pH2O_D_entry.config(bg='light gray', fg='black')

            self.update()

    def pH2O_set_apply_func(self):

        if self.MODES.index(self.DPG_power.get()):

            self.TDP_set_entry.config(bg='gray', fg = "white")

            self.RH_set_entry.config(bg='gray', fg = "white")

            self.pH2O_set_entry.config(bg='gray', fg = "white")

            self.update()

            TSC = self.g_sys_instance.Temperatures_SC[-1]

            if len(self.TDP_set_entry.get()) == 0 and len(self.RH_set.get()) == 0 and len(self.pH2O_set.get()) == 0:

                messagebox.showwarning(title='Input Error', message="No entry for TDP or RH or pH2O")

            elif len(self.TDP_set_entry.get()) > 0: #TDP entry

                if len(self.RH_set.get()) == 0 and len(self.pH2O_set.get()) == 0:

                    target_TDP = float(self.TDP_set_entry.get())

                    #print(target_TDP)

                    reply_DPG_set = self.cons.send_command_to_PC('s DPG_set '+  str(target_TDP))

                    if reply_DPG_set == 'e 0\n':

                        print('Command success')

                        self.TDP_set_entry.config(bg='light gray', fg='black')

                        self.pH2O_set_entry.config(bg='light gray', fg='black')

                        self.RH_set_entry.config(bg='light gray', fg='black')

                        self.update()

                else:

                    messagebox.showwarning(title='Input Error', message="Choose one input")

            elif len(self.RH_set.get()) > 0: #RH entry

                if len(self.TDP_set_entry.get()) == 0 and len(self.pH2O_set.get()) == 0: 

                    RH_input = float(self.RH_set.get())

                    if RH_input >=10 and RH_input <=90: #RH limits

                        target_pressure = (RH_input/100.0)*self.ph2oSat(TSC)

                        Cell_pressure_output = self.cons.send_command_to_PC('g CellP')

                        print('Cell_pressure_output', Cell_pressure_output)

                        Cell_pressure_string_list = Cell_pressure_output.split('\n')  #Convert to Pa

                        Cell_pressure_string = Cell_pressure_string_list[0].split('---')[0]

                        Cell_pressure = float(Cell_pressure_string)*1000

                        #self.pH2O_set.set((target_pressure/Cell_pressure)*1000,2)

                        self.pH2O_set_entry.insert(0, str(round((target_pressure/Cell_pressure)*1000,2)))

                        target_TDP = opt.brentq(lambda T: self.ph2oSat_solve(T, target_pressure), -50, 50)

                        reply_DPG_set = self.cons.send_command_to_PC('s DPG_set '+  str(target_TDP))

                        self.TDP_set_entry.insert(0, str(round(target_TDP,2)))

                        if reply_DPG_set == 'e 0\n':

                            print('Command success')

                            self.pH2O_set_entry.config(bg='light gray', fg='black')

                            self.RH_set_entry.config(bg='light gray', fg='black')

                            self.TDP_set_entry.config(bg='light gray', fg='black')

                            self.update()

                        reply_DPG_set = self.cons.send_command_to_PC('s DPG_set '+  str(target_TDP))
                            
                        #print('reply_DPG_set', reply_DPG_set)

                    elif RH_input >=90:

                        messagebox.showwarning(title='RH offlimits', message="Condensation Warning")

                    else:

                        messagebox.showwarning(title='RH offlimits', message="Low RH Warning")

                else:

                     messagebox.showwarning(title='Input Error', message="Choose one input")

            elif len(self.pH2O_set.get()) > 0: # pH2O entry

                if len(self.TDP_set_entry.get()) == 0 and len(self.RH_set.get()) == 0:

                    Cell_pressure_output = self.cons.send_command_to_PC('g CellP')

                    #print(Cell_pressure_output)

                    Cell_pressure_string_list = Cell_pressure_output.split('\n')  #Convert to Pa

                    Cell_pressure_string = Cell_pressure_string_list[0].split('---')[0]

                    Cell_pressure = float(Cell_pressure_string)*1000

                    target_pressure = (float(self.pH2O_set.get())/1000.0)*Cell_pressure

                    RH_input = (target_pressure/self.ph2oSat(TSC))*100

                    if RH_input >=10 and RH_input <=90: #RH limits

                        target_TDP = opt.brentq(lambda T: self.ph2oSat_solve(T, target_pressure), -50, 50)

                        self.RH_set_entry.insert(0, str(round(RH_input,2)))

                        self.TDP_set_entry.insert(0, str(round(target_TDP,2)))
                    
                        reply_DPG_set = self.cons.send_command_to_PC('s DPG_set '+  str(target_TDP))

                        if reply_DPG_set == 'e 0\n':

                            print('Command success')

                            self.pH2O_set_entry.config(bg='light gray', fg='black')

                            self.RH_set_entry.config(bg='light gray', fg='black')

                            self.TDP_set_entry.config(bg='light gray', fg='black')

                            self.update()

                    elif RH_input >=90:

                        messagebox.showwarning(title='pH2O offlimits', message="Condensation Warning")

                    else:

                        messagebox.showwarning(title='pH2O offlimits', message="Low pH2O warning")

                else:

                    messagebox.showwarning(title='Input Error', message="Choose one entry for RH or pH2O")

            else:

                messagebox.showwarning(title='Input Error', message="Choose one input")

        else:

            messagebox.showwarning(title='Power Error', message="Switch controller on")

    def SC_set_apply_func(self):

        if self.MODES.index(self.SC_power.get()):

            #self.validate(self.SC_set.get(), input_type, input_range, var_name)

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


    def CC_set_apply_func(self):

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


    def DPG_set_apply_func(self):

        if self.MODES.index(self.DPG_power.get()):

            #self.validate(self.DPG_set.get(), input_type, input_range, var_name)

            self.DPG_set_entry.config(bg='gray', fg = "white")

            self.update()

            reply = self.cons.send_command_to_PC('s DPG_set '+str(self.DPG_set.get()))

            if reply == 'e 0\n':

                self.DPG_set_entry.config(bg='light gray', fg='black')

                self.update()

            else:

                messagebox.showwarning(title='Command Error', message="Check entry")

        else:

            messagebox.showwarning(title='Power Error', message="Switch controller on")


    def ph2oSat_solve(self, T, P):

        return 610.78 * exp((T * 17.2684) / (T + 238.3)) - P

    def ph2oSat(self, T):

        return 610.78 * exp((T * 17.2684) / (T + 238.3))