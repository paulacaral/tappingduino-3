# -*- coding: utf-8 -*-
"""
Created on Thu Mar 05 11:16:40 2020

@author: Paula
"""


"""
Todas las funciones que se usan para cargar los datos y calcular los valores medios en cada caso (por trial, por condicion para un sujeto, para todos los sujetos, etc.). WARNING: CAMBIE EL DIRECTORIO A DONDE TENGA LOS DATOS EN SU COMPUTADORA. USE LOS DATOS CON LOS TRIALS CORREGIDOS (SIGNOS CORRECTOS Y BIEN CLASIFICADOS POR VÁLIDO O INVÁLIDO).
"""


import numpy as np
import matplotlib.pyplot as plt
import glob


#%% Loading data

# Function for loading data specific data from either the block or trial files.
def Loading_data(subject_number,block, trial, *asked_data):
    # IMPORTANTE: DAR INPUTS COMO STRING
    # Hay que darle si o si numero de sujeto y bloque y el trial puede estar especificado o ser None. Recordar que los archivos que no tienen identificado el trial tienen guardada la informacion de todo el bloque: condicion usada, errores, percepcion del sujeto y si el trial fue valido o invalido. En cambio, al especificar el trial se tiene la informacion de cada trial particular, es decir, asincronias, datos crudos, respuestas y estimulos.

    # Depending on getting "None" or a number for input trial, defines a different filename to load.
    if trial is None:
        file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trials.npz")       
        #file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/BUGRTACK_S'+subject_number+"*-block"+str(block)+"-trials.npz")    
    else:
        file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trial"+str(trial)+".npz")    
       #file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/BUGRTACK_S'+subject_number+"*-block"+str(block)+"-trial"+str(trial)+".npz")    
    
    # Loads the file
    npz = np.load(file_to_load[0])
    # If the wanted data is not specified, the function prints all the data you can ask for in that file chosen. Else, returns the wanted data.
    if len(asked_data) == 0:
        print("The file contains:")
        return sorted(npz)
    else:
        data_to_return = []
        for a in asked_data:
            data_to_return.append(npz[a])                                
        return data_to_return[:]

#%% Testing Loading_data and plotting asynchronies
#plt.figure(figsize=(10,8))
asynch = Loading_data('001',0,0,'asynch')
print(asynch)
#plt.plot(asynch[0],'.-')
#plt.xlabel('# beep',fontsize=12)
#plt.ylabel('Asynchrony[ms]',fontsize=12)
#plt.grid() 
#plt.title('S005, RL, Trial 11')
#plt.savefig('Asynch_S005_RL_T11.png')

#%% Load asynchronies

# Loads all asynchronies for a subject for an specific block and returns all plots for valid trials
def Loading_asynch(subject_number,block):
    file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trials.npz")
    #file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/BUGRTACK_S'+subject_number+"*-block"+str(block)+"-trials.npz")    
   
    # Loads the file
    npz = np.load(file_to_load[0])
    # Will only care for valid trials so first gets all valid trials's indices
    trials = npz['trials']
    valid_index = []
    for i in range(len(trials)):
        if trials[i] == 1:
            valid_index.append(i)
    
    # Only for valid trials loads the file and plots asynchronies
    for trial in valid_index:
        file_to_load_trial = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trial"+str(trial)+".npz")    
        #file_to_load_trial = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/BUGRTACK_S'+subject_number+"*-block"+str(block)+"-trial"+str(trial)+".npz")    
        npz_trial = np.load(file_to_load_trial[0])
        asynch_trial = npz_trial['asynch']
        plt.plot(asynch_trial,'.-', label = 'trial %d' % trial)
    plt.xlabel('# beep',fontsize=12)
    plt.ylabel('Asynchrony[ms]',fontsize=12)
    plt.grid()  
    plt.legend()

    return


#%% Find number block that has certain condition for a subject

def Find_block(subject_number,stim_cond,resp_cond):
    
    # First build a vector with all conditions given to a subject in order (so that each condition is associated to an index). Here range is 5 because we have 5 conditions only.
    condit_stim = []
    condit_resp = []
    for i in range(5):
        conditions = Loading_data(subject_number,i,None,'conditions')
        condit_stim_block = conditions[0][0][2]
        condit_resp_block = conditions[0][0][5]
        condit_stim.append(condit_stim_block)
        condit_resp.append(condit_resp_block)
        
    # Search for the index of the specified condition in the inputs
    i = 0;
    while i < len(condit_stim):
        if condit_stim[i] == stim_cond:
           if condit_resp[i] == resp_cond:
               return i
           else:
               i = i+1;
        else:
            i=i+1;
#%% GRAF 1

# Plots all asynchronies for a subject in a condition given.

def Loading_asynch_cond(subject_number,stim_cond,resp_cond):
    # First finds the block number in which the condition was given to that subject
    block = Find_block(subject_number, stim_cond, resp_cond)
    file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trials.npz")
    #file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/BUGRTACK_S'+subject_number+"*-block"+str(block)+"-trials.npz")    
    
    # Loads the file
    npz = np.load(file_to_load[0])
    
    # Gets trials information for block since we only want valid trials
    trials = npz['trials']
    valid_index = []
    for i in range(len(trials)):
        if trials[i] == 1:
            valid_index.append(i)

    # For valid trials loads its asynchronies and plots them
    plt.figure(figsize=(10,8))
    
    for trial in valid_index:
        file_to_load_trial = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trial"+str(trial)+".npz")    
        #file_to_load_trial = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/BUGRTACK_S'+subject_number+"*-block"+str(block)+"-trial"+str(trial)+".npz")    
        
        npz_trial = np.load(file_to_load_trial[0])
        asynch_trial = npz_trial['asynch']
        plt.plot(asynch_trial,'.-', label = 'trial %d' % trial)
        
        
    plt.xlabel('# beep',fontsize=15)
    plt.ylabel('Asynchrony[ms]',fontsize=15)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid()  
    plt.legend()
    plt.title('Sujeto %s, Condicion %s%s' % (subject_number,stim_cond,resp_cond),fontsize=15)
    #plt.savefig('alltrials_S%s_%s%s.png' % (subject_number,stim_cond,resp_cond))
    return


