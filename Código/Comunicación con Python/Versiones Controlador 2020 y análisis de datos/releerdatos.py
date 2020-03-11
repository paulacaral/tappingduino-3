# -*- coding: utf-8 -*-
"""
Created on Thu Mar 05 15:45:53 2020

@author: Paula
"""
import serial, time
import numpy as np
import matplotlib.pyplot as plt
import random
import os
from itertools import permutations 
import glob
import pickle


#%% Loading data

# Function for loading data specific data from either the block or trial files.
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










class Error(Exception):
   """Base class for other exceptions"""
   pass
#%% Simulo datos

stim_time_not = Loading_data('005',3,6,'stim')
resp_time_not = Loading_data('005',3,6,'resp')
stim_time = stim_time_not[0]
resp_time = resp_time_not[0]
N_stim = len(stim_time)
N_resp = len(resp_time)

#%%
errors = []
valid_trial = []
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
                print(diff)
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
#            trial = trial + 1;
        
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
    print('Hubo un raise error')
    # appends conditions for this trial at the end of the conditions vectors, so that it can repeat at the end
#    Stim_conds.append(Stim_conds[trial])
#    Fdbk_conds.append(Fdbk_conds[trial])
  
    # go to next trial
#    trial = trial + 1;
    # add 1 to number of trials per block since will have to repeat one
#    N_trials_per_block = N_trials_per_block + 1;

# SAVE DATA FROM TRIAL (VALID OR NOT)
#np.savez_compressed(filename_data, raw=data, stim=stim_time, resp=resp_time, asynch=asynchrony)
