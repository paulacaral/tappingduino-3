# -*- coding: utf-8 -*-
"""
Created on Thu Mar 05 11:16:40 2020

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
        file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\2020\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trials.npz")
        #file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/BUGRTACK_S'+subject_number+"*-block"+str(block)+"-trials.npz")    
    else:
        file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\2020\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trial"+str(trial)+".npz")    
    
        #file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/BUGRTACK_S'+subject_number+"*-block"+str(block)+"-trial"+str(trial)+".npz")    
    
    npz = np.load(file_to_load[0])
    if len(asked_data) == 0:
        print("The file contains:")
        return sorted(npz)
    else:
        data_to_return = []
        for a in asked_data:
            data_to_return.append(npz[a])                                
        return data_to_return[:]


#%% Testing Loading_data and plotting asynchronies

asynch = Loading_data('001',1,16,'asynch')
plt.plot(asynch[0],'.-')
plt.xlabel('# beep',fontsize=12)
plt.ylabel('Asynchrony[ms]',fontsize=12)
plt.grid() 


#%% Load asynchronies

# Loads all asynchronies for a subject for an specific block and returns all plots
def Loading_asynch(subject_number,block):
    file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\2020\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trials.npz")
    #file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/BUGRTACK_S'+subject_number+"*-block"+str(block)+"-trials.npz")    
    npz = np.load(file_to_load[0])
    trials = npz['trials']
    
    valid_index = []
    for i in range(len(trials)):
        if trials[i] == 1:
            valid_index.append(i)
    
    for trial in valid_index:
        file_to_load_trial = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\2020\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trial"+str(trial)+".npz")    
        #file_to_load_trial = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/BUGRTACK_S'+subject_number+"*-block"+str(block)+"-trial"+str(trial)+".npz")    
        npz_trial = np.load(file_to_load_trial[0])
        asynch_trial = npz_trial['asynch']
        plt.plot(asynch_trial,'.-', label = 'trial %d' % trial)
    plt.xlabel('# beep',fontsize=12)
    plt.ylabel('Asynchrony[ms]',fontsize=12)
    plt.grid()  
    plt.legend()

    return

#%% Mean value per trial 

def Mean_value_trial(subject_number,block,trial):
    # This function calculates the asynchronies mean value for an specific trial of a condition block of a subject. The first N_transit asynchronies are disregarded.
    N_transit = 40
    min_len_asynch_vector = N_transit + 5
    asynch = Loading_data(subject_number,block,trial,'asynch')
    if len(asynch[0])> min_len_asynch_vector:
        asynch_final = asynch[0][-40:]
        return np.mean(asynch_final)
    else:
        print("Asynch vector is not long enough")

#%% Mean value of mean value of all trials

def Mean_value_meanvaluetrial(subject_number,block):
    # This function calculates the mean value of all trials: takes the mean value of asynchronies for each trial and calculates the mean value between all of them. Will only take into account valid trials
    file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Codigo\2020\DATOS/S'+subject_number+"*-block"+str(block)+"-trials.npz")
    #file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/S'+subject_number+"*-block"+str(block)+"-trials.npz")    
    npz = np.load(file_to_load[0])
    trials = npz['trials']
    
    valid_index = []
    for i in range(len(trials)):
        if trials[i] == 1:
            valid_index.append(i)
    
    mean_value_per_trial = []
    
    for trial in valid_index:
        mean_value_per_trial.append(Mean_value_trial(subject_number,block,trial))
    
    return np.mean(mean_value_per_trial)
    

#%% Find block that has certain condition for each subject

def Find_block(subject_number,stim_cond,resp_cond):
    
    condit_stim = []
    condit_resp = []
    
    for i in range(5):
        conditions = Loading_data(subject_number,i,None,'conditions')
        condit_stim_block = conditions[0][0][2]
        condit_resp_block = conditions[0][0][5]
        condit_stim.append(condit_stim_block)
        condit_resp.append(condit_resp_block)
        
    i = 0;
    while i < len(condit_stim):
        if condit_stim[i] == stim_cond:
           if condit_resp[i] == resp_cond:
               return i
           else:
               i = i+1;
        else:
            i=i+1;

#%% Mean value for a condition for all subjects

def Mean_value_condition(total_number_subjects,stim_cond,resp_cond):
    mean_values_all_subjects = []
    for i in range(1,total_number_subjects):
        subject_block = Find_block('{0:0>3}'.format(i),stim_cond,resp_cond)
        mean_values_all_subjects.append(Mean_value_meanvaluetrial('{0:0>3}'.format(i),subject_block))
        
    return np.mean(mean_values_all_subjects)    
    