#%% GRAF 2

# Calculates the mean value for asynchrony in a beepnumber across all trials (for a subject for a condition)

def Mean_across_trials(subject_number,stim_cond,resp_cond):
    # First finds the block number in which the condition was given to that subject
    block = Find_block(subject_number,stim_cond,resp_cond)
    
    # Loads the file
    file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trials.npz")
    #file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/S'+subject_number+"*-block"+str(block)+"-trials.npz")    
    npz = np.load(file_to_load[0])
    
    # Will only work with valid trials so finds their indices
    trials = npz['trials']
    
    valid_index = []
    for i in range(len(trials)):
        if trials[i] == 1:
            valid_index.append(i)
    
    # Won't take all beeps in a trial: gets last 40 beeps assuring it has disregarded at least 5 at the beginning. That's why we need the asynchronies' vector to have a minimum length
    N_transit = 40
    min_len_asynch_vector = N_transit + 5       
    
    # Cuts and checks length on trial vector
    trials_matrix = []
    for trial in valid_index:
        asynch = Loading_data(subject_number,block,trial,'asynch')
        if len(asynch[0])> min_len_asynch_vector:
            asynch_final = asynch[0][-N_transit:]
            trials_matrix.append(asynch_final)
        else:
            print("Asynch vector is not long enough")

    # Define a beep vector just for plotting
    cant_beeps = np.arange(len(trials_matrix[0]))

    # Calculates the mean value for asynchronies for a beep across trials:
    # The vector trials_matrix is a matrix that has dimentions (#beeps per trial)x(#trials) and its elements are the asynchronies for each beep in each trial. To find the mean value for asynchronies across trials we'll get the mean of the "column vector" in the matrix. That means running through the first index (j) first and then the second one (i).
    mean_across_trials = []
    std_across_trials = []
    for i in range(len(trials_matrix[0])):
        column_to_mean = []
        for j in range(len(trials_matrix)):
            column_to_mean.append(trials_matrix[j][i])
        mean_across_trials.append(np.mean(column_to_mean))
        std_across_trials.append(np.std(column_to_mean)/np.sqrt(len(column_to_mean))) 
     
    # Plots the mean value for asynchronies across trials
#    plt.figure(figsize=(10,8))
#    plt.errorbar(cant_beeps,mean_across_trials,std_across_trials,fmt='.-',label='Mean all trials')
#    plt.xlabel('# beep',fontsize=15)
#    plt.ylabel('Asynchrony[ms]',fontsize=15)
#    plt.xticks(fontsize = 15)
#    plt.yticks(fontsize = 15)
#    plt.grid()  
#    plt.legend(fontsize=15)
#    plt.title('Sujeto %s, Condicion %s%s' % (subject_number,stim_cond,resp_cond),fontsize=15)
#    plt.savefig('mean_across_trials_S%s_%s%s.png' % (subject_number,stim_cond,resp_cond))
    
    return mean_across_trials, std_across_trials, cant_beeps


#%% GRAF 2 - Running last function

m1_LL, s1_LL, c = Mean_across_trials('001','L','L')
m2_LL, s2_LL, c = Mean_across_trials('002','L','L')
m3_LL, s3_LL, c = Mean_across_trials('003','L','L')
m4_LL, s4_LL, c = Mean_across_trials('004','L','L')
m5_LL, s5_LL, c = Mean_across_trials('005','L','L')

m1_LL_mean = np.mean(m1_LL)
m2_LL_mean = np.mean(m2_LL)
m3_LL_mean = np.mean(m3_LL)
m4_LL_mean = np.mean(m4_LL)
m5_LL_mean = np.mean(m5_LL)

allmeans_LL = []
allmeans_LL.append(m1_LL_mean)
allmeans_LL.append(m2_LL_mean)
allmeans_LL.append(m3_LL_mean)
allmeans_LL.append(m4_LL_mean)
allmeans_LL.append(m5_LL_mean)

allmeansNS001_LL = []
allmeansNS001_LL.append(m2_LL_mean)
allmeansNS001_LL.append(m3_LL_mean)
allmeansNS001_LL.append(m4_LL_mean)
allmeansNS001_LL.append(m5_LL_mean)

allmeansNS003_LL = []
allmeansNS003_LL.append(m2_LL_mean)
allmeansNS003_LL.append(m1_LL_mean)
allmeansNS003_LL.append(m4_LL_mean)
allmeansNS003_LL.append(m5_LL_mean)

mean_allmeans_LL = np.mean(allmeans_LL)
mean_allmeansNS001_LL = np.mean(allmeansNS001_LL)
mean_allmeansNS003_LL = np.mean(allmeansNS003_LL)


