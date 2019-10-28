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
arduino = serial.Serial('/dev/ttyACM0', 9600)


#%% definitions

ISI = 500;		# interstimulus interval (milliseconds)
N_stim = 5;	# number of bips within a sequence

cant_trials = 1;
#%%
# fprintf(ardu,'ARDU;I%d;N%d;P%d;B%d;E%d;X',[ISI N_stim 100 10 3]);	% send parameters

name = raw_input("Ingrese su nombre: ")

bloque = 1;
for trial in range(cant_trials):
    raw_input("Press Enter to start trial")
    timestr = time.strftime("%Y_%m_%d-%H:%M:%S")
    filename_raw = name+"-"+timestr+"-"+"bloque"+str(bloque)+"-"+"trial"+str(trial)+"-raw.txt"
    filename_stim = name+"-"+timestr+"-"+"bloque"+str(bloque)+"-"+"trial"+str(trial)+"-stim.txt"
    filename_fdbk = name+"-"+timestr+"-"+"bloque"+str(bloque)+"-"+"trial"+str(trial)+"-fdbk.txt"
    filename_asynch = name+"-"+timestr+"-"+"bloque"+str(bloque)+"-"+"trial"+str(trial)+"-asynch.txt"
    
    
    espera = random.randrange(10,20,1)/10.0
    time.sleep(espera)
    
    
    message = ";SR;FR;I%d;N%d;P%d;B%d;E%d;X" % (ISI, N_stim, 100, 10, 3)
    arduino.write(message)
    
    
    data = []
    aux = arduino.readline()
    while (aux[0]!='E'):
        data.append(aux)
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
    fdbk_number = []
    stim_time = []
    fdbk_time = []
    
    for events in range(e_total):
        if e_type[events]=='S':
            stim_number.append(e_number[events])
            stim_time.append(e_time[events])
            
        if e_type[events]=='F':
            fdbk_number.append(e_number[events])
            fdbk_time.append(e_time[events])
            
    long_stim = len(stim_time)
    long_fdbk = len(fdbk_time)
    # Calcula asincronias 
    
    j = 0 #contador de estimulos
    i = long_fdbk-1 #contador de respuestas
    
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
    
# Se fija si el trial es valido. Si lo es, entonces guarda los datos, calcula las asincronias y devuelve los graficos. Si no, no. 
   
    if long_stim_pares == long_fdbk_pares:
        
        # Guarda datos crudos
        f_raw = open(filename_raw,"w+")
        f_stim = open(filename_stim,"w+")
        f_fdbk = open(filename_fdbk,"w+")

        for event in data:
            f_raw.write(event) # guarda los datos crudos
        
        for event in stim_time:
            f_stim.write(str(event)+"\n")   
        
        for event in fdbk_time:
            f_fdbk.write(str(event)+"\n")
        
        f_raw.close()
        f_stim.close()        
        f_fdbk.close()
               
        
        # Calcula y guarda asincronias
        asynchrony = []
        f_asynch = open(filename_asynch,"w+")
        
        for k in range(long_stim_pares):
            asynchrony.append(stim_pares[k]-fdbk_pares[k])
            f_asynch.write(str(stim_pares[k]-fdbk_pares[k])+"\n")
    
        f_asynch.close()
    #==============================================================================
    # Grafica los resultados

#        my_labels = {"stim" : "Stimulus", "fdbk" : "Feedback"}
#        for j in range(long_stim):
#            plt.axvline(x=stim_time[j],color='r',linestyle='dashed',label=my_labels["stim"])
#            my_labels["stim"] = "_nolegend_"
#         
#        for k in range(long_fdbk):
#            plt.axvline(x=fdbk_time[k],color='b',label=my_labels["fdbk"])
#            my_labels["fdbk"] = "_nolegend_"
#           
#        plt.axis([min(stim_time)-50,max(fdbk_time)+50,0,1])
#        plt.xlabel('Tiempo[ms]',fontsize=12)
#        plt.ylabel(' ')
#        plt.grid()    
#        plt.legend(fontsize=12)
#        plt.show()
#         
    #==============================================================================

    #==============================================================================
    # Grafica el rango entre el primer par estimulo-feedback que se queda y el ultimo
    
        my_labels = {"stim" : "Stimulus", "fdbk" : "Feedback"}
        for j in range(long_stim_pares):
            plt.axvline(x=stim_pares[j],color='y',linestyle='dashed',label=my_labels["stim"])
            my_labels["stim"] = "_nolegend_"
        
        for k in range(long_fdbk_pares):
            plt.axvline(x=fdbk_pares[k],color='c',label=my_labels["fdbk"])
            my_labels["fdbk"] = "_nolegend_"
            
        plt.axis([min(fdbk_pares)-50,max(stim_pares)+50,0,1])
          
        plt.xlabel('Tiempo[ms]',fontsize=12)
        plt.ylabel(' ')
        plt.grid()    
        plt.legend(fontsize=12)
        plt.show()
     
    #==============================================================================
    

    #==============================================================================
    # Grafica las asincronias    
        
        plt.plot(asynchrony,'.')
        plt.xlabel('# beep',fontsize=12)
        plt.ylabel('Asynchrony[ms]',fontsize=12)
        plt.grid()    
        plt.show()
        
    #==============================================================================

    else:
        print("Hay que repetir el trial")
        # cant_trials = cant_trials+1 ---- para que esto funcione trials deberia correr en un while