import xml.etree.ElementTree as ET

import datetime

from matplotlib.figure import Figure

import matplotlib.pyplot as plt

import numpy as np

#tree = ET.parse('Data_01_08_2021_part1.xml')

#root = tree.getroot()

f1 = open("Data_1_11_2021_exp1.xml", "r") 

f2 = open("Data_1_11_2021_exp2.xml", "r") 

f3 = open("Data_1_11_2021_exp3.xml", "r") 

lines = f1.readlines() 

DPG_T = []

DPT  = []

date_time = []

date_time_list = []

pH2O = []

T = []

for line in lines:

	root = ET.fromstring(line)
	
	DPG_T.append(float(root[4].text))

	date_time.append((root[1].text))

	DPT.append(float(root[5].text))

	pH2O.append(float(root[7].text))


for date_time_string in date_time:

	date_time_list.append(datetime.datetime.strptime(date_time_string, "%Y-%m-%d %H:%M:%S.%f"))

for i in range(len(date_time_list)):

	T.append((date_time_list[i]-date_time_list[0]).seconds)

DPG_T = np.asarray(DPG_T)

DPT = np.asarray(DPT)

pH2O = np.asarray(pH2O)

T = np.asarray(T)

fig, ax1 = plt.subplots()

ax1.set_xlabel('Time (min)')
ax1.set_ylabel('Temperature ($^\circ$C)')
ax1.grid(True, 'major', 'both')

ax1_twin = ax1.twinx()
ax1_twin.set_ylabel('pH2O (ppt)')

ax1.plot(T/60.0, DPG_T, 'b', label='DPG temperature')

ax1.plot(T/60.0, DPT, 'r', label='Dew point temperature')

ax1_twin.plot(T/60.0, pH2O, 'k', label = 'pH2O')

ax1.set_xlim(10,28)

#ax1.set_ylim(0,25)

plt.legend()

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