plt.figure(figsize=(10,8))
plt.errorbar(c,m1_LL,s1_LL,fmt='.-',label='S001')
plt.errorbar(c,m2_LL,s2_LL,fmt='.-',label='S002')
plt.errorbar(c,m3_LL,s3_LL,fmt='.-',label='S003')
plt.errorbar(c,m4_LL,s4_LL,fmt='.-',label='S004')
plt.errorbar(c,m5_LL,s5_LL,fmt='.-',label='S005')
plt.hlines(mean_allmeans_LL,0,40,linestyle='solid',color='k', label='Mean all S')
plt.hlines(mean_allmeansNS001_LL,0,40,linestyle='solid',color='blue', label='Mean w/o S001')
plt.hlines(mean_allmeansNS003_LL,0,40,linestyle='solid',color='green',label='Mean w/o S003')
plt.hlines(m1_LL_mean,0,40,linestyle='dashed',color='blue',label='Mean S001')
plt.hlines(m3_LL_mean,0,40,linestyle='dashed',color='green',label='Mean S003')
plt.xlabel('# beep',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=9)
plt.title('Condition LL',fontsize=15)
plt.savefig('mean_across_trials_LL_sinOutliers.png')    


##################################################


m1_RR, s1_RR, c = Mean_across_trials('001','R','R')
m2_RR, s2_RR, c = Mean_across_trials('002','R','R')
m3_RR, s3_RR, c = Mean_across_trials('003','R','R')
m4_RR, s4_RR, c = Mean_across_trials('004','R','R')
m5_RR, s5_RR, c = Mean_across_trials('005','R','R')


m1_RR_mean = np.mean(m1_RR)
m2_RR_mean = np.mean(m2_RR)
m3_RR_mean = np.mean(m3_RR)
m4_RR_mean = np.mean(m4_RR)
m5_RR_mean = np.mean(m5_RR)

allmeans_RR = []
allmeans_RR.append(m1_RR_mean)
allmeans_RR.append(m2_RR_mean)
allmeans_RR.append(m3_RR_mean)
allmeans_RR.append(m4_RR_mean)
allmeans_RR.append(m5_RR_mean)

allmeansNS001_RR = []
allmeansNS001_RR.append(m2_RR_mean)
allmeansNS001_RR.append(m3_RR_mean)
allmeansNS001_RR.append(m4_RR_mean)
allmeansNS001_RR.append(m5_RR_mean)

allmeansNS003_RR = []
allmeansNS003_RR.append(m2_RR_mean)
allmeansNS003_RR.append(m1_RR_mean)
allmeansNS003_RR.append(m4_RR_mean)
allmeansNS003_RR.append(m5_RR_mean)

mean_allmeans_RR = np.mean(allmeans_RR)
mean_allmeansNS001_RR = np.mean(allmeansNS001_RR)
mean_allmeansNS003_RR = np.mean(allmeansNS003_RR)

plt.figure(figsize=(10,8))
plt.errorbar(c,m1_RR,s1_RR,fmt='.-',label='S001')
plt.errorbar(c,m2_RR,s2_RR,fmt='.-',label='S002')
plt.errorbar(c,m3_RR,s3_RR,fmt='.-',label='S003')
plt.errorbar(c,m4_RR,s4_RR,fmt='.-',label='S004')
plt.errorbar(c,m5_RR,s5_RR,fmt='.-',label='S005')
plt.hlines(mean_allmeans_RR,0,40,linestyle='solid',color='k', label='Mean all S')
plt.hlines(mean_allmeansNS001_RR,0,40,linestyle='solid',color='blue', label='Mean w/o S001')
plt.hlines(mean_allmeansNS003_RR,0,40,linestyle='solid',color='green',label='Mean w/o S003')
plt.hlines(m1_RR_mean,0,40,linestyle='dashed',color='blue',label='Mean S001')
plt.hlines(m3_RR_mean,0,40,linestyle='dashed',color='green',label='Mean S003')
plt.xlabel('# beep',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=9)
plt.title('Condition RR',fontsize=15)
plt.savefig('mean_across_trials_RR_sinOutliers.png')  


################################################


m1_BB, s1_BB, c = Mean_across_trials('001','B','B')
m2_BB, s2_BB, c = Mean_across_trials('002','B','B')
m3_BB, s3_BB, c = Mean_across_trials('003','B','B')
m4_BB, s4_BB, c = Mean_across_trials('004','B','B')
m5_BB, s5_BB, c = Mean_across_trials('005','B','B')

m1_BB_mean = np.mean(m1_BB)
m2_BB_mean = np.mean(m2_BB)
m3_BB_mean = np.mean(m3_BB)
m4_BB_mean = np.mean(m4_BB)
m5_BB_mean = np.mean(m5_BB)

allmeans_BB = []
allmeans_BB.append(m1_BB_mean)
allmeans_BB.append(m2_BB_mean)
allmeans_BB.append(m3_BB_mean)
allmeans_BB.append(m4_BB_mean)
allmeans_BB.append(m5_BB_mean)

allmeansNS001_BB = []
allmeansNS001_BB.append(m2_BB_mean)
allmeansNS001_BB.append(m3_BB_mean)
allmeansNS001_BB.append(m4_BB_mean)
allmeansNS001_BB.append(m5_BB_mean)

allmeansNS003_BB = []
allmeansNS003_BB.append(m2_BB_mean)
allmeansNS003_BB.append(m1_BB_mean)
allmeansNS003_BB.append(m4_BB_mean)
allmeansNS003_BB.append(m5_BB_mean)

mean_allmeans_BB = np.mean(allmeans_BB)
mean_allmeansNS001_BB = np.mean(allmeansNS001_BB)
mean_allmeansNS003_BB = np.mean(allmeansNS003_BB)

