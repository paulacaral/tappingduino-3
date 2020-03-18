# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 11:25:14 2020

@author: paula
"""

import serial, time
import numpy as np
import matplotlib.pyplot as plt
import random
import os
from itertools import permutations 
import glob
import pickle
import pandas as pd


#%%

# Define Python user-defined exceptions
class Error(Exception):
   """Base class for other exceptions"""
   pass

#%% METO TODO LO DE ABAJO EN UNA FUNCIÓN

def Check_trials(subject_number,cant_total_block):
    for block in range(cant_total_block):
        aux = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\2020\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"-*-block"+str(block)+"*-raw.dat")
        errors = []
        valid_trial = []
        for trial in range(len(aux)):
            filename_raw_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\2020\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"-*-block"+str(block)+"-trial"+str(trial)+"-raw.dat")
            df = pd.read_table(filename_raw_load[0], sep="\s+",header=None)

            data = []
            
            for j in range(len(df)):    
                x = []
                for k in range(3):
                    x.append(str(df[k][j]))
                y = ' '.join(x)
                data.append(y)
            
            # Separates data in type, number and time
            e_total = len(data)
            e_type = []
            e_number = []
            e_time = []
            for event in data:
                e_type.append(event.split()[0])
                e_number.append(int(event.split()[1]))
                e_time.append(int(event.split()[2]))
            
            # Separates number and time according to if it comes from stimulus or response
            stim_number = []
            resp_number = []
            stim_time = []
            resp_time = []
            for events in range(e_total):
                if e_type[events]=='S':
                    stim_number.append(e_number[events])
                    stim_time.append(e_time[events])
                    
                if e_type[events]=='R':
                    resp_number.append(e_number[events])
                    resp_time.append(e_time[events])
            
            # determine number of stimulus and responses registered
            N_stim = len(stim_time)
            N_resp = len(resp_time)
           
            asynchrony = []

            try: 
                if N_resp > 0: # if there were any responses
                
                    j = 0; # stimulus counter
                    k = 0; # responses counter for finding first stimuli with decent response
                    i = N_resp-1; # responses counter for finding last stimuli with response
                    first_stim_responded_flag = False; # flag if there was a stimuli with a recent response
                    last_resp_flag = False;         
                    
                    # find first stimulus with a decent response
                    while j < 5: # if the first response doesn't match with any of the 5 first stimuli, then re-do the trial
                        diff = stim_time[j]-resp_time[k];
                        if abs(diff)<200:
                            first_stim_responded_index = j;
                            first_stim_responded_flag = True;
                            break;
                        else:
                            j = j+1;
     
                    
                    if first_stim_responded_flag == True:
                        pass;
                    else:
                        #print('Error tipo NFR')
                        errors.append('NoFirstResp')
                        raise Error 
                                    
                    
                    # find response to last stimulus (last response that should be considerated)
                    while i > 0:
                        diff = stim_time[N_stim-1]-resp_time[i]
                        if abs(diff)<200:
                            last_resp_index = i;
                            last_resp_flag = True;
                            break;
                        else:
                            i = i-1;
                            
                    if last_resp_flag == True:
                        pass;
                    else:
                        #print('Error tipo NLR')
                        errors.append('NoLastResp')
                        raise Error 
                                
                    
                    # new vectors of stimulus and responses that only contain those that have a pair of the other type        
                    stim_paired = stim_time[first_stim_responded_index:N_stim]
                    resp_paired = resp_time[0:(last_resp_index+1)]
                    N_stim_paired = len(stim_paired)
                    N_resp_paired = len(resp_paired)
                    
                    if N_stim_paired == N_resp_paired:
                                          
                        
                        # Calculate and save asynchronies
                        for k in range(N_stim_paired):
                            diff = resp_paired[k]-stim_paired[k]
                            if abs(diff)<200:
                                asynchrony.append(diff)
                            else:
                                #print('Error tipo OOT')
                                errors.append('OutOfThreshold')
                                raise Error
                                
                                 
                        # if the code got here, then the trial is valid!:
                        valid_trial.append(1)
                        errors.append('NoError') 
                                           
                    else:
                        if N_stim_paired > N_resp_paired: # if subject skipped an stimuli
                            # trial is not valid! then:
                            #print('Error tipo SS')
                            errors.append('SkipStim')
                        else: # if there's too many responses
                            # trial is not valid! then:
                            #print('Error tipo TMR')
                            errors.append('TooManyResp')
                        
                        raise Error
                        
                          
                else: # if there were no responses
                    # trial is not valid! then:
                    #print('Error tipo NR')
                    errors.append('NoResp')  
                    raise Error
                 
                   
            except (Error):
                # trial is not valid! then:
                valid_trial.append(0)
                    
                # appends conditions for this trial at the end of the conditions vectors, so that it can repeat at the end
                #Stim_conds.append(Stim_conds[trial])
                #Fdbk_conds.append(Fdbk_conds[trial])
                
        # Chequeo si el nuevo vector de errores es igual al guardado para ese bloque en el vivo
        err_prev_raw=Loading_data(subject_number,block,None,'errors')
        err_prev = []
        for l in range(len(err_prev_raw[0])):
            err_prev.append(err_prev_raw[0][l])
            
        if errors == err_prev:
            print("Los trials del bloque "+str(block)+" están bien clasificados")
        else:
            print("Los trials del bloque "+str(block)+" NO están bien clasificados, mira:")
            print("El vector de errores del vivo es: ") 
            print(err_prev)
            print("El vector de errores del check es: ")
            print(errors)
            
    return errors
#%%

# AHORA EN PARTES FUERA DE LA FUNCION


#%% Load raw file for trial
# Loads raw file for trial and creates a vector data that emulates exactly what it would get from arduino in real time in an experiment.

subject_number = '001'
block = 1
trial = 2
#filename_raw_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/S'+subject_number+"-*-block"+str(block)+"-trial"+str(trial)+"-raw.dat")

filename_raw_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\2020\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"-*-block"+str(block)+"-trial"+str(trial)+"-raw.dat")

df = pd.read_table(filename_raw_load[0], sep="\s+",header=None)

data = []

for j in range(len(df)):    
    x = []
    for i in range(3):
        x.append(str(df[i][j]))
    y = ' '.join(x)
    data.append(y)

#%% Process the data

# read information from arduino
#data = []
#aux = arduino.readline()
#while (aux[0]!='E'):
#    data.append(aux);
#    f_raw.write(aux); # save raw data
#    aux = arduino.readline();
#

# Separates data in type, number and time
e_total = len(data)
e_type = []
e_number = []
e_time = []
for event in data:
    e_type.append(event.split()[0])
    e_number.append(int(event.split()[1]))
    e_time.append(int(event.split()[2]))

# Separates number and time according to if it comes from stimulus or response
stim_number = []
resp_number = []
stim_time = []
resp_time = []
for events in range(e_total):
    if e_type[events]=='S':
        stim_number.append(e_number[events])
        stim_time.append(e_time[events])
        
    if e_type[events]=='R':
        resp_number.append(e_number[events])
        resp_time.append(e_time[events])

# determine number of stimulus and responses registered
N_stim = len(stim_time)
N_resp = len(resp_time)

# close raw data file    
#f_raw.close()

#%% Data is put to the test to know if the trial is valid or invalid
# ---------------------------------------------------------------
# Asynchronies calculation

# vector that will contain asynchronies if they are calculated
asynchrony = []

try: 
    if N_resp > 0: # if there were any responses
    
        j = 0; # stimulus counter
        k = 0; # responses counter for finding first stimuli with decent response
        i = N_resp-1; # responses counter for finding last stimuli with response
        first_stim_responded_flag = False; # flag if there was a stimuli with a recent response
        last_resp_flag = False;                
        
        
        # find first stimulus with a decent response
        while j < 5: # if the first response doesn't match with any of the 5 first stimuli, then re-do the trial
            diff = stim_time[j]-resp_time[k];
            if abs(diff)<200:
                first_stim_responded_index = j;
                first_stim_responded_flag = True;
                break;
            else:
                j = j+1;

        
        if first_stim_responded_flag == True:
            pass;
        else:
            print('Error tipo NFR')
            errors.append('NoFirstResp')
            raise Error 
                        
        
        # find response to last stimulus (last response that should be considerated)
        while i > 0:
            diff = stim_time[N_stim-1]-resp_time[i]
            if abs(diff)<200:
                last_resp_index = i;
                last_resp_flag = True;
                break;
            else:
                i = i-1;
                
        if last_resp_flag == True:
            pass;
        else:
            print('Error tipo NLR')
            errors.append('NoLastResp')
            raise Error 
                    
        
        # new vectors of stimulus and responses that only contain those that have a pair of the other type        
        stim_paired = stim_time[first_stim_responded_index:N_stim]
        resp_paired = resp_time[0:(last_resp_index+1)]
        N_stim_paired = len(stim_paired)
        N_resp_paired = len(resp_paired)
        
        if N_stim_paired == N_resp_paired:
                              
            
            # Calculate and save asynchronies
            for k in range(N_stim_paired):
                diff = resp_paired[k]-stim_paired[k]
                if abs(diff)<200:
                    asynchrony.append(diff)
                else:
                    print('Error tipo OOT')
                    errors.append('OutOfThreshold')
                    raise Error
                    
                     
            # if the code got here, then the trial is valid!:
            valid_trial.append(1)
            errors.append('NoError') 
            
        #==============================================================================
        # Plot all pair of stimulus and feedback
#                    plt.figure(1)
#                    my_labels = {"stim" : "Stimulus", "resp" : "Response"}
#                    for j in range(N_stim):
#                        plt.axvline(x=stim_time[j],color='b',linestyle='dashed',label=my_labels["stim"])
#                        my_labels["stim"] = "_nolegend_"
#                    
#                    for k in range(N_resp):
#                        plt.axvline(x=resp_time[k],color='r',label=my_labels["resp"])
#                        my_labels["resp"] = "_nolegend_"
#                    
#                # Put a yellow star on the stimulus that have a paired response.
#                    for j in range(N_stim_paired):
#                        plt.plot(stim_paired[j],0.5,'*',color='y')
#                        
#                    plt.axis([min(stim_time)-50,max(resp_time)+50,0,1])
#                      
#                    plt.xlabel('Tiempo[ms]',fontsize=12)
#                    plt.ylabel(' ')
#                    plt.grid()    
#                    plt.legend(fontsize=12)
            
        #==============================================================================
   
        #==============================================================================
        # Plot asynchronies
#                    plt.figure(2)
#                    plt.plot(asynchrony,'.-')
#                    plt.xlabel('# beep',fontsize=12)
#                    plt.ylabel('Asynchrony[ms]',fontsize=12)
#                    plt.grid()    
        #==============================================================================
    
            # go to next trial
            trial = trial + 1;
        
        else:
            if N_stim_paired > N_resp_paired: # if subject skipped an stimuli
                # trial is not valid! then:
                print('Error tipo SS')
                errors.append('SkipStim')
            else: # if there's too many responses
                # trial is not valid! then:
                print('Error tipo TMR')
                errors.append('TooManyResp')
            
            raise Error
            
              
    else: # if there were no responses
        # trial is not valid! then:
        print('Error tipo NR')
        errors.append('NoResp')  
        raise Error
     
       
except (Error):
    # trial is not valid! then:
    valid_trial.append(0)
        
    # appends conditions for this trial at the end of the conditions vectors, so that it can repeat at the end
    #Stim_conds.append(Stim_conds[trial])
    #Fdbk_conds.append(Fdbk_conds[trial])
  
    # go to next trial
    trial = trial + 1;
    # add 1 to number of trials per block since will have to repeat one
    #N_trials_per_block = N_trials_per_block + 1;

# SAVE DATA FROM TRIAL (VALID OR NOT)
#np.savez_compressed(filename_data, raw=data, stim=stim_time, resp=resp_time, asynch=asynchrony)