import xml.etree.ElementTree as ET

import datetime

from matplotlib.figure import Figure

import matplotlib.pyplot as plt

import numpy as np


f = open("CC_calibration_02_01_2021.xml", "r") 

f2 = open("CC_calibration_part_2_02_01_2021.xml","r")

f3 = open("CC_calibration_part_3_02_01_2021.xml","r")

f4 = open("CC_calibration_part_4_02_02_2021.xml", "r")

lines = f4.readlines() 

CC_T = []

SC_T = []

DPG_T = []

DPT  = []

date_time = []

date_time_list = []

pH2O = []

pCO2 = []

T = []

for line in lines:

	root = ET.fromstring(line)

	date_time.append((root[1].text))
	
	SC_T.append(float(root[2].text))

	CC_T.append(float(root[3].text))

	DPG_T.append(float(root[4].text))

	DPT.append(float(root[5].text))

	pCO2.append(float(root[6].text))

	pH2O.append(float(root[7].text))


for date_time_string in date_time:

	date_time_list.append(datetime.datetime.strptime(date_time_string, "%Y-%m-%d %H:%M:%S.%f"))

for i in range(len(date_time_list)):

	T.append((date_time_list[i]-date_time_list[0]).seconds)

DPG_T = np.asarray(DPG_T)

DPT = np.asarray(DPT)

pH2O = np.asarray(pH2O)

#print(len(T))

T = np.asarray(T)

fig, ax1 = plt.subplots()

ax1.set_xlabel('Time (min)')
ax1.set_ylabel('Temperature (C')
#ax1.set_ylabel('Temperature ($^\circ$C)')
ax1.grid(True, 'major', 'both')

#ax1_twin = ax1.twinx()
#ax1_twin.set_ylabel('pH2O (ppt)')

#ax1.plot(T/60.0, pCO2, 'k', label = 'pH2O')

#ax1.plot(T/60.0, SC_T, 'y', label='SC temperature')

ax1.plot(T/60.0, CC_T, 'm', label='CC temperature')

#ax1.plot(T/60.0, DPG_T, 'b', label='DPG temperature')

#ax1.plot(T/60.0, DPT, 'r', label='Dew point temperature')

#ax1.legend(loc=2)

#ax1_twin.plot(T/60.0, pH2O, 'k', label = 'pH2O')

#ax1_twin.legend(loc=1)

#ax1.set_xlim(90,108)

#ax1.set_ylim(10,35)

#ax1_twin.set_ylim(13,31)

#ax1_twin.set_ylim(14,33)

plt.tight_layout()

plt.show()



#2021-01-08 01:43:03.053016

''''
dict = {}

for child in root:

	dict['pCO2'] = float(child.find('co2').text)

	dict['pH2O'] = float(child.find('h2o').text)

	dict['IVOLT'] = float(child.find('ivolt').text)

	dict['Cell_temp'] = float(child.find('celltemp').text)

	dict['Cell_pressure'] = float(child.find('cellpres').text)


print(dict)

'''