plt.figure(figsize=(10,8))
plt.errorbar(c,m1_BB,s1_BB,fmt='.-',label='S001')
plt.errorbar(c,m2_BB,s2_BB,fmt='.-',label='S002')
plt.errorbar(c,m3_BB,s3_BB,fmt='.-',label='S003')
plt.errorbar(c,m4_BB,s4_BB,fmt='.-',label='S004')
plt.errorbar(c,m5_BB,s5_BB,fmt='.-',label='S005')
plt.hlines(mean_allmeans_BB,0,40,linestyle='solid',color='k', label='Mean all S')
plt.hlines(mean_allmeansNS001_BB,0,40,linestyle='solid',color='blue', label='Mean w/o S001')
plt.hlines(mean_allmeansNS003_BB,0,40,linestyle='solid',color='green',label='Mean w/o S003')
plt.hlines(m1_BB_mean,0,40,linestyle='dashed',color='blue',label='Mean S001')
plt.hlines(m3_BB_mean,0,40,linestyle='dashed',color='green',label='Mean S003')
plt.xlabel('# beep',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=9)
plt.title('Condition BB',fontsize=15)
plt.savefig('mean_across_trials_BB_sinOutliers.png')  


################################################


m1_RL, s1_RL, c = Mean_across_trials('001','R','L')
m2_RL, s2_RL, c = Mean_across_trials('002','R','L')
m3_RL, s3_RL, c = Mean_across_trials('003','R','L')
m4_RL, s4_RL, c = Mean_across_trials('004','R','L')
m5_RL, s5_RL, c = Mean_across_trials('005','R','L')

m1_RL_mean = np.mean(m1_RL)
m2_RL_mean = np.mean(m2_RL)
m3_RL_mean = np.mean(m3_RL)
m4_RL_mean = np.mean(m4_RL)
m5_RL_mean = np.mean(m5_RL)

allmeans_RL = []
allmeans_RL.append(m1_RL_mean)
allmeans_RL.append(m2_RL_mean)
allmeans_RL.append(m3_RL_mean)
allmeans_RL.append(m4_RL_mean)
allmeans_RL.append(m5_RL_mean)

allmeansNS001_RL = []
allmeansNS001_RL.append(m2_RL_mean)
allmeansNS001_RL.append(m3_RL_mean)
allmeansNS001_RL.append(m4_RL_mean)
allmeansNS001_RL.append(m5_RL_mean)

allmeansNS003_RL = []
allmeansNS003_RL.append(m2_RL_mean)
allmeansNS003_RL.append(m1_RL_mean)
allmeansNS003_RL.append(m4_RL_mean)
allmeansNS003_RL.append(m5_RL_mean)

mean_allmeans_RL = np.mean(allmeans_RL)
mean_allmeansNS001_RL = np.mean(allmeansNS001_RL)
mean_allmeansNS003_RL = np.mean(allmeansNS003_RL)

plt.figure(figsize=(10,8))
plt.errorbar(c,m1_RL,s1_RL,fmt='.-',label='S001')
plt.errorbar(c,m2_RL,s2_RL,fmt='.-',label='S002')
plt.errorbar(c,m3_RL,s3_RL,fmt='.-',label='S003')
plt.errorbar(c,m4_RL,s4_RL,fmt='.-',label='S004')
plt.errorbar(c,m5_RL,s5_RL,fmt='.-',label='S005')
plt.hlines(mean_allmeans_RL,0,40,linestyle='solid',color='k', label='Mean all S')
plt.hlines(mean_allmeansNS001_RL,0,40,linestyle='solid',color='blue', label='Mean w/o S001')
plt.hlines(mean_allmeansNS003_RL,0,40,linestyle='solid',color='green',label='Mean w/o S003')
plt.hlines(m1_RL_mean,0,40,linestyle='dashed',color='blue',label='Mean S001')
plt.hlines(m3_RL_mean,0,40,linestyle='dashed',color='green',label='Mean S003')
plt.xlabel('# beep',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=9)
plt.title('Condition RL',fontsize=15)
plt.savefig('mean_across_trials_RL_sinOutliers.png')  


################################################


m1_LR, s1_LR, c = Mean_across_trials('001','L','R')
m2_LR, s2_LR, c = Mean_across_trials('002','L','R')
m3_LR, s3_LR, c = Mean_across_trials('003','L','R')
m4_LR, s4_LR, c = Mean_across_trials('004','L','R')
m5_LR, s5_LR, c = Mean_across_trials('005','L','R')

m1_LR_mean = np.mean(m1_LR)
m2_LR_mean = np.mean(m2_LR)
m3_LR_mean = np.mean(m3_LR)
m4_LR_mean = np.mean(m4_LR)
m5_LR_mean = np.mean(m5_LR)

allmeans_LR = []
allmeans_LR.append(m1_LR_mean)
allmeans_LR.append(m2_LR_mean)
allmeans_LR.append(m3_LR_mean)
allmeans_LR.append(m4_LR_mean)
allmeans_LR.append(m5_LR_mean)

allmeansNS001_LR = []
allmeansNS001_LR.append(m2_LR_mean)
allmeansNS001_LR.append(m3_LR_mean)
allmeansNS001_LR.append(m4_LR_mean)
allmeansNS001_LR.append(m5_LR_mean)

allmeansNS003_LR = []
allmeansNS003_LR.append(m2_LR_mean)
allmeansNS003_LR.append(m1_LR_mean)
allmeansNS003_LR.append(m4_LR_mean)
allmeansNS003_LR.append(m5_LR_mean)

