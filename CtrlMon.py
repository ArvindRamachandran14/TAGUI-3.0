# CtrlMon.py
# Class to define content of the Monitor tab.
#
# Change history:
#   20191115:KDT - Original issue

import tkinter as tk 
from tkinter import ttk, Frame, Canvas, LabelFrame, Label, Spinbox, OptionMenu, StringVar, Button, Scale, HORIZONTAL, VERTICAL, Text, Entry
import matplotlib
import numpy as np
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt
import global_sys_var as g_sys
from datetime import datetime
import Data_coord
import math

class CtrlMon(Frame) :
    def __init__(self, name, g_sys_instance, consumer_object, mainform_object, *args, **kwargs) :
       
        Frame.__init__(self, *args, **kwargs)
        self.name = name
        self.g_sys_instance = g_sys_instance
        self.consumer_object = consumer_object
        self.mainform_object = mainform_object
        self.log_btn_text = StringVar()
        self.exp_btn_text = StringVar()
        self.log_btn_text.set('Record data')
        self.exp_btn_text.set('Start experiment')
        self.plot1_density = 7 #7 data points leads to 15 second data
        self.plot2_density = 7 
        self.plot3_density = 7 
        self.log_frequency_list = [2, 4, 10, 60]
        self.slider_list = [0,1,2,3,4,5]
        self.slider_list_value = [1,15,30,60,120,7200]
        #self.slider_list_log = (np.log(self.slider_list)*100).tolist()
        self.buildContent()

    def buildContent(self) :

        self.label = Label(self, text ="")

        self.label.grid(row=0, column=0, rowspan=2)
        self.log_frequency_scale = Scale(self, from_=min(self.log_frequency_list), to=max(self.log_frequency_list), command=self.log_frequency_scale_value_check, orient=HORIZONTAL, label='log rate (s)')#, command=set_plot_range(1))
        self.log_frequency_scale.grid(row=2, column=0, columnspan=2)

        self.button2 = ttk.Button(self, textvariable=self.log_btn_text, command=self.log_data)
        self.button2.grid(row=2, column=1, columnspan=2)

        self.label = Label(self, text ="")

        self.label.grid(row=3, column=0, rowspan=2)

        self.label1 = Label(self, text = 'Temperatures')
        self.label1.grid(row = 5, column = 0, padx = 2, pady = 2)
  
        self.label2 = Label(self, text = 'Partial Pressures')
        self.label2.grid(row = 5, column = 1, padx = 2, pady = 2)
  
        self.label3 = Label(self, text = 'Sample Weight')
        self.label3.grid(row = 5, column = 2, padx = 3, pady = 3)

        self.toolbarframe1 = Frame(self)

        self.toolbarframe2 = Frame(self)

        self.toolbarframe3 = Frame(self)

        self.scale1_textvariable = StringVar()

        self.scale2_textvariable = StringVar()

        self.scale3_textvariable = StringVar()

        self.scale1_textvariable.set('Plot range(m): '+ str(self.slider_list_value[0]))

        self.scale2_textvariable.set('Plot range(m): '+ str(self.slider_list_value[0]))

        self.scale3_textvariable.set('Plot range(m): '+ str(self.slider_list_value[0]))

        self.scale1 = Scale(self, from_=min(self.slider_list), to=max(self.slider_list), command=self.scale_value_show1, showvalue=0, orient=HORIZONTAL)#, command=set_plot_range(1))
        self.scale1.grid(row=6, column=0, rowspan=1)

        self.scale1_label = Label(self, textvariable=self.scale1_textvariable)

        self.scale1_label.grid(row=7, column=0, rowspan=1)

        self.scale2 = Scale(self, from_=min(self.slider_list), to=max(self.slider_list), command=self.scale_value_show2, showvalue=0, orient=HORIZONTAL)#, command=set_plot_range(2))
        self.scale2.grid(row=6, column=1, rowspan=1)

        self.scale2_label = Label(self, textvariable=self.scale2_textvariable)
        self.scale2_label.grid(row=7, column=1, rowspan=1)

        self.scale3 = Scale(self, from_=min(self.slider_list), to=max(self.slider_list), command=self.scale_value_show3, showvalue=0, orient=HORIZONTAL)#, command=set_plot_range(3))
        self.scale3.grid(row=6, column=2, rowspan=1)

        self.scale3_label = Label(self, textvariable=self.scale3_textvariable)
        self.scale3_label.grid(row=7, column=2, rowspan=1)

        # Plot Sample Chamber temperature

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
        self.cnvs1.get_tk_widget().grid(row=8, column=0)

        self.outputtextbox1_variable = StringVar()

        self.outputtextbox1 = Label(self, textvariable=self.outputtextbox1_variable)

        self.outputtextbox1.grid(row=9, column=0)

        #self.toolbarframe1.grid(row=8, column=0)

        #self.toolbar1 = NavigationToolbar2Tk(self.cnvs1,self.toolbarframe1)
       
        #self.cnvs1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
      
        #Plot Conditioning Chamber temperature

        self.fig2 = Figure(figsize=(4.1, 3.8))
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2_twin = self.ax2.twinx()
        self.ax2.set_xlabel('Time (sec)')
        self.ax2.set_ylabel('pCO2 (ppm)')
        self.ax2_twin.set_ylabel('pH2O (ppt)')
        self.ax2.set_autoscalex_on(True)
        self.ax2_twin.set_autoscalex_on(True)
        #self.ax2.set_ybound(10, 40)
        self.ax2.set_autoscaley_on(True)
        self.ax2.grid(True, 'major', 'both')
        self.fig2.tight_layout()
   
        self.cnvs2 = FigureCanvasTkAgg(self.fig2, self)
        self.cnvs2.get_tk_widget().grid(row=8, column=1)

        self.outputtextbox2_variable = StringVar()

        self.outputtextbox2 = Label(self, textvariable=self.outputtextbox2_variable)

        self.outputtextbox2.grid(row=9, column=1)

        #self.toolbarframe2.grid(row=8, column=1)

        #self.toolbar2 = NavigationToolbar2Tk(self.cnvs2,self.toolbarframe2)

       
        #self.cnvs2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Plot DPG temperature

        self.fig3 = Figure(figsize=(3.8, 3.8))
        self.ax3 = self.fig3.add_subplot(111)
        self.ax3.set_xlabel('Time (sec)')
        self.ax3.set_ylabel('Temperature ($^\circ$C)')
        self.ax3.set_autoscalex_on(True)
        #self.ax3.set_ybound(10, 40)
        self.ax3.set_autoscaley_on(True)
        self.ax3.grid(True, 'major', 'both')
        self.fig3.tight_layout()
   
        self.cnvs3 = FigureCanvasTkAgg(self.fig3, self)
        self.cnvs3.get_tk_widget().grid(row=8, column=2)

        self.outputtextbox3_variable = StringVar()

        self.outputtextbox3 = Label(self, textvariable=self.outputtextbox3_variable)

        self.outputtextbox3.grid(row=9, column=2)

        #self.toolbarframe3.grid(row=8, column=2)

        #self.toolbar3 = NavigationToolbar2Tk(self.cnvs3,self.toolbarframe3)
       
        #self.cnvs3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    '''
    def set_plot_range(graph_no):

        if graph_no == 1:

            self.plot1_range = self.scale1.get()

        elif graph_no == 2:

            self.plot2_range = self.scale2.get()

         elif graph_no == 3:

            self.plot3_range = self.scale3.get()
    '''

    def log_frequency_scale_value_check(self, value):

        newvalue =  min(self.log_frequency_list, key=lambda x:abs(x-float(value)))
       
        self.log_frequency_scale.set(newvalue)

    def scale_value_show1(self, value):

        self.scale1_textvariable.set('Plot range(m): '+ str(self.slider_list_value[int(value)]))

    def scale_value_show2(self, value):

        self.scale2_textvariable.set('Plot range(m): '+ str(self.slider_list_value[int(value)]))

    def scale_value_show3(self, value):

        self.scale3_textvariable.set('Plot range(m): '+ str(self.slider_list_value[int(value)]))

    def animate_temperatures(self, i):

        self.ax1.clear()
        self.ax1.set_xlabel('Time (sec)')
        self.ax1.set_ylabel('Temperature ($^\circ$C)')
        self.ax1.set_autoscalex_on(True)
        #self.ax1.set_ybound(10, 40)
        self.ax1.set_autoscaley_on(True)
        self.ax1.grid(True, 'major', 'both')

        self.plot1_range = self.slider_list_value[self.scale1.get()]*60 #converting seconds to list range

        index = int(self.plot1_range/15.0)

        self.ax1.plot(self.g_sys_instance.time_list[(25000-self.plot1_density*index):], self.g_sys_instance.Temperatures_SC[(25000-self.plot1_density*index):], 'k', label="TSC")

        self.ax1.plot(self.g_sys_instance.time_list[(25000-self.plot2_density*index):], self.g_sys_instance.Temperatures_CC[(25000-self.plot2_density*index):], 'b', label="TCC")

        self.ax1.plot(self.g_sys_instance.time_list[(25000-self.plot3_density*index):], self.g_sys_instance.Temperatures_DPG[(25000-self.plot3_density*index):], 'r', label="TDPG")

        self.ax1.legend()

        self.outputtextbox1_variable.set("TCC = "+str(self.g_sys_instance.Temperatures_CC[-1])+" TSC = "+str(self.g_sys_instance.Temperatures_SC[-1])+" TDPG = "+str(self.g_sys_instance.Temperatures_DPG[-1]))

    def animate_pressures(self, i):

        self.ax2.clear()
        self.ax2_twin.clear()
        self.ax2.set_xlabel('Time (sec)')
        self.ax2.set_ylabel('pCO2 (ppm)')
        self.ax2_twin.set_ylabel('pH2O (ppt)')
        self.ax2.tick_params('y', colors='b')
        self.ax2_twin.tick_params('y', colors='r')
        self.ax2.set_autoscalex_on(True)
        self.ax2.grid(True, 'major', 'both')

        self.plot2_range = self.slider_list_value[self.scale2.get()]*60  #converting seconds to list range

        index = int(self.plot2_range/15.0)

        #print(self.g_sys_instance.pH2O_list[-1])

        self.ax2.plot(self.g_sys_instance.time_list[(25000-self.plot2_density*index):], self.g_sys_instance.pCO2_list[(25000-self.plot2_density*index):], color='b', label='pCO2')

        self.ax2_twin.plot(self.g_sys_instance.time_list[(25000-self.plot2_density*index):], self.g_sys_instance.pH2O_list[(25000-self.plot2_density*index):], color='r', label='pH2O')

        #self.ax2.legend(loc=3)

        #self.ax2_twin.legend(loc=4)

        self.outputtextbox2_variable.set("pCO2 = "+str(self.g_sys_instance.pCO2_list[-1])+" pH2O = "+str(self.g_sys_instance.pH2O_list[-1]))

    def animate_sw(self, i):

        self.ax3.clear()
        self.ax3.set_xlabel('Time (sec)')
        self.ax3.set_ylabel('Weight (g)')

        self.ax3.set_autoscalex_on(True)

        self.ax3.grid(True, 'major', 'both')

        self.plot3_range = self.slider_list_value[self.scale3.get()]*60 
        
        index = int(self.plot3_range/15.0)

        self.ax3.plot(self.g_sys_instance.time_list[(25000-self.plot3_density*index):], self.g_sys_instance.sample_weight[(25000-self.plot3_density*index):], 'k')

        self.outputtextbox3_variable.set("WGT = "+str(self.g_sys_instance.sample_weight[-1]))

    def log_data(self):

        #print(self.log_btn_text.get())

        if str(self.log_btn_text.get()) == "Record data": 

            self.consumer_object.log_data(self, datetime.now(), self.log_frequency_scale.get()) 

        elif str(self.log_btn_text.get()) == 'Stop recording':

            self.consumer_object.stop_logging()

            self.log_btn_text.set('Record data') 
