# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:04:30 2019

@author: paula
"""

import serial, time
import numpy as np
import matplotlib.pyplot as plt
import random
#%%

#arduino = serial.Serial('/dev/ttyACM0', 9600)
arduino = serial.Serial('/COM3', 9600)

#%% definitions

ISI = 500;		# interstimulus interval (milliseconds)
N_stim = 10;	# number of bips within a sequence

#%%
# fprintf(ardu,'ARDU;I%d;N%d;P%d;B%d;E%d;X',[ISI N_stim 100 10 3]);	% send parameters

name = raw_input("Ingrese su nombre: ")

cant_trials = 1;
trial = 0

#name = "fijo";
bloque = 1;
raw_input("Press Enter to start trial")
timestr = time.strftime("%Y_%m_%d-%H.%M.%S")
#==============================================================================
# 
# filename_valid_trials = name+"-"+timestr+"-"+"bloque"+str(bloque)+"-trials.txt" 
# f_trial = open(filename_valid_trials,"a+")
#            
#==============================================================================
valid_trial = []
filename_trial = name+"-"+"bloque"+str(bloque)+"-trials"

while (trial < cant_trials):
#==============================================================================
#     # Genero todos los archivos: crudo, stim, resp y asynch
#     filename_raw = name+"-"+timestr+"-"+"bloque"+str(bloque)+"-"+"trial"+str(trial)+"-raw.txt"
#     filename_stim = name+"-"+timestr+"-"+"bloque"+str(bloque)+"-"+"trial"+str(trial)+"-stim.txt"
#     filename_resp = name+"-"+timestr+"-"+"bloque"+str(bloque)+"-"+"trial"+str(trial)+"-resp.txt"
#     filename_asynch = name+"-"+timestr+"-"+"bloque"+str(bloque)+"-"+"trial"+str(trial)+"-asynch.txt"
#     
#     f_raw = open(filename_raw,"w+")
#     f_stim = open(filename_stim,"w+")
#     f_resp = open(filename_resp,"w+")
#     f_asynch = open(filename_asynch,"w+")
# 
#==============================================================================

    filename_data = name+"-"+timestr+"-"+"bloque"+str(bloque)+"-"+"trial"+str(trial)
        
    filename_data_load = name+"-"+timestr+"-"+"bloque"+str(bloque)+"-"+"trial"


    espera = random.randrange(10,20,1)/10.0
    time.sleep(espera)
    
    
    message = ";SR;FR;I%d;N%d;P%d;B%d;E%d;X" % (ISI, N_stim, 100, 10, 3)
    arduino.write(message)
    
    
    data = []
    aux = arduino.readline()
    while (aux[0]!='E'):
        data.append(aux);
#        f_raw.write(aux); # guarda los datos crudos
        aux = arduino.readline();
        
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
    resp_number = []
    stim_time = []
    resp_time = []
    
    for events in range(e_total):
        if e_type[events]=='S':
            stim_number.append(e_number[events])
            stim_time.append(e_time[events])
#            f_stim.write(str(e_time[events])+"\n")   

            
        if e_type[events]=='F':
            resp_number.append(e_number[events])
            resp_time.append(e_time[events])
#            f_resp.write(str(e_time[events])+"\n")

    long_stim = len(stim_time)
    long_resp = len(resp_time)


#==============================================================================
#                
#     f_raw.close()
#     f_stim.close()        
#     f_resp.close()
# 
#==============================================================================

    # Calcula asincronias 
    
    j = 0 #contador de estimulos
    i = long_resp-1 #contador de respuestas
    
    while j < long_stim:
        diff = stim_time[j]-resp_time[0]
        if abs(diff)<200:
            indice_primer_stim = j
            break;
        else:
            j = j+1
    
    while i > 0:
        diff = stim_time[long_stim-1]-resp_time[i]
        if abs(diff)<200:
            indice_ultimo_resp = i+1
            break;
        else:
            i = i-1
    
    stim_pares = stim_time[indice_primer_stim:]
    resp_pares = resp_time[0:indice_ultimo_resp]
    long_stim_pares = len(stim_pares)
    long_resp_pares = len(resp_pares)
    
# Se fija si el trial es valido. Si lo es, entonces guarda los datos, calcula las asincronias y devuelve los graficos. Si no, no. 
   
    asynchrony = []

    if long_stim_pares == long_resp_pares:
                
        valid_trial.append(1)
#        f_trial.write(str(trial)+"\t 1 \n")
        # Calcula y guarda asincronias
        
        for k in range(long_stim_pares):
            asynchrony.append(stim_pares[k]-resp_pares[k])
#            f_asynch.write(str(stim_pares[k]-resp_pares[k])+"\n")
    
#        f_asynch.close()
    #==============================================================================
    # Grafica los resultados

#        my_labels = {"stim" : "Stimulus", "resp" : "Feedback"}
#        for j in range(long_stim):
#            plt.axvline(x=stim_time[j],color='r',linestyle='dashed',label=my_labels["stim"])
#            my_labels["stim"] = "_nolegend_"
#         
#        for k in range(long_resp):
#            plt.axvline(x=resp_time[k],color='b',label=my_labels["resp"])
#            my_labels["resp"] = "_nolegend_"
#           
#        plt.axis([min(stim_time)-50,max(resp_time)+50,0,1])
#        plt.xlabel('Tiempo[ms]',fontsize=12)
#        plt.ylabel(' ')
#        plt.grid()    
#        plt.legend(fontsize=12)
#        plt.show()
#         
    #==============================================================================

    #==============================================================================
    # Grafica el rango entre el primer par estimulo-feedback que se queda y el ultimo
    
        my_labels = {"stim" : "Stimulus", "resp" : "Feedback"}
        for j in range(long_stim_pares):
            plt.axvline(x=stim_pares[j],color='y',linestyle='dashed',label=my_labels["stim"])
            my_labels["stim"] = "_nolegend_"
        
        for k in range(long_resp_pares):
            plt.axvline(x=resp_pares[k],color='c',label=my_labels["resp"])
            my_labels["resp"] = "_nolegend_"
            
        plt.axis([min(resp_pares)-50,max(stim_pares)+50,0,1])
          
        plt.xlabel('Tiempo[ms]',fontsize=12)
        plt.ylabel(' ')
        plt.grid()    
        plt.legend(fontsize=12)
        #plt.show()
     
    #==============================================================================
    

    #==============================================================================
    # Grafica las asincronias    
        
        plt.figure()
        plt.plot(asynchrony,'.')
        plt.xlabel('# beep',fontsize=12)
        plt.ylabel('Asynchrony[ms]',fontsize=12)
        plt.grid()    
        #plt.show()
        
    #==============================================================================

        trial = trial + 1;
    
    else:
        valid_trial.append(0)
#        f_trial.write(str(trial)+"\t 0 \n")

#        f_asynch.close()
        print("Hay que repetir el trial")
        raw_input("Press Enter to start trial")
        trial = trial + 1;
        cant_trials = cant_trials+1;
    
    np.savez_compressed(filename_data, crudo=data, stim=stim_time, resp=resp_time, asynch=asynchrony)
        
#f_trial.close()
    
np.savez_compressed(filename_trial,trials=valid_trial)

#%%

npztrial = np.load(filename_trial+".npz")
npztrial["trials"]

trial1 = np.load(filename_data_load+"1.npz")

trial1["crudo"]
trial1["stim"]
trial1["resp"]
trial1["asynch"]
