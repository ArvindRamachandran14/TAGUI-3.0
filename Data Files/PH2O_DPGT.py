import xml.etree.ElementTree as ET

import datetime

from matplotlib.figure import Figure

import matplotlib.pyplot as plt

import numpy as np

f = open("Data_01_18_2021.xml", "r") 

lines = f.readlines() 

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


DPG_T_max_index = DPG_T.index(np.max(DPG_T[100:500]))

DPT_max_index = DPT.index(np.max(DPT[100:500]))

print(DPG_T_max_index, DPT_max_index)

print(date_time[DPG_T_max_index], date_time[DPT_max_index])


plt.plot(np.asarray(T[450:690])-T[450],DPG_T[450:690])

plt.plot(np.asarray(T[450:690])-T[450],DPT[450:690])


#plt.plot(np.asarray(T[465:705])-T[465], DPT[465:705])

#plt.plot(DPG_T[450:490], pH2O[465:505], 'ko')

plt.show()


