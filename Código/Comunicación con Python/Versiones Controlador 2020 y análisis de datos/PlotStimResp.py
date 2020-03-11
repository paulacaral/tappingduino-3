# -*- coding: utf-8 -*-
"""
Created on Thu Mar 05 15:29:31 2020

@author: Paula
"""
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

#%%
def Loading_data(subject_number,block, trial, *asked_data):
    # IMPORTANTE: DAR INPUTS COMO STRING
    # Hay que darle si o si numero de sujeto y bloque y el trial puede estar especificado o ser None. Recordar que los archivos que no tienen identificado el trial tienen guardada la informacion de todo el bloque: condicion usada, errores, percepcion del sujeto y si el trial fue valido o invalido. En cambio, al especificar el trial se tiene la informacion de cada trial particular, es decir, asincronias, datos crudos, respuestas y estimulos.

    if trial is None:
        file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Codigo\2020\DATOS/S'+subject_number+"*-block"+str(block)+"-trials.npz")
       # file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/S'+subject_number+"*-block"+str(block)+"-trials.npz")    
    else:
        file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Codigo\2020\DATOS/S'+subject_number+"*-block"+str(block)+"-trial"+str(trial)+".npz")    
    
        #file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/S'+subject_number+"*-block"+str(block)+"-trial"+str(trial)+".npz")    
    
    npz = np.load(file_to_load[0])
    if len(asked_data) == 0:
        print("The file contains:")
        return sorted(npz)
    else:
        data_to_return = []
        for a in asked_data:
            data_to_return.append(npz[a])                                
        return data_to_return[:]


#%% Cargar datos

stim_time = Loading_data('005',3,6,'stim')
resp_time = Loading_data('005',3,6,'resp')
N_stim = len(stim_time[0])
N_resp = len(resp_time[0])

#%% Plot 
#==============================================================================
#  Plot all pair of stimulus and feedback
plt.figure(1,figsize=(20,20),dpi=72)

my_labels = {"stim" : "Stimulus", "resp" : "Response"}
for j in range(N_stim):
    plt.axvline(x=stim_time[0][j],color='b',linestyle='dashed',label=my_labels["stim"])
    my_labels["stim"] = "_nolegend_"
 
for k in range(N_resp):
     plt.axvline(x=resp_time[0][k],color='r',label=my_labels["resp"])
     my_labels["resp"] = "_nolegend_"
 
 # Put a yellow star on the stimulus that have a paired response.
#for j in range(N_stim_paired):
#    plt.plot(stim_paired[j],0.5,'*',color='y')
 
plt.axis([min(stim_time[0])-50,max(resp_time[0])+50,0,1])
   
plt.xlabel('Tiempo[ms]',fontsize=12)
plt.ylabel(' ')
plt.grid()    
plt.legend(fontsize=12)
                 

# Plot asynchronies
#plt.figure(2)
#plt.plot(asynchrony,'.-')
#plt.xlabel('# beep',fontsize=12)
#plt.ylabel('Asynchrony[ms]',fontsize=12)
#plt.grid()    
#==============================================================================
