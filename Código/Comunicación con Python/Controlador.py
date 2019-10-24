# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:04:30 2019

@author: paula
"""

import serial, time
import numpy as np
import matplotlib.pyplot as plt
#%%
arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)


#%% definitions

ISI = 500;		# interstimulus interval (milliseconds)
N_stim = 15;	# number of bips within a sequence


#%%
# fprintf(ardu,'ARDU;I%d;N%d;P%d;B%d;E%d;X',[ISI N_stim 100 10 3]);	% send parameters

name = raw_input("Ingrese su nombre: ")
timestr = time.strftime("%Y_%m_%d-%H:%M:%S")
filename = name+"-"+timestr+"-raw.txt"

message = ";I%d;N%d;P%d;B%d;E%d;X" % (ISI, N_stim, 100, 10, 3)
arduino.write(message)


data = []
aux = arduino.readline()
f = open(filename,"a+")
while (aux[0]!='E'):
    data.append(aux)
    aux = arduino.readline();
    f.write(aux) # guarda los datos crudos
    
f.close()

# Separa los datos en tipo, numero y tiempo
e_total = len(data)
e_type = []
e_number = []
e_time = []
for event in data:
    e_type.append(event.split()[0])
    e_number.append(int(event.split()[1]))
    e_time.append(int(event.split()[2]))

# Separa numero y tiempo segun si corresponden a feedback o estimulo
stim_number = []
fdbk_number = []
stim_time = []
fdbk_time = []
for i in range(e_total):
    if e_type[i]=='S':
        stim_number.append(e_number[i])
        stim_time.append(e_time[i])
    if e_type[i]=='F':
        fdbk_number.append(e_number[i])
        fdbk_time.append(e_time[i])

# Grafica los resultados
long_stim = len(stim_time)
long_fdbk = len(fdbk_time)
my_labels = {"stim" : "Stimulus", "fdbk" : "Feedback"}
plt.figure(figsize=(9,6))
for j in range(long_stim):
    plt.axvline(x=stim_time[j],color='r',linestyle='dashed',label=my_labels["stim"])
    my_labels["stim"] = "_nolegend_"

for k in range(long_fdbk):
    plt.axvline(x=fdbk_time[k],color='b',label=my_labels["fdbk"])
    my_labels["fdbk"] = "_nolegend_"
   
plt.axis([min(stim_time)-10,max(stim_time)+10,0,1])
plt.xlabel('Tiempo[ms]',fontsize=12)
plt.grid()    
plt.legend(fontsize=12)
plt.show()

#%%
# Grafica asincronias 
asynchrony = []
j = 0
i = 0

if long_stim < long_fdbk:
    while i in range(long_fdbk-1):
        diff = stim_time[j]-fdbk_time[i]
        if abs(diff)<150:
            asynchrony.append(diff)
            j = j+1
            i = i+1
        else:
            j = j+1

else:
     while j in range(long_stim-1):
        diff = stim_time[j]-fdbk_time[i]
        if abs(diff)<150:
            asynchrony.append(diff)
            j = j+1
            i = i+1
        else:
            j = j+1


plt.plot(asynchrony,'.')
plt.xlabel('# beep',fontsize=12)
plt.ylabel('Asynchrony[ms]',fontsize=12)
plt.grid()    
plt.show()