#! /usr/local/bin/python3 
# -*- coding: utf-8 -*-

# This is a conumer example.

from ctypes import c_int, c_double, c_byte, c_bool, Structure, sizeof
from random import random
import mmap
import os
import time
from datetime import datetime, timedelta
from subprocess import Popen
from pathlib import Path
import tkinter as tk
import json
#import pykbhit as pykb
import global_tech_var as g_tech_instance
import dicttoxml

encoding = 'utf-8'
loop = None
recCount = 21

class TAData(Structure) :
    _pack_ = 4
    _fields_ = [ \
        ('recNum', c_int),
        ('recTime', c_double),
        ('SC_T', c_double),
        ('CC_T', c_double),
        ('DPG_T', c_double),
        ('pH2O', c_double),
        ('pCO2', c_double),
        ('TDP', c_double),
        ('Sample_weight', c_double),
        ('Status', c_int)
        ]

class TAShare(Structure) :
    _pack_ = 4
    _fields_ = [ \
            ('command', c_byte * 80),
            ('reply', c_byte * 80),
            ('recCount', c_int),
            ('recIdx', c_int),
            ('data', TAData * recCount)]

class consumer() :
    def __init__(self, g_sys_instance) :

        #self.g_tech_instance= g_tech_instance
        self.g_sys_instance = g_sys_instance
        self.startTime = None
        self.bDone = False
        self.recNum = 0
        self.taShare = None
        self.taData = None
        self.mmShare = None
        self.mmfd = None
        self.lastIdx = -1
        self.recsGot = 0
        self.f = None
        self.last_logged_time = datetime.now()
        self.log_frequency = 2
        #self.f = open('data_file_'+str(datetime.now())+'.xml', "w+")
        #self.kb = pykb.KBHit()

    # consume
    # This function gets unread data from the shared memory circular
    # buffer at the specified interval.
    def consume(self) :

        tash = TAShare.from_buffer(self.mmShare)

        while not self.lastIdx == tash.recIdx :
            self.lastIdx += 1
            if self.lastIdx == recCount :
                
                self.lastIdx = 0

            tad = TAData.from_buffer(tash.data[self.lastIdx])

            temp_dict = {}

            if tad.SC_T > 0.0:
                
                self.g_sys_instance.Temperatures_SC.append(round(tad.SC_T,2))

                self.g_sys_instance.Temperatures_CC.append(round(tad.CC_T,2))

                self.g_sys_instance.Temperatures_DPG.append(round(tad.DPG_T,2))

                self.g_sys_instance.Temperatures_DP.append(round(tad.TDP,2))

                self.g_sys_instance.pH2O_list.append(round(tad.pH2O,2))

                self.g_sys_instance.pCO2_list.append(round(tad.pCO2,2))

                self.g_sys_instance.sample_weight.append(round(tad.Sample_weight,2))

                self.g_sys_instance.time_list.append(tad.recTime)

                temp_dict['datetime'] = datetime.now()

                temp_dict['time'] = str(temp_dict['datetime'])

                temp_dict['SC_T'] = tad.SC_T

                temp_dict['CC_T'] = tad.CC_T

                temp_dict['DPG_T'] = tad.DPG_T

                temp_dict['TDP'] = tad.TDP

                temp_dict['pCO2'] = tad.pCO2

                temp_dict['pH2O'] = tad.pH2O

                temp_dict['Sample_weight'] = tad.Sample_weight

            xmlstring = dicttoxml.dicttoxml(temp_dict, attr_type=False, custom_root='TAData').replace(b'<?xml version="1.0" encoding="UTF-8" ?>', b'')

            self.g_sys_instance.time_list.pop(0)

            self.g_sys_instance.Temperatures_SC.pop(0)

            self.g_sys_instance.Temperatures_CC.pop(0)

            self.g_sys_instance.Temperatures_DPG.pop(0)

            self.g_sys_instance.Temperatures_DP.pop(0)

            self.g_sys_instance.pH2O_list.pop(0)

            self.g_sys_instance.pCO2_list.pop(0)

            self.g_sys_instance.sample_weight.pop(0)


            if self.g_sys_instance.blogging == True and temp_dict['datetime'] >= self.last_logged_time + timedelta(seconds=self.log_frequency):   

                #print(xmlstring.decode("utf-8"))

                self.f.write(xmlstring.decode("utf-8")+'\n')

                self.last_logged_time += timedelta(seconds=self.log_frequency)

            '''
            print('P: {0:4d} {1:10.3f} {2:10.3f} {3:10.3f} {4:10.3f} {5:10.3f} {6:10.3f} {7:10.3f} {8:d}'.format( \
                tad.recNum, tad.recTime, \
                tad.SC_T1, tad.CC_T1, tad.DPG_T1, \
                tad.pH2O, tad.pCO2,\
                tad.Sample_weight, tad.Status))
            '''
            self.recsGot += 1

        return 0

    def initialize(self) :

        self.mmfd = open('taShare', 'r+b')

        self.mmShare = mmap.mmap(self.mmfd.fileno(), sizeof(TAShare))


    def Connect(self, mainform_object,  monitor_object, serial_port, baud_rate, time_out):
        
        shFile = Path('taShare')
        if shFile.is_file() :
            os.remove('taShare')

        if self.g_sys_instance.bsimulation == True:

            Popen(['python3', 'TADAQ.py']) #Starts the TADAQ program

        elif self.g_sys_instance.bsimulation == False:

            Popen(['python3', 'TADAQ.py', serial_port, baud_rate, time_out]) #Starts the TADAQ program

        time.sleep(2) #Time for TADAQ to edit bconnected flag in taui.json

        with open('taui.json', 'r') as fCfg :
            
            config = json.loads(fCfg.read())

            bconnected = config["bconnected"] 

        if bconnected == "True":

            self.initialize()

            mainform_object.connect_btn_text.set("Disconnect")

            mainform_object.status_label_text.set('Running')

            #monitor_object.ax1.clear()

            #monitor_object.ax2.clear()

            #monitor_object.ax2_twin.clear()

            #monitor_object.ax3.clear()

            #self.g_sys_instance.run_experiment = True

    def log_data(self, monitor_object, start_time, log_frequency):

        #self.f.write('<Data>')

        self.g_sys_instance.blogging = True

        self.last_logged_time = start_time

        self.log_frequency = log_frequency

        monitor_object.log_btn_text.set("Stop recording")

    def stop_logging(self):

        self.g_sys_instance.blogging = False

        #self.f.write('<\Data>')

        self.f.close()

    def send_command_to_PC(self, command):

        #print('command received is', command)

        tash = TAShare.from_buffer(self.mmShare)

        cmdBuf = bytearray(command, encoding) 

        tash.command[0:len(cmdBuf)] = cmdBuf #adding command to shared memory

        time.sleep(2) #Small time delay needed to get response back

        #Get the reply until its not empty, but also have a time out incase there was no commmand or the connection broke

        reply = bytearray(tash.reply).decode(encoding).rstrip('\x00') # Decoding reply from shared memory

        #print('reply on the consumer end is ', reply)

        #print(type(reply))

        return(reply)
        
    def Disconnect(self, mainform_object, monitor_object):

        print('Disconnecting')

        tash = TAShare.from_buffer(self.mmShare)

        cmdBuf = bytearray('@{EXIT}', encoding) #send the EXIT command to the shared memory, the TADAQ reads this and exits thhe program

        tash.command[0:len(cmdBuf)] = cmdBuf

        g_tech_instance.bconnected = "False"

        mainform_object.status_label_text.set('Idle')

        #self.g_sys_instance.run_experiment = False

        print(g_tech_instance.cfg)

        monitor_object.ax1.clear()

        monitor_object.ax2.clear()

        monitor_object.ax2_twin.clear()

        monitor_object.ax3.clear()

        #print('Disconnected')

        #self.ser_PC.close()
