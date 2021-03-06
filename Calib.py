from tkinter import Frame, LabelFrame, Label, Spinbox, Button, Text, StringVar, Radiobutton, OptionMenu, Entry, Scale, HORIZONTAL
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import time

class Calib(Frame) :

    def __init__(self, parent, g_sys_instance, cons, *args, **kwargs) :
        Frame.__init__(self, *args, **kwargs)
        self.g_sys_instance = g_sys_instance
        self.cons = cons
        self.plot_density = 7
        self.slider_list = [0,1,2,3,4]
        self.slider_list_value = [0.5,1,15,30,60]
        #self.parent = parent
        self.buildContent()

    def buildContent(self) :

        self.output = StringVar()

        self.scale_textvariable = StringVar()

        choose_controller_list = ["SC", "CC", "DPG"]

        self.controller_label = Label(self, text = 'Choose Controller:')
        
        self.controller_label.grid(row = 0, column = 0, padx = 2, pady = 2, sticky='e')

        self.choose_controller_variable = StringVar()

        self.choose_controller_widget = OptionMenu(self, self.choose_controller_variable, *choose_controller_list)#, command=self.show_plot)

        self.choose_controller_widget.grid(row = 0, column = 1, padx = 2, pady = 2, sticky='w')

        self.choose_controller_variable.set("SC")

        self.plot_label_variable = StringVar()

        self.plot_label = Label(self, textvariable=self.plot_label_variable)

        self.plot_label_variable.set("Sample Chamber Temperature")

        self.plot_label.grid(row=0, column=2, padx = 2, pady = 2, sticky='n')


        self.Settings = LabelFrame(self, text= 'Settings')

        self.Settings.grid(row=1,column=1, padx=2, pady=2, rowspan=12, sticky='N')

        self.scale = Scale(self, from_=min(self.slider_list), to=max(self.slider_list), command=self.scale_value_show, showvalue=0, orient=HORIZONTAL)#, command=set_plot_range(1))
        self.scale.grid(row=1, column=2, rowspan=1)

        self.scale_textvariable.set('Plot range(m): '+ str(self.slider_list_value[0]))

        self.scale1_label = Label(self, textvariable=self.scale_textvariable)

        self.scale1_label.grid(row=2, column=2, rowspan=1)

        self.fig1 = Figure(figsize=(3.8, 3.8))
        self.ax1 = self.fig1.add_subplot(111)
        self.ax1.set_xlabel('Time (sec)')
        self.ax1.set_ylabel('Temperature ($^\circ$C)')
        self.ax1.set_autoscalex_on(True)
        self.ax1.set_ybound(10, 40)
        self.ax1.set_autoscaley_on(True)
        self.ax1.grid(True, 'major', 'both')

        self.fig1.tight_layout()
      
        self.cnvs1 = FigureCanvasTkAgg(self.fig1, self)
        self.cnvs1.get_tk_widget().grid(row=3, column=2, padx = 2, pady = 2, sticky='n')

        self.outputtextbox_variable = StringVar()

        self.PowerSettings = LabelFrame(self.Settings, text = 'Power')
        
        self.PowerSettings.grid(row=2,column=1, padx=2, pady=2, rowspan=2, columnspan=4, sticky='e')

        self.outputtextbox = Label(self, textvariable=self.outputtextbox_variable)

        self.outputtextbox.grid(row=4, column=2)

        MODES = [("ON", "1"),("OFF", "0")]

        Label(self.PowerSettings, text = '', width=7).grid(row=3, column=1)

        self.power_label = Label(self.PowerSettings, text = 'Power:', width = 5)

        self.power_label.grid(row = 3, column = 2, padx = 2, pady = 2, sticky='e')

        self.v1 = StringVar()
        self.v1.set("0") # initialize

        for i in range(2):
            self.rb1 = Radiobutton(self.PowerSettings, text=MODES[i][0], variable=self.v1, value=MODES[i][1])
            self.rb1.grid(row=3, column=i+3, padx = 2, pady = 2, sticky='w')
 
        self.box_values_power = Button(self.PowerSettings, text="Apply", command=self.send_power_settings)#, command=self.send_command)
        self.box_values_power.grid(row = 4, column = 4, padx = 2, pady = 2, sticky='e')

        self.PIDSettings = LabelFrame(self.Settings, text = 'PID paramters')
        
        self.PIDSettings.grid(row=5,column=1, padx=2, pady=2, rowspan=4, columnspan=4, sticky='e')

        self.P = StringVar()

        self.P_label = Label(self.PIDSettings, text = "Proportional gain:")

        self.P_label.grid(row = 6, column = 1, padx = 2, pady = 2, sticky='e')


        self.P_entry = Entry(self.PIDSettings, width=5, textvariable=self.P) 

        self.P_entry.grid(row = 6, column = 2, padx = 2, pady = 2, sticky='e')


        self.I = StringVar()

        self.I_label = Label(self.PIDSettings, text = "Integral gain:")

        self.I_label.grid(row = 7, column = 1, padx = 2, pady = 2, sticky='e')


        self.I_entry = Entry(self.PIDSettings, width=5, textvariable=self.I) 

        self.I_entry.grid(row = 7, column = 2, padx = 2, pady = 2, sticky='e')


        self.D = StringVar()

        self.D_label = Label(self.PIDSettings, text = "Derivative gain:")

        self.D_label.grid(row = 8, column = 1, padx = 2, pady = 2, sticky='e')


        self.D_entry = Entry(self.PIDSettings, width=5, textvariable=self.D) 

        self.D_entry.grid(row = 8, column = 2, padx = 2, pady = 2, sticky='e')

        self.box_values_PID = Button(self.PIDSettings, text="Apply", command=self.send_PID_settings)#, command=self.send_command)
        self.box_values_PID.grid(row = 9, column = 3, padx = 2, pady = 2, sticky='e')


        self.grpSetPoint = LabelFrame(self.Settings, text = 'Set Point')


        self.grpSetPoint.grid(row=10, column=1, rowspan=2, padx=2, pady=2, columnspan=4, sticky='e')

        Label(self.grpSetPoint, text = '', width=5).grid(row=11, column=1)

        self.setpoint_label = Label(self.grpSetPoint, text="Set Point:")

        self.setpoint_label.grid(row=11,column=2, padx=2, pady=2, sticky='w')

        self.setpoint_variable = StringVar()

        self.setpoint_entry = Entry(self.grpSetPoint, width=5, textvariable=self.setpoint_variable) 

        self.setpoint_entry.grid(row=11,column=3, padx=2, pady=2, sticky='e')

        self.box_values_setpoint = Button(self.grpSetPoint, text="Apply", command=self.send_set_point)
        self.box_values_setpoint.grid(row = 12, column = 4, padx = 2, pady = 2, sticky='e')
 
        #Label(self.grpSetPoint, text="Arvind").grid(row=12, column=4)


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

        if self.choose_controller_variable.get() == "SC":

            self.ax1.plot(self.g_sys_instance.time_list[(25000-self.plot_density*index):], self.g_sys_instance.Temperatures_SC[(25000-self.plot_density*index):], 'k', label="TSC")

            self.outputtextbox_variable.set(" TSC = "+str(self.g_sys_instance.Temperatures_SC[-1]))

            self.plot_label_variable.set("  Sample Chamber Temperature")

        elif self.choose_controller_variable.get() == "CC":

            self.ax1.plot(self.g_sys_instance.time_list[(25000-self.plot_density*index):], self.g_sys_instance.Temperatures_CC[(25000-self.plot_density*index):], 'b', label="TSC")

            self.outputtextbox_variable.set("TCC = "+str(self.g_sys_instance.Temperatures_CC[-1])) 

            self.plot_label_variable.set("  Conditioning Chamber Temperature")

        elif self.choose_controller_variable.get() == "DPG":
            
            self.ax1.plot(self.g_sys_instance.time_list[(25000-self.plot_density*index):], self.g_sys_instance.Temperatures_DPG[(25000-self.plot_density*index):], 'r', label="TSC")

            self.outputtextbox_variable.set("TDPG = "+str(self.g_sys_instance.Temperatures_DPG[-1]))

            self.plot_label_variable.set("  Dew Point Generator Temperature")


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



