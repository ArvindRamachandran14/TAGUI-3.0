from tkinter import Frame, LabelFrame, Label, Spinbox, Button, Text, StringVar, Radiobutton, OptionMenu, Entry, Scale, HORIZONTAL, Checkbutton, IntVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from datetime import datetime
import time

class Calib(Frame) :

    def __init__(self, parent, g_sys_instance, g_cal_instance, cons, *args, **kwargs) :
        Frame.__init__(self, *args, **kwargs)
        self.g_sys_instance = g_sys_instance
        self.g_cal_instance = g_cal_instance
        self.cons = cons
        self.plot_density = 7
        self.slider_list = [0,1,2,3,4]
        self.slider_list_value = [0.5,1,15,30,60]
        #self.parent = parent

        self.calib_check_var = IntVar()
        Checkbutton(self, text="Calibration mode", variable=self.calib_check_var, command=self.set_bcalibration).grid(row=0, column=0, sticky='W')

        self.build_SC_table()
        self.build_CC_table()
        self.build_DPG_table()
        self.buildContent()

    def buildContent(self) :

        self.output = StringVar()

        self.scale_textvariable = StringVar()

        '''
        choose_controller_list = ["SC", "CC", "DPG"]

        self.controller_label = Label(self, text = 'Choose Controller:')
        
        self.controller_label.grid(row = 0, column = 0, padx = 2, pady = 2, sticky='e')

        self.choose_controller_variable = StringVar()

        self.choose_controller_widget = OptionMenu(self, self.choose_controller_variable, *choose_controller_list, command=self.update_settings)

        self.choose_controller_widget.grid(row = 0, column = 1, padx = 2, pady = 2, sticky='w')

        self.choose_controller_variable.set("SC")

        self.plot_label_variable = StringVar()

        self.plot_label = Label(self, textvariable=self.plot_label_variable)

        #self.plot_label_variable.set("Sample Chamber Temperature")

        #self.plot_label.grid(row=0, column=2, padx = 2, pady = 2, sticky='N')
        '''

        self.check_var1 = IntVar()
        Checkbutton(self, text="TSC", variable=self.check_var1).grid(row=0, column=10, sticky='NW')
        self.check_var2 = IntVar()
        Checkbutton(self, text="TCC", variable=self.check_var2).grid(row=0, column=10, sticky='N')
        self.check_var3 = IntVar()
        Checkbutton(self, text="TDPG", variable=self.check_var3).grid(row=0, column=10, sticky='NE')

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
      
        self.cnvs1 = FigureCanvasTkAgg(self.fig1, self)
        self.cnvs1.get_tk_widget().grid(row=1, column=9, padx = 2, pady = 0, columnspan=3, sticky='NW')

        self.outputtextbox_variable = StringVar()

        self.scale = Scale(self, from_=min(self.slider_list), to=max(self.slider_list), command=self.scale_value_show, showvalue=0, orient=HORIZONTAL)#, command=set_plot_range(1))
        self.scale.grid(row=2, column=10, rowspan=1)

        self.scale_textvariable.set('Plot range(m): '+ str(self.slider_list_value[0]))

        self.scale1_label = Label(self, textvariable=self.scale_textvariable)

        self.scale1_label.grid(row=3, column=10, rowspan=1)

        self.outputtextbox = Label(self, textvariable=self.outputtextbox_variable)

        self.outputtextbox.grid(row=4, column=10)

    def build_SC_table(self):

        self.SC_settings_variable = StringVar()

        self.SC_settings_label = Label(self, textvariable=self.SC_settings_variable)

        self.SC_settings = LabelFrame(self, labelwidget=self.SC_settings_label)

        self.SC_settings_variable.set('SC settings')

        self.SC_settings.grid(row=1,column=0, padx=2, pady=2, rowspan=12, sticky='N')

        self.SC_powersettings = LabelFrame(self.SC_settings, text = 'Power')
        
        self.SC_powersettings.grid(row=2,column=0, padx=2, pady=2, rowspan=2, columnspan=3, sticky='e')

        MODES = [("ON", "1"),("OFF", "0")]

        Label(self.SC_powersettings, text = '', width=7).grid(row=3, column=1)

        self.SC_power_label = Label(self.SC_powersettings, text = 'Power:', width = 5)

        self.SC_power_label.grid(row = 3, column = 0, padx = 2, pady = 2, sticky='e')

        self.SC_v1 = StringVar()
        self.SC_v1.set("0") # initialize

        for i in range(2):
            self.SC_rb1 = Radiobutton(self.SC_powersettings, text=MODES[i][0], variable=self.SC_v1, value=MODES[i][1])
            self.SC_rb1.grid(row=3, column=i+1, padx = 2, pady = 2, sticky='w')
 
        self.box_values_power = Button(self.SC_powersettings, text="Apply", command=self.send_power_settings)#, command=self.send_command)
        self.box_values_power.grid(row = 4, column = 2, padx = 2, pady = 2, sticky='e')

        self.SC_PIDSettings = LabelFrame(self.SC_settings, text = 'PID parameters')
        
        self.SC_PIDSettings.grid(row=5,column=0, padx=2, pady=2, rowspan=4, columnspan=3, sticky='e')

        self.SC_P = StringVar()

        self.SC_P_label = Label(self.SC_PIDSettings, text = "P gain:")

        self.SC_P_label.grid(row = 6, column = 0, padx = 2, pady = 2, sticky='e')

        self.SC_P_entry = Entry(self.SC_PIDSettings, width=5, textvariable=self.SC_P) 

        self.SC_P_entry.grid(row = 6, column = 1, padx = 2, pady = 2, sticky='e')

        self.SC_I = StringVar()

        self.SC_I_label = Label(self.SC_PIDSettings, text = "I gain:")

        self.SC_I_label.grid(row = 7, column = 0, padx = 2, pady = 2, sticky='e')

        self.SC_I_entry = Entry(self.SC_PIDSettings, width=5, textvariable=self.SC_I) 

        self.SC_I_entry.grid(row = 7, column = 1, padx = 2, pady = 2, sticky='e')

        self.SC_D = StringVar()

        self.SC_D_label = Label(self.SC_PIDSettings, text = "D gain:")

        self.SC_D_label.grid(row = 8, column = 0, padx = 2, pady = 2, sticky='e')

        self.SC_D_entry = Entry(self.SC_PIDSettings, width=5, textvariable=self.SC_D) 

        self.SC_D_entry.grid(row = 8, column = 1, padx = 2, pady = 2, sticky='e')

        self.SC_box_values_PID = Button(self.SC_PIDSettings, text="Apply", command=self.send_PID_settings)#, command=self.send_command)
        self.SC_box_values_PID.grid(row = 9, column = 2, padx = 2, pady = 2, sticky='e')

        self.SC_grpSetPoint = LabelFrame(self.SC_settings, text = 'Set Point')

        self.SC_grpSetPoint.grid(row=10, column=0, rowspan=2, padx=2, pady=2, columnspan=3, sticky='e')

        Label(self.SC_grpSetPoint, text = '', width=5).grid(row=11, column=1)

        self.setpoint_label = Label(self.SC_grpSetPoint, text="Set Point:")

        self.setpoint_label.grid(row=11,column=0, padx=2, pady=2, sticky='w')

        self.setpoint_variable = StringVar()

        self.setpoint_entry = Entry(self.SC_grpSetPoint, width=5, textvariable=self.setpoint_variable) 

        self.setpoint_entry.grid(row=11,column=1, padx=2, pady=2, sticky='e')

        self.box_values_setpoint = Button(self.SC_grpSetPoint, text="Apply", command=self.send_set_point)
        self.box_values_setpoint.grid(row = 12, column = 2, padx = 2, pady = 2, sticky='e')
 
        #Label(self.grpSetPoint, text="Arvind").grid(row=12, column=4)

    def build_CC_table(self):

        self.CC_settings_variable = StringVar()

        self.CC_settings_label = Label(self, textvariable=self.CC_settings_variable)

        self.CC_settings = LabelFrame(self, labelwidget=self.CC_settings_label)

        self.CC_settings_variable.set('CC settings')

        self.CC_settings.grid(row=1,column=3, padx=2, pady=2, rowspan=12, sticky='NE')

        self.CC_powersettings = LabelFrame(self.CC_settings, text = 'Power')
        
        self.CC_powersettings.grid(row=2,column=3, padx=2, pady=2, rowspan=2, columnspan=3, sticky='e')

        MODES = [("ON", "1"),("OFF", "0")]

        Label(self.CC_powersettings, text = '', width=7).grid(row=3, column=4)

        self.CC_power_label = Label(self.CC_powersettings, text = 'Power:', width = 5)

        self.CC_power_label.grid(row = 3, column = 3, padx = 2, pady = 2, sticky='e')

        self.CC_v1 = StringVar()
        self.CC_v1.set("0") # initialize

        for i in range(2):
            self.CC_rb1 = Radiobutton(self.CC_powersettings, text=MODES[i][0], variable=self.CC_v1, value=MODES[i][1])
            self.CC_rb1.grid(row=3, column=i+3, padx = 2, pady = 2, sticky='w')
 
        self.box_values_power = Button(self.CC_powersettings, text="Apply", command=self.send_power_settings)#, command=self.send_command)
        self.box_values_power.grid(row = 4, column = 5, padx = 2, pady = 2, sticky='e')

        self.CC_PIDSettings = LabelFrame(self.CC_settings, text = 'PID parameters')
        
        self.CC_PIDSettings.grid(row=5,column=3, padx=2, pady=2, rowspan=4, columnspan=3, sticky='e')

        self.CC_P = StringVar()

        self.CC_P_label = Label(self.CC_PIDSettings, text = "P gain:")

        self.CC_P_label.grid(row = 6, column = 3, padx = 2, pady = 2, sticky='e')

        self.CC_P_entry = Entry(self.CC_PIDSettings, width=5, textvariable=self.CC_P) 

        self.CC_P_entry.grid(row = 6, column = 4, padx = 2, pady = 2, sticky='e')

        self.CC_I = StringVar()

        self.CC_I_label = Label(self.CC_PIDSettings, text = "I gain:")

        self.CC_I_label.grid(row = 7, column = 3, padx = 2, pady = 2, sticky='e')

        self.CC_I_entry = Entry(self.CC_PIDSettings, width=5, textvariable=self.CC_I) 

        self.CC_I_entry.grid(row = 7, column = 4, padx = 2, pady = 2, sticky='e')

        self.CC_D = StringVar()

        self.CC_D_label = Label(self.CC_PIDSettings, text = "D gain:")

        self.CC_D_label.grid(row = 8, column = 3, padx = 2, pady = 2, sticky='e')

        self.CC_D_entry = Entry(self.CC_PIDSettings, width=5, textvariable=self.CC_D) 

        self.CC_D_entry.grid(row = 8, column = 4, padx = 2, pady = 2, sticky='e')

        self.CC_box_values_PID = Button(self.CC_PIDSettings, text="Apply", command=self.send_PID_settings)#, command=self.send_command)
        self.CC_box_values_PID.grid(row = 9, column = 5, padx = 2, pady = 2, sticky='e')

        self.CC_grpSetPoint = LabelFrame(self.CC_settings, text = 'Set Point')

        self.CC_grpSetPoint.grid(row=10, column=3, rowspan=2, padx=2, pady=2, columnspan=3, sticky='e')

        Label(self.CC_grpSetPoint, text = '', width=5).grid(row=11, column=4)

        self.CC_setpoint_label = Label(self.CC_grpSetPoint, text="Set Point:")

        self.CC_setpoint_label.grid(row=11,column=3, padx=2, pady=2, sticky='w')

        self.CC_etpoint_variable = StringVar()

        self.CC_setpoint_entry = Entry(self.CC_grpSetPoint, width=5, textvariable=self.setpoint_variable) 

        self.CC_setpoint_entry.grid(row=11,column=4, padx=2, pady=2, sticky='e')

        self.CC_box_values_setpoint = Button(self.CC_grpSetPoint, text="Apply", command=self.send_set_point)
        self.CC_box_values_setpoint.grid(row = 12, column = 5, padx = 2, pady = 2, sticky='e')

    def build_DPG_table(self):

        self.DPG_settings_variable = StringVar()

        self.DPG_settings_label = Label(self, textvariable=self.DPG_settings_variable)

        self.DPG_settings = LabelFrame(self, labelwidget=self.DPG_settings_label)

        self.DPG_settings_variable.set('DPG settings')

        self.DPG_settings.grid(row=1,column=6, padx=2, pady=2, rowspan=12, sticky='N')

        self.DPG_powersettings = LabelFrame(self.DPG_settings, text = 'Power')
        
        self.DPG_powersettings.grid(row=2,column=6, padx=2, pady=2, rowspan=2, columnspan=3, sticky='e')

        MODES = [("ON", "1"),("OFF", "0")]

        Label(self.DPG_powersettings, text = '', width=7).grid(row=3, column=7)

        self.DPG_power_label = Label(self.DPG_powersettings, text = 'Power:', width = 5)

        self.DPG_power_label.grid(row = 3, column = 6, padx = 2, pady = 2, sticky='e')

        self.DPG_v1 = StringVar()
        self.DPG_v1.set("0") # initialize

        for i in range(2):
            self.DPG_rb1 = Radiobutton(self.DPG_powersettings, text=MODES[i][0], variable=self.DPG_v1, value=MODES[i][1])
            self.DPG_rb1.grid(row=3, column=i+6, padx = 2, pady = 2, sticky='w')
 
        self.box_values_power = Button(self.DPG_powersettings, text="Apply", command=self.send_power_settings)#, command=self.send_command)
        self.box_values_power.grid(row = 4, column = 8, padx = 2, pady = 2, sticky='e')

        self.DPG_PIDSettings = LabelFrame(self.DPG_settings, text = 'PID parameters')
        
        self.DPG_PIDSettings.grid(row=5,column=6, padx=2, pady=2, rowspan=4, columnspan=3, sticky='e')

        self.DPG_P = StringVar()

        self.DPG_P_label = Label(self.DPG_PIDSettings, text = "P gain:")

        self.DPG_P_label.grid(row = 6, column = 6, padx = 2, pady = 2, sticky='e')

        self.DPG_P_entry = Entry(self.DPG_PIDSettings, width=5, textvariable=self.DPG_P) 

        self.DPG_P_entry.grid(row = 6, column = 7, padx = 2, pady = 2, sticky='e')

        self.DPG_I = StringVar()

        self.DPG_I_label = Label(self.DPG_PIDSettings, text = "I gain:")

        self.DPG_I_label.grid(row = 7, column = 6, padx = 2, pady = 2, sticky='e')

        self.DPG_I_entry = Entry(self.DPG_PIDSettings, width=5, textvariable=self.DPG_I) 

        self.DPG_I_entry.grid(row = 7, column = 7, padx = 2, pady = 2, sticky='e')

        self.DPG_D = StringVar()

        self.DPG_D_label = Label(self.DPG_PIDSettings, text = "D gain:")

        self.DPG_D_label.grid(row = 8, column = 6, padx = 2, pady = 2, sticky='e')

        self.DPG_D_entry = Entry(self.DPG_PIDSettings, width=5, textvariable=self.DPG_D) 

        self.DPG_D_entry.grid(row = 8, column = 7, padx = 2, pady = 2, sticky='e')

        self.DPG_box_values_PID = Button(self.DPG_PIDSettings, text="Apply", command=self.send_PID_settings)#, command=self.send_command)
        self.DPG_box_values_PID.grid(row = 9, column = 8, padx = 2, pady = 2, sticky='e')

        self.DPG_grpSetPoint = LabelFrame(self.DPG_settings, text = 'Set Point')

        self.DPG_grpSetPoint.grid(row=10, column=6, rowspan=2, padx=2, pady=2, columnspan=3, sticky='e')

        Label(self.DPG_grpSetPoint, text = '', width=5).grid(row=11, column=7)

        self.DPG_setpoint_label = Label(self.DPG_grpSetPoint, text="Set Point:")

        self.DPG_setpoint_label.grid(row=11,column=6, padx=2, pady=2, sticky='w')

        self.DPG_setpoint_variable = StringVar()

        self.DPG_setpoint_entry = Entry(self.DPG_grpSetPoint, width=5, textvariable=self.setpoint_variable) 

        self.DPG_setpoint_entry.grid(row=11,column=7, padx=2, pady=2, sticky='e')

        self.DPG_box_values_setpoint = Button(self.DPG_grpSetPoint, text="Apply", command=self.send_set_point)
        self.DPG_box_values_setpoint.grid(row = 12, column = 8, padx = 2, pady = 2, sticky='e')


    def set_bcalibration(self):

        if self.calib_check_var.get():

            self.g_cal_instance.bcalibration = True

        else:

            self.g_cal_instance.bcalibration = False


    def check_box_settings(self):

        print('self.check_var1',  self.check_var1.get())

    '''    
    def update_settings(self, list):

        #print(time.time())

        self.settings_variable.set(self.choose_controller_variable.get()+' settings')

        temp_power = self.cons.send_command_to_PC('g '+self.choose_controller_variable.get()+'_power')

        #print(temp_power)
     
        temp_power = int(float(temp_power.split('---')[0]))

        if temp_power == 1:

            self.v1.set("1")

        elif temp_power == 0:

            self.v1.set("0")

        #print(datetime.now())

        temp_P = self.cons.send_command_to_PC('g '+self.choose_controller_variable.get()+'_P').split('---')[0]

        self.P.set(temp_P)

        #print(datetime.now())

        temp_I = self.cons.send_command_to_PC('g '+self.choose_controller_variable.get()+'_I').split('---')[0]

        self.I.set(temp_I)

        #print(datetime.now())

        temp_D = self.cons.send_command_to_PC('g '+self.choose_controller_variable.get()+'_D').split('---')[0]

        self.D.set(temp_D)

        #print(datetime.now())

        temp_set_point = self.cons.send_command_to_PC('g '+self.choose_controller_variable.get()+'_set').split('---')[0]

        self.setpoint_variable.set(temp_set_point)

        #print(datetime.now())
    '''

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

        if self.check_var1.get():

            self.ax1.plot(self.g_sys_instance.time_list[(25000-self.plot_density*index):], self.g_sys_instance.Temperatures_SC[(25000-self.plot_density*index):], 'k', label="TSC")

            outputstring=" TSC = "+str(self.g_sys_instance.Temperatures_SC[-1])+"   "

            self.outputtextbox_variable.set(outputstring)

            self.ax1.legend()

            #self.plot_label_variable.set("  Sample Chamber Temperature")

        if self.check_var2.get():

            self.ax1.plot(self.g_sys_instance.time_list[(25000-self.plot_density*index):], self.g_sys_instance.Temperatures_CC[(25000-self.plot_density*index):], 'b', label="TCC")

            outputstring+="TCC = "+str(self.g_sys_instance.Temperatures_CC[-1])+"   "

            self.outputtextbox_variable.set(outputstring) 

            self.ax1.legend()

            #self.plot_label_variable.set("  Conditioning Chamber Temperature")

        if self.check_var3.get():
            
            self.ax1.plot(self.g_sys_instance.time_list[(25000-self.plot_density*index):], self.g_sys_instance.Temperatures_DPG[(25000-self.plot_density*index):], 'r', label="TDPG")

            outputstring+="TDPG = "+str(self.g_sys_instance.Temperatures_DPG[-1])

            self.outputtextbox_variable.set(outputstring)

            self.ax1.legend()

            #self.plot_label_variable.set("  Dew Point Generator Temperature")

        outputstring=""


        #self.ax1.plot(self.g_sys_instance.time_list[(10000-self.plot1_range*index):], self.g_sys_instance.Temperatures_DPG[(10000-self.plot1_range*index):], 'r', label="TDPG")

        #self.ax1.legend()

        #self.outputtextbox1_variable.set("TCC = "+str(self.g_sys_instance.Temperatures_CC[-1])+" TSC = "+str(self.g_sys_instance.Temperatures_SC[-1])+" TDPG = "+str(self.g_sys_instance.Temperatures_DPG[-1]))

    def scale_value_show(self, value):
        
        self.scale_textvariable.set('Plot range(m): '+ str(self.slider_list_value[int(value)]))

    def show_plot(self, list):

        if self.choose_controller_variable.get() == "SC":

            self.cnvs1.get_tk_widget().grid(row=1, column=2, padx = 2, pady = 2, sticky='n')

        if self.choose_controller_variable.get() == "CC":

            self.cnvs2.get_tk_widget().grid(row=1, column=2, padx = 2, pady = 2, sticky='n')

    def send_power_settings(self):

        command_power = 's '+self.choose_controller_variable.get()+ '_power '+self.v1.get()

        reply_power = self.cons.send_command_to_PC(command_power)

        time.sleep(2)

    def send_PID_settings(self):

        command_P = 's '+self.choose_controller_variable.get()+ '_P '+self.P_entry.get()

        reply_P = self.cons.send_command_to_PC(command_P)

        time.sleep(2)

        command_I = 's '+self.choose_controller_variable.get()+ '_I '+self.I_entry.get()

        reply_I = self.cons.send_command_to_PC(command_I)

        time.sleep(2)

        command_D = 's '+self.choose_controller_variable.get()+ '_D '+self.D_entry.get()

        reply_D = self.cons.send_command_to_PC(command_D)

        time.sleep(2)

    def send_set_point(self):

        command_set = 's '+self.choose_controller_variable.get()+'_set '+self.setpoint_entry.get()

        reply_set = self.cons.send_command_to_PC(command_set)