mean_allmeans_LR = np.mean(allmeans_LR)
mean_allmeansNS001_LR = np.mean(allmeansNS001_LR)
mean_allmeansNS003_LR = np.mean(allmeansNS003_LR)

plt.figure(figsize=(10,8))
plt.errorbar(c,m1_LR,s1_LR,fmt='.-',label='S001')
plt.errorbar(c,m2_LR,s2_LR,fmt='.-',label='S002')
plt.errorbar(c,m3_LR,s3_LR,fmt='.-',label='S003')
plt.errorbar(c,m4_LR,s4_LR,fmt='.-',label='S004')
plt.errorbar(c,m5_LR,s5_LR,fmt='.-',label='S005')
plt.hlines(mean_allmeans_LR,0,40,linestyle='solid',color='k', label='Mean all S')
plt.hlines(mean_allmeansNS001_LR,0,40,linestyle='solid',color='blue', label='Mean w/o S001')
plt.hlines(mean_allmeansNS003_LR,0,40,linestyle='solid',color='green',label='Mean w/o S003')
plt.hlines(m1_LR_mean,0,40,linestyle='dashed',color='blue',label='Mean S001')
plt.hlines(m3_LR_mean,0,40,linestyle='dashed',color='green',label='Mean S003')
plt.xlabel('# beep',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=9)
plt.title('Condition LR',fontsize=15)
plt.savefig('mean_across_trials_LR_sinOutliers.png')  



#%% GRAF 3

# Calculates the mean value for asynchronies in a beep number across subjects (for a condition).

def Mean_across_subjects(total_number_subjects,stim_cond,resp_cond):
    # First builds the "subjects matrix": matrix with (#beeps per trial)x(#subjects) dimention. It uses the last function "Mean_across_trials" to get one only asychronies vector for each subject (for the condition given).
    subjects_matrix = [] 
    for i in range(1,total_number_subjects+1):
        m, s, c = Mean_across_trials('{0:0>3}'.format(i),stim_cond,resp_cond)
        subjects_matrix.append(m)    
     
    # Again we want to calculate the mean value along columns, so the code is the same as before with this new matrix.
    mean_across_subjects = []
    std_across_subjects = []
    for i in range(len(subjects_matrix[0])):
        column_to_mean = []
        for j in range(len(subjects_matrix)):
            column_to_mean.append(subjects_matrix[j][i])
        mean_across_subjects.append(np.mean(column_to_mean))
        std_across_subjects.append(np.std(column_to_mean)/np.sqrt(len(column_to_mean))) 

    
    # Plots the mean value for asynchronies across subjects
#    plt.figure(figsize=(10,8))
#    plt.errorbar(c,mean_across_subjects,std_across_subjects,fmt='.-',label='Mean all subjects')
#    plt.xlabel('# beep',fontsize=15)
#    plt.ylabel('Asynchrony[ms]',fontsize=15)
#    plt.xticks(fontsize = 15)
#    plt.yticks(fontsize = 15)
#    plt.grid()  
#    plt.legend(fontsize=15)
#    plt.title('Condicion %s%s' % (stim_cond,resp_cond),fontsize=15)
#    plt.savefig('mean_across_subjects_WOS001_%s%s.png' % (stim_cond,resp_cond))
#    
    return mean_across_subjects, std_across_subjects, c
    
#%% GRAF 3 - Running the last function

m_LL, s_LL, c = Mean_across_subjects(5,'L','L')
m_RR, s_RR, c = Mean_across_subjects(5,'R','R')
m_BB, s_BB, c = Mean_across_subjects(5,'B','B')
m_RL, s_RL, c = Mean_across_subjects(5,'R','L')
m_LR, s_LR, c = Mean_across_subjects(5,'L','R')

