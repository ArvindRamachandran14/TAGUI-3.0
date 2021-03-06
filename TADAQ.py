#! /usr/local/bin/python3 
# -*- coding: utf-8 -*-

#################################### Thermodynammic Analyzer Data Acqusition Program #################################### 
from ctypes import c_int, c_double, c_byte, c_bool, Structure, sizeof #creates c type structures
from random import random #random numbers
import mmap #memory map
import os 
from datetime import datetime
import datetime as dt 
import asyncio #timing to work right asychronous call - go and read the data and the meanwhile you can do other things
import socket
import xml.etree.ElementTree as ET
import time
import global_tech_var as g
import sys
import json
import serial
encoding = 'utf-8' # covers straight ascii 8 bit char codes 
loop = None #variable timeer uses
recCount = 21 #how many records are in the shared memory 

#ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=3) #Define serial port

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
            ('command', c_byte * 80), # 80 byte buffer
            ('reply', c_byte * 80),
            ('recCount', c_int),
            ('recIdx', c_int),
            ('data', TAData * recCount)]

class producer() :
    def __init__(self, interval) :
        self.startTime = None
        self.bDone = False 
        self.interval = interval
        self.bForked = False
        self.recNum = 0
        self.taShare = None
        self.taData = None
        self.mmShare = None
        self.mmfd = None
        self.startTime = None
        self.sem = None             # Added semaphore instance here
        self.sock = None
        self.host = 'localhost'     # localhost
        self.port = 50007
        self.initialize()

    @asyncio.coroutine
    def produce(self, ser) :
        TCC = TSC = TSC2 = TDP = TDP2 = Wgt = pH2O = pCO2 = 0.0 # Changed temp1, temp2, temp3 to TCC TSC TDP, added Wgt 
        status = 0
        tash = TAShare.from_buffer(self.mmShare) 
        while not self.bDone : #Run until user wants to EXIT
            command = bytearray(tash.command).decode(encoding).rstrip('\x00')
            if command == '%EXIT' :
                self.mmfd.close()
                self.bDone = True #Set the binary variable to Exit program
            else :
                recIdx = tash.recIdx + 1
                if recIdx >= tash.recCount :
                    recIdx = 0

                # Get some data
                taData = self.getDataFromTA('g all', ser) #added 'g all' paramter to  self.getDataFromTA()

                # Get the time
                now = datetime.now()
                seconds = now.hour * 3600 + now.minute * 60 + now.second + now.microsecond / 1000000
                if self.startTime == None :
                    self.startTime = seconds
                seconds = seconds - self.startTime

                tash.data[recIdx].recNum = self.recNum
                self.recNum += 1
                tash.data[recIdx].recTime = seconds

                #################### Transfer data to the data buffer ####################
                if type(taData).__name__ == 'list' :

                    (TSC, TSC2, TCC, TDP, pH2O, pCO2, TDP2, Wgt, status) = taData #Watch out for the order of variables

                    tash.data[recIdx].SC_T = TSC
                    #tash.data[recIdx].SC_T2 = data_list[1] #SC_T2 omitted in this model
                    tash.data[recIdx].CC_T = TCC
                    tash.data[recIdx].DPG_T = TDP
                    tash.data[recIdx].pH2O = pH2O
                    tash.data[recIdx].pCO2 = pCO2
                    tash.data[recIdx].TDP = TDP2 
                    tash.data[recIdx].Sample_weight = Wgt
                    tash.data[recIdx].Status = status
                
                else:

                    tash.data[recIdx].SC_T = 0
                    #tash.data[recIdx].SC_T2 = data_list[1] #SC_T2 omitted in this model
                    tash.data[recIdx].CC_T = 0
                    tash.data[recIdx].DPG_T = 0
                    tash.data[recIdx].pH2O = 0
                    tash.data[recIdx].pCO2 = 0
                    tash.data[recIdx].TDP = 0
                    tash.data[recIdx].Sample_weight = 0
                    tash.data[recIdx].Status = -1

                tash.recIdx = recIdx

            
                # Print the TADAQ output
                '''
                print('P: {0:4d} {1:10.3f} {2:10.3f} {3:10.3f} {4:10.3f} {5:10.3f} {6:10.3f} {7:10.3f}{8:d}'.format( \
                    tash.data[recIdx].recNum, tash.data[recIdx].recTime, \
                    tash.data[recIdx].SC_T1, tash.data[recIdx].CC_T1, tash.data[recIdx].DPG_T1, \
                    tash.data[recIdx].pH2O, tash.data[recIdx].pCO2, \
                    tash.data[recIdx].Sample_weight, tash.data[recIdx].Status)) #SC_T2 and Dew Point Temp deleted from print statement
                '''
                
                yield from asyncio.sleep(self.interval)
        
        return 0
        
    async def doCmd(self, ser) :
        while not self.bDone :
            async with self.sem:            # async with added here to control access
                tash = TAShare.from_buffer(self.mmShare)
                command = bytearray(tash.command).decode(encoding).rstrip('\x00')
                if not command == '' :
                    #print(f'Command received in TADAQ is: {command}')
                    for idx in range(0,80) :
                        tash.reply[idx] = 0
                        tash.command[idx] = 0
                    if command == '@{EXIT}' :
                        self.bDone = True
                        sReply = 'OK'
                    else :
                        sReply = self.getDataFromTA(command, ser)

                    #print('Reply is', sReply)

                    # Put the reply into the shared reply buffer
                    repBuf = bytearray(sReply, encoding)
                    tash.reply[0:len(repBuf)] = repBuf
                    # Semaphore is released here
            await asyncio.sleep(0.050)
        self.mmfd.close()   

    def initialize(self) :
        tempTASH = TAShare()
        tempTASH.command[0:80] = [0] * 80
        tempTASH.reply[0:80] = [0] * 80
        tempTASH.recCount = recCount
        tempTASH.recIdx = -1
        self.mmfd = open('taShare', 'w+b') # read and write, binary file memory mapped file descriptor
        L = self.mmfd.write(tempTASH) #size of the files
        self.mmfd.flush() #
        print('Mapped size: ', L)
        ### Creating shared memory region between TADAQ and TAGUI ### 
        self.mmShare = mmap.mmap(self.mmfd.fileno(), sizeof(tempTASH))
        self.sem = asyncio.Semaphore(1)         # Added semaphore creation

    def socket_connection(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    
    def getDataFromTA(self, cmd, ser) :

        ############################# This is the function that reads the latest data stored in the TAC ############################# 

        #print(dt.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
	

        with open(g.cfgFile, 'r') as fCfg :
            config = json.loads(fCfg.read())        # Read config file
            g.initialize(config)              # Initialize the globals

        if g.bsimulation == "True": #Simulation mode on

            cmdBytes = bytearray(cmd, 'utf-8')
            try :
                self.sock.send(cmdBytes)
                rData = self.sock.recv(128)
            except Exception :
                retVal = -1
            else :
                sData = rData.decode('utf-8')
                if cmd == 'g all' :
                    if sData[0] == 'v' :
                        sData = sData[2:]
                        vals = sData.split(',', 8)
                        retval = [float(val) for val in vals] #list
                        retval.append(0)            # for status
                    else :
                        retval = sData # string with single value
                else :
                    #print('received response at TADAQ is', sData)
                    retval = sData

            return retval

        elif g.bsimulation == "False": #Experiment mode on

            #print('commmand received in TADAQ end is', cmd)

            if cmd == 'g all':

                cmd+='\n'

                ser.write(cmd.encode())

                Output_string = ser.readline().decode()

                #print('Output is', Output_string)

                Split_strings_list  = Output_string.split(',')

                data_list = []

                for i in range(9):
                
                    if i < 8:

                        data_list.append(float(Split_strings_list[i]))

                    else:
                        
                        data_list.append(int(Split_strings_list[i]))

                return(data_list)

            else:                 

                #print('Command sent is', cmd)
                cmd+='\n'
                print('Command sent is', cmd)

                ser.write(cmd.encode())

                while True:

                    Output = ser.readline().decode()

                    if len(Output) > 0:

                        return(Output) 

        
# main program

async def main() :

    with open(g.cfgFile, 'r') as fCfg :
        config = json.loads(fCfg.read())        # Read config file
        g.initialize(config)              # Initialize the globals

    #print(len(sys.argv))

    if len(sys.argv) == 1: # No arguments passed i.e. simulation mode on

        print('Simulation mode on')

        g.bsimulation = "True"

        g.bconnected = "True" 

    elif len(sys.argv) > 1: # arguments passed i.e. experiment mode on

        print('Experiment mode on')

        g.bsimulation = "False"

        port = sys.argv[1]
        baud_rate = sys.argv[2]
        time_out = int(sys.argv[3])

        ser = serial.Serial(port, baud_rate, timeout=time_out)

        ser.write('c-check\n'.encode()) #Send connection check command to TAC program

        reply = ser.readline().decode()

        print('TADAQ reply was', reply)

        if reply == "Ok\n":

        #print('TADAQ reply was', reply)
   
            g.bconnected = "True"

        time.sleep(1)

        ser.reset_input_buffer()

        ser.reset_output_buffer()

    g.update()

    if g.bconnected == "True":
        prod = producer(2)      # Interval argument

        if g.bsimulation == "True":
            prod.socket_connection()
            task1 = asyncio.create_task(prod.produce(None))
            task2 = asyncio.create_task(prod.doCmd(None))
            await task1
            await task2

        elif g.bsimulation == "False":

            task1 = asyncio.create_task(prod.produce(ser))
            task2 = asyncio.create_task(prod.doCmd(ser))
            await task1
            await task2
       
        print('Done')

asyncio.run(main())
