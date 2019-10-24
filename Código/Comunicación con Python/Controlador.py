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
N_stim = 10;	# number of bips within a sequence


#%%
# fprintf(ardu,'ARDU;I%d;N%d;P%d;B%d;E%d;X',[ISI N_stim 100 10 3]);	% send parameters

name = raw_input("Ingrese su nombre: ")
timestr = time.strftime("%Y_%m_%d-%H:%M:%S")
filename = name+"-"+timestr+"-raw.txt"


message = ";SB;FB;I%d;N%d;P%d;B%d;E%d;X" % (ISI, N_stim, 100, 10, 3)
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

#%%
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
   
plt.axis([min(stim_time)-50,max(fdbk_time)+50,0,1])
plt.xlabel('Tiempo[ms]',fontsize=12)
plt.grid()    
plt.legend(fontsize=12)
plt.show()

#%%
# Grafica asincronias 

j = 0
i = long_fdbk-1

while j < long_stim:
    diff = stim_time[j]-fdbk_time[0]
    if abs(diff)<200:
        indice_primer_stim = j
        break;
    else:
        j = j+1

while i > 0:
    diff = stim_time[long_stim-1]-fdbk_time[i]
    if abs(diff)<200:
        indice_ultimo_fdbk = i+1
        break;
    else:
        i = i-1

stim_pares = stim_time[indice_primer_stim:]
fdbk_pares = fdbk_time[0:indice_ultimo_fdbk]


long_stim_pares = len(stim_pares)
long_fdbk_pares = len(fdbk_pares)
my_labels = {"stim" : "Stimulus", "fdbk" : "Feedback"}
plt.figure(figsize=(9,6))
for j in range(long_stim_pares):
    plt.axvline(x=stim_pares[j],color='y',linestyle='dashed',label=my_labels["stim"])
    my_labels["stim"] = "_nolegend_"

for k in range(long_fdbk_pares):
    plt.axvline(x=fdbk_pares[k],color='c',label=my_labels["fdbk"])
    my_labels["fdbk"] = "_nolegend_"
    
plt.axis([min(fdbk_pares)-50,max(stim_pares)+50,0,1])
  
plt.xlabel('Tiempo[ms]',fontsize=12)
plt.grid()    
plt.legend(fontsize=12)
plt.show()


asynchrony = []

for k in range(long_stim_pares):
    asynchrony.append(stim_pares[k]-fdbk_pares[k])

plt.plot(asynchrony,'.')
plt.xlabel('# beep',fontsize=12)
plt.ylabel('Asynchrony[ms]',fontsize=12)
plt.grid()    
plt.show()