plt.figure(figsize=(10,8))
plt.errorbar(c,m_LL,s_LL,fmt='.-',label='LL')
plt.errorbar(c,m_RR,s_RR,fmt='.-',label='RR')
plt.errorbar(c,m_BB,s_BB,fmt='.-',label='BB')
plt.errorbar(c,m_RL,s_RL,fmt='.-',label='RL')
plt.errorbar(c,m_LR,s_LR,fmt='.-',label='LR')
plt.xlabel('# beep',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('All conditions means across subjects',fontsize=15)
plt.savefig('mean_across_subjects_sinOutliers.png')    
    
     
#%% GRAF 4

# Calculates the mean value for asynchronies along subjects (for all subjects for a condition).

def Mean_along_subjects(total_number_subjects,stim_cond,resp_cond):
    # First builds the "subjects matrix": matrix with (#beeps per trial)x(#subjects) dimention. It uses the last function "Mean_across_trials" to get one only asychronies vector for each subject (for the condition given).
    subjects_matrix = [] 
    for i in range(1,total_number_subjects+1):
        m, s, c = Mean_across_trials('{0:0>3}'.format(i),stim_cond,resp_cond)
        subjects_matrix.append(m)    
     
    # Calculates the mean value now along rows, so we can skip one index in the searching.
    mean_along_subjects = []
    stdn_along_subjects = []
    for i in range(len(subjects_matrix)):
        mean_along_subjects.append(np.mean(subjects_matrix[i]))
        stdn_along_subjects.append(np.std(subjects_matrix[i])/np.sqrt(len(subjects_matrix[i]))) 

    # Plots mean value for asynchronies along trials for a subject for a condition
#    plt.figure(figsize=(10,8))
#    plt.errorbar(c,mean_along_subjects,stdn_along_subjects,fmt='.-',label='Mean all subjects')
#    plt.xlabel('# beep',fontsize=15)
#    plt.ylabel('Asynchrony[ms]',fontsize=15)
#    plt.xticks(fontsize = 15)
#    plt.yticks(fontsize = 15)
#    plt.grid()  
#    plt.legend(fontsize=15)
#    plt.title('Condicion %s%s' % (stim_cond,resp_cond),fontsize=15)
#    plt.savefig('mean_along_subjects_%s%s.png' % (stim_cond,resp_cond))
    
    return mean_along_subjects, stdn_along_subjects, c


#%% GRAF 4 - Running last function

m_LL, s_LL, c = Mean_along_subjects(5,'L','L')
m_RR, s_RR, c = Mean_along_subjects(5,'R','R')
m_BB, s_BB, c = Mean_along_subjects(5,'B','B')
m_RL, s_RL, c = Mean_along_subjects(5,'R','L')
m_LR, s_LR, c = Mean_along_subjects(5,'L','R')


# Reacomodo para tener un vector por sujeto y no uno por condicion
mS1 = []
mS2 = []
mS3 = []
mS4 = []
mS5 = []

mS1.append(m_LL[0])
mS1.append(m_RR[0])
mS1.append(m_BB[0])
mS1.append(m_RL[0])
mS1.append(m_LR[0])

mS2.append(m_LL[1])
mS2.append(m_RR[1])
mS2.append(m_BB[1])
mS2.append(m_RL[1])
mS2.append(m_LR[1])

mS3.append(m_LL[2])
mS3.append(m_RR[2])
mS3.append(m_BB[2])
mS3.append(m_RL[2])
mS3.append(m_LR[2])

mS4.append(m_LL[3])
mS4.append(m_RR[3])
mS4.append(m_BB[3])
mS4.append(m_RL[3])
mS4.append(m_LR[3])

mS5.append(m_LL[4])
mS5.append(m_RR[4])
mS5.append(m_BB[4])
mS5.append(m_RL[4])
mS5.append(m_LR[4])

# Idem con std
sS1 = []
sS2 = []
sS3 = []
sS4 = []
sS5 = []

sS1.append(s_LL[0])
sS1.append(s_RR[0])
sS1.append(s_BB[0])
sS1.append(s_RL[0])
sS1.append(s_LR[0])

sS2.append(s_LL[1])
sS2.append(s_RR[1])
sS2.append(s_BB[1])
sS2.append(s_RL[1])
sS2.append(s_LR[1])

sS3.append(s_LL[2])
sS3.append(s_RR[2])
sS3.append(s_BB[2])
sS3.append(s_RL[2])
sS3.append(s_LR[2])

sS4.append(s_LL[3])
sS4.append(s_RR[3])
sS4.append(s_BB[3])
sS4.append(s_RL[3])
sS4.append(s_LR[3])

sS5.append(s_LL[4])
sS5.append(s_RR[4])
sS5.append(s_BB[4])
sS5.append(s_RL[4])
sS5.append(s_LR[4])


# Calculo el promedio para cada condición y lo guardo en un vector aparte para graficarlo
mean_m_LL = np.mean(m_LL)
mean_m_RR = np.mean(m_RR)
mean_m_BB = np.mean(m_BB)
mean_m_RL = np.mean(m_RL)
mean_m_LR = np.mean(m_LR)

mean_m = []
mean_m.append(mean_m_LL)
mean_m.append(mean_m_RR)
mean_m.append(mean_m_BB)
mean_m.append(mean_m_RL)
mean_m.append(mean_m_LR)


# Eje x
CC = np.arange(5)

# Hago el plot
plt.figure(figsize=(10,8))
plt.errorbar(CC,mS1,sS1,fmt='.-',label='S001')
plt.errorbar(CC,mS2,sS2,fmt='.-',label='S002')
plt.errorbar(CC,mS3,sS3,fmt='.-',label='S003')
plt.errorbar(CC,mS4,sS4,fmt='.-',label='S004')
plt.errorbar(CC,mS5,sS5,fmt='.-',label='S005')
plt.plot(CC,mean_m,'*',markersize=15)
plt.xlabel('Condiciones ',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
labels = ['LL', 'RR', 'BB','RL','LR']
plt.xticks(CC,labels, fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('All conditions means along trials for all subjects')
#plt.savefig('mean_along_subjects_CCxAxis_sinOutliers.png')



#%% Finding trials outliers

def Trials_outliers(subject_number,stim_cond,resp_cond):
    # First finds the block number in which the condition was given to that subject
    block = Find_block(subject_number, stim_cond, resp_cond)
    file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trials.npz")
    #file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/BUGRTACK_S'+subject_number+"*-block"+str(block)+"-trials.npz")    
    
    # Loads the file
    npz = np.load(file_to_load[0])
    
    # Gets trials information for block since we only want valid trials
    trials = npz['trials']
    valid_index = []
    for i in range(len(trials)):
        if trials[i] == 1:
            valid_index.append(i)

    for trial in valid_index:        
         # Won't take all beeps in a trial: gets last 40 beeps assuring it has disregarded at least 5 at the beginning. That's why we need the asynchronies' vector to have a minimum length
        N_transit = 40
        min_len_asynch_vector = N_transit + 5       
    
        # Cuts and checks length on trial vector
        asynch = Loading_data(subject_number,block,trial,'asynch')
        if len(asynch[0])> min_len_asynch_vector:
            asynch_trial = asynch[0][-N_transit:]
        else:
            print("Asynch vector is not long enough")      
        
        # Calculates trial mean asynchrony
        trial_mean = np.mean(asynch_trial)
        dif_vector = []
        for k in range(len(asynch_trial)):
            dif_vector.append(abs(trial_mean-asynch_trial[k]))
        threshold = 110;
        if max(dif_vector)> threshold:
            print('El trial %i de la condicion %s%s(B%i) del sujeto S%s es outlier' % (trial,stim_cond,resp_cond,block,subject_number))
#            plt.figure()
#            plt.plot(asynch_trial,'.-', label = 'trial %d' % trial)
#            plt.hlines(trial_mean,0,40,color='k',linestyle='solid',label='mean asynchrony')
#            plt.hlines(trial_mean-threshold,0,40,color='gray',linestyle='dashed')
#            plt.hlines(trial_mean+threshold,0,40,color='gray',linestyle='dashed')
#            plt.xlabel('# beep',fontsize=15)
#            plt.ylabel('Asynchrony[ms]',fontsize=15)
#            plt.xticks(fontsize = 15)
#            plt.yticks(fontsize = 15)
#            plt.grid()  
#            plt.legend()
#            plt.title('Sujeto %s, Condicion %s%s' % (subject_number,stim_cond,resp_cond),fontsize=15)
#
#            plt.savefig('trials_outliers_S%s_%s%s_Trial%i.png' % (subject_number,stim_cond,resp_cond,trial))
#                    
            
        
    return 

#%% Running last function for all subjects for all conditions

total_number_subjects = 5

for i in range(1,total_number_subjects+1):
    Trials_outliers('{0:0>3}'.format(i),'B','B')
    Trials_outliers('{0:0>3}'.format(i),'R','R')
    Trials_outliers('{0:0>3}'.format(i),'L','L')
    Trials_outliers('{0:0>3}'.format(i),'R','L')
    Trials_outliers('{0:0>3}'.format(i),'L','R')
    
    
#%% GRAFICOS 5 Y 6, PASO 1


# Calculates mean value along trials

def Mean_along_trials(subject_number, stim_cond, resp_cond):
     # First finds the block number in which the condition was given to that subject
    block = Find_block(subject_number,stim_cond,resp_cond)
    
    # Loads the file
    file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trials.npz")
    #file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/S'+subject_number+"*-block"+str(block)+"-trials.npz")    
    npz = np.load(file_to_load[0])
    
    # Will only work with valid trials so finds their indices
    trials = npz['trials']
    
    valid_index = []
    for i in range(len(trials)):
        if trials[i] == 1:
            valid_index.append(i)
    
    # Won't take all beeps in a trial: gets last 40 beeps assuring it has disregarded at least 5 at the beginning. That's why we need the asynchronies' vector to have a minimum length
    N_transit = 40
    min_len_asynch_vector = N_transit + 5       
    
    # Cuts and checks length on trial vector
    trials_matrix = []
    for trial in valid_index:
        asynch = Loading_data(subject_number,block,trial,'asynch')
        if len(asynch[0])> min_len_asynch_vector:
            asynch_final = asynch[0][-N_transit:]
            trials_matrix.append(asynch_final)
        else:
            print("Asynch vector is not long enough")

    # Calculates the mean value for asynchronies along trials:
    # The vector trials_matrix is a matrix that has dimentions (#beeps per trial)x(#trials) and its elements are the asynchronies for each beep in each trial. To find the mean value for asynchronies along trials we'll get the mean of the "row vector" in the matrix. That means running through the first index (j) first and then the second one (i).
    mean_along_trials = []
    std_along_trials = []
    for j in range(len(trials_matrix)):
        mean_along_trials.append(np.mean(trials_matrix[j]))
        std_along_trials.append(np.std(trials_matrix[j])/np.sqrt(len(trials_matrix[j]))) 

    return mean_along_trials, std_along_trials


#%% GRAFICOS 5 Y 6, PASO 2

def Mean_across_meantrials(subject_number,stim_cond,resp_cond):
    mean_along_trials, std_along_trials = Mean_along_trials(subject_number, stim_cond,resp_cond)
    
    mean_mean = np.mean(mean_along_trials)
    mean_std = np.std(mean_along_trials)/np.sqrt(len(mean_along_trials))
    std_mean = np.mean(std_along_trials)
    std_std = np.std(std_along_trials)/np.sqrt(len(std_along_trials))
    
    return mean_mean, mean_std, std_mean, std_std

#%% GRAFICOS 5 Y 6, PASO 2 bis
# Running last function for all conditions for all subjects. Builds a vector for each subject where each element is the mean for each condition.

Condition_vector= [['L','L'],['B','B'],['R','R'],['L','R'],['R','L']] 

# Create empty vectors for mean and std for all subjects
total_number_subjects = 5    
for i in range(1,total_number_subjects+1):
#for i in range(1,3) + range(4,total_number_subjects+1):   
    globals()['mean_S%s' % '{0:0>3}'.format(i)] = []
    globals()['mean_S%s_err' % '{0:0>3}'.format(i)] = []
    globals()['std_S%s' % '{0:0>3}'.format(i)] = []
    globals()['std_S%s_err' % '{0:0>3}'.format(i)] = []

#for i in range(2,total_number_subjects+1):
for i in range(1,3) + range(4,total_number_subjects+1):   
    for cond_pair in Condition_vector:
        eval('mean_S'+'{0:0>3}'.format(i)).append(Mean_across_meantrials('{0:0>3}'.format(i),cond_pair[0],cond_pair[1])[0])
        eval('mean_S'+'{0:0>3}'.format(i)+'_err').append(Mean_across_meantrials('{0:0>3}'.format(i),cond_pair[0],cond_pair[1])[1])
        eval('std_S'+'{0:0>3}'.format(i)).append(Mean_across_meantrials('{0:0>3}'.format(i),cond_pair[0],cond_pair[1])[2])
        eval('std_S'+'{0:0>3}'.format(i)+'_err').append(Mean_across_meantrials('{0:0>3}'.format(i),cond_pair[0],cond_pair[1])[3])

#%% GRAFICOS 5 Y 6, PASO 3

# Calculates mean across subjects for the vectors just created. Builds a vector with the result of mean and std for each condition.

#asyn_mean_ave_percond = []
#asyn_mean_err_percond = []
#asyn_std_ave_percond = []
#asyn_std_err_percond = []

#asyn_mean_ave_percond_NS001 = []
#asyn_mean_err_percond_NS001 = []
#asyn_std_ave_percond_NS001 = []
#asyn_std_err_percond_NS001 = []

asyn_mean_ave_percond_NS003 = []
asyn_mean_err_percond_NS003 = []
asyn_std_ave_percond_NS003 = []
asyn_std_err_percond_NS003 = []

for i in range(len(Condition_vector)):
    column_to_mean_mean = []
    column_to_mean_std = []
    for j in range(1,3) + range(4,total_number_subjects+1):   
#    for j in range(2,total_number_subjects+1):
        column_to_mean_mean.append(eval('mean_S'+'{0:0>3}'.format(j))[i])
        column_to_mean_std.append(eval('std_S'+'{0:0>3}'.format(j))[i])
    asyn_mean_ave_percond_NS003.append(np.mean(column_to_mean_mean))
    asyn_mean_err_percond_NS003.append(np.std(column_to_mean_mean)/np.sqrt(len(column_to_mean_mean)))
    asyn_std_ave_percond_NS003.append(np.mean(column_to_mean_std))
    asyn_std_err_percond_NS003.append(np.std(column_to_mean_std)/np.sqrt(len(column_to_mean_std)))
#%% GRAFICOS 5 Y 6, PLOTEO
# Eje x
CC = np.arange(5)

plt.figure(figsize=(10,8))
plt.errorbar(CC,asyn_mean_ave_percond,asyn_mean_err_percond,color='k',fmt='*-',label='Mean sobre todos los sujetos')
plt.errorbar(CC,asyn_mean_ave_percond_NS001,asyn_mean_err_percond_NS001,fmt='*-',label='Mean sin S001')
plt.errorbar(CC,asyn_mean_ave_percond_NS003,asyn_mean_err_percond_NS003,color='green',fmt='*-',label='Mean sin S003')
plt.xlabel('Condiciones ',fontsize=15)
plt.ylabel('Mean asynchrony[ms]',fontsize=15)
labels = ['LL', 'RR', 'BB','RL','LR']
plt.xticks(CC,labels, fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('asyn_mean_ave_percond')
plt.savefig('asyn_mean_ave_percond_sinOutliers.png')


plt.figure(figsize=(10,8))
plt.errorbar(CC,asyn_std_ave_percond,asyn_std_err_percond,color='k',fmt='*-',label='Std sobre todos los sujetos')
plt.errorbar(CC,asyn_std_ave_percond_NS001,asyn_std_err_percond_NS001,fmt='*-',label='Std sin S001')
plt.errorbar(CC,asyn_std_ave_percond_NS003,asyn_std_err_percond_NS003,color='green',fmt='*-',label='Std sin S003')
plt.xlabel('Condiciones ',fontsize=15)
plt.ylabel('Asynchrony s standard deviation[ms]',fontsize=15)
labels = ['LL', 'BB', 'RR','LR','RL']
plt.xticks(CC,labels, fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('asyn_std_ave_percond')
plt.savefig('asyn_std_ave_percond_sinOutliers.png')


#%% GRAFICOS 7 Y 8, PLOTEO

# Eje x
CC = np.arange(5)

plt.figure(figsize=(10,8))
plt.errorbar(CC,mean_S001,mean_S001_err,fmt='*-',label='S001')
plt.errorbar(CC,mean_S002,mean_S002_err,fmt='*-',label='S002')
plt.errorbar(CC,mean_S003,mean_S003_err,fmt='*-',label='S003')
plt.errorbar(CC,mean_S004,mean_S004_err,fmt='*-',label='S004')
plt.errorbar(CC,mean_S005,mean_S005_err,fmt='*-',label='S005')
plt.xlabel('Condiciones ',fontsize=15)
plt.ylabel('Mean asynchrony[ms]',fontsize=15)
labels = ['LL', 'RR', 'BB','RL','LR']
plt.xticks(CC,labels, fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('asyn_mean_eachSubj')
plt.savefig('asyn_mean_eachSubj.png')


plt.figure(figsize=(10,8))
plt.errorbar(CC,std_S001,std_S001_err,fmt='*-',label='S001')
plt.errorbar(CC,std_S002,std_S002_err,fmt='*-',label='S002')
plt.errorbar(CC,std_S003,std_S003_err,fmt='*-',label='S003')
plt.errorbar(CC,std_S004,std_S004_err,fmt='*-',label='S004')
plt.errorbar(CC,std_S005,std_S005_err,fmt='*-',label='S005')
plt.xlabel('Condiciones ',fontsize=15)
plt.ylabel('Asynchrony standard deviation[ms]',fontsize=15)
labels = ['LL', 'RR', 'BB','RL','LR']
plt.xticks(CC,labels, fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('asyn_std_eachSubj')
plt.savefig('asyn_std_eachSubj.png')



