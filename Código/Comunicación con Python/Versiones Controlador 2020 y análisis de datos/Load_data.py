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

asynch = Loading_data('001',1,16,'asynch')
plt.plot(asynch[0],'.-')
plt.xlabel('# beep',fontsize=12)
plt.ylabel('Asynchrony[ms]',fontsize=12)
plt.grid() 


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
    #plt.legend()
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
        std_across_trials.append(np.std(column_to_mean)) 
    
    # Making std error into sterr.
    std_across_trials = std_across_trials/np.sqrt(len(std_across_trials))
     
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
m5_LL, s5_LL, c = Mean_across_trials('004','L','L')


plt.figure(figsize=(10,8))
plt.errorbar(c,m1_LL,s1_LL,fmt='.-',label='S001')
plt.errorbar(c,m2_LL,s2_LL,fmt='.-',label='S002')
plt.errorbar(c,m3_LL,s3_LL,fmt='.-',label='S003')
plt.errorbar(c,m4_LL,s4_LL,fmt='.-',label='S004')
plt.errorbar(c,m5_LL,s5_LL,fmt='.-',label='S005')
plt.xlabel('# beep',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('Condition LL',fontsize=15)
plt.savefig('mean_across_trials_LL.png')    


##################################################


m1_RR, s1_RR, c = Mean_across_trials('001','R','R')
m2_RR, s2_RR, c = Mean_across_trials('002','R','R')
m3_RR, s3_RR, c = Mean_across_trials('003','R','R')
m4_RR, s4_RR, c = Mean_across_trials('004','R','R')
m5_RR, s5_RR, c = Mean_across_trials('004','R','R')


plt.figure(figsize=(10,8))
plt.errorbar(c,m1_RR,s1_RR,fmt='.-',label='S001')
plt.errorbar(c,m2_RR,s2_RR,fmt='.-',label='S002')
plt.errorbar(c,m3_RR,s3_RR,fmt='.-',label='S003')
plt.errorbar(c,m4_RR,s4_RR,fmt='.-',label='S004')
plt.errorbar(c,m5_RR,s5_RR,fmt='.-',label='S005')
plt.xlabel('# beep',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('Condition RR',fontsize=15)
plt.savefig('mean_across_trials_RR.png')  


################################################


m1_BB, s1_BB, c = Mean_across_trials('001','B','B')
m2_BB, s2_BB, c = Mean_across_trials('002','B','B')
m3_BB, s3_BB, c = Mean_across_trials('003','B','B')
m4_BB, s4_BB, c = Mean_across_trials('004','B','B')
m5_BB, s5_BB, c = Mean_across_trials('004','B','B')


plt.figure(figsize=(10,8))
plt.errorbar(c,m1_BB,s1_BB,fmt='.-',label='S001')
plt.errorbar(c,m2_BB,s2_BB,fmt='.-',label='S002')
plt.errorbar(c,m3_BB,s3_BB,fmt='.-',label='S003')
plt.errorbar(c,m4_BB,s4_BB,fmt='.-',label='S004')
plt.errorbar(c,m5_BB,s5_BB,fmt='.-',label='S005')
plt.xlabel('# beep',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('Condition BB',fontsize=15)
plt.savefig('mean_across_trials_BB.png')  


################################################


m1_RL, s1_RL, c = Mean_across_trials('001','R','L')
m2_RL, s2_RL, c = Mean_across_trials('002','R','L')
m3_RL, s3_RL, c = Mean_across_trials('003','R','L')
m4_RL, s4_RL, c = Mean_across_trials('004','R','L')
m5_RL, s5_RL, c = Mean_across_trials('004','R','L')


plt.figure(figsize=(10,8))
plt.errorbar(c,m1_RL,s1_RL,fmt='.-',label='S001')
plt.errorbar(c,m2_RL,s2_RL,fmt='.-',label='S002')
plt.errorbar(c,m3_RL,s3_RL,fmt='.-',label='S003')
plt.errorbar(c,m4_RL,s4_RL,fmt='.-',label='S004')
plt.errorbar(c,m5_RL,s5_RL,fmt='.-',label='S005')
plt.xlabel('# beep',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('Condition RL',fontsize=15)
plt.savefig('mean_across_trials_RL.png')  


################################################


m1_LR, s1_LR, c = Mean_across_trials('001','L','R')
m2_LR, s2_LR, c = Mean_across_trials('002','L','R')
m3_LR, s3_LR, c = Mean_across_trials('003','L','R')
m4_LR, s4_LR, c = Mean_across_trials('004','L','R')
m5_LR, s5_LR, c = Mean_across_trials('004','L','R')


plt.figure(figsize=(10,8))
plt.errorbar(c,m1_LR,s1_LR,fmt='.-',label='S001')
plt.errorbar(c,m2_LR,s2_LR,fmt='.-',label='S002')
plt.errorbar(c,m3_LR,s3_LR,fmt='.-',label='S003')
plt.errorbar(c,m4_LR,s4_LR,fmt='.-',label='S004')
plt.errorbar(c,m5_LR,s5_LR,fmt='.-',label='S005')
plt.xlabel('# beep',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('Condition LR',fontsize=15)
plt.savefig('mean_across_trials_LR.png')  



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
        std_across_subjects.append(np.std(column_to_mean)) 

    # Making std error into sterr.    
    std_across_subjects = std_across_subjects/np.sqrt(len(std_across_subjects))
    
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
#    plt.savefig('mean_across_subjects_%s%s.png' % (stim_cond,resp_cond))
    
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
plt.savefig('mean_across_subjects.png')    
    
     
#%% GRAF 4

# Calculates the mean value for asynchronies along trials (for all subjects for a condition).

def Mean_along_trials(total_number_subjects,stim_cond,resp_cond):
    # First builds the "subjects matrix": matrix with (#beeps per trial)x(#subjects) dimention. It uses the last function "Mean_across_trials" to get one only asychronies vector for each subject (for the condition given).
    subjects_matrix = [] 
    for i in range(1,total_number_subjects+1):
        m, s, c = Mean_across_trials('{0:0>3}'.format(i),stim_cond,resp_cond)
        subjects_matrix.append(m)    
     
    # Calculates the mean value now along rows, so we can skip one index in the searching.
    mean_along_trials = []
    std_along_trials = []
    for i in range(len(subjects_matrix)):
        mean_along_trials.append(np.mean(subjects_matrix[i]))
        std_along_trials.append(np.std(subjects_matrix[i])) 
    # Making std error into sterr.      
    std_along_trials = std_along_trials/np.sqrt(len(std_along_trials))

    # Plots mean value for asynchronies along trials for a subject for a condition
#    plt.figure(figsize=(10,8))
#    plt.errorbar(c,mean_along_trials,std_along_trials,fmt='.-',label='Mean all subjects')
#    plt.xlabel('# beep',fontsize=15)
#    plt.ylabel('Asynchrony[ms]',fontsize=15)
#    plt.xticks(fontsize = 15)
#    plt.yticks(fontsize = 15)
#    plt.grid()  
#    plt.legend(fontsize=15)
#    plt.title('Condicion %s%s' % (stim_cond,resp_cond),fontsize=15)
#    plt.savefig('mean_along_trials_%s%s.png' % (stim_cond,resp_cond))
    
    return mean_along_trials, std_along_trials, c


#%% GRAF 4 - Running last function

m_LL, s_LL, c = Mean_along_trials(5,'L','L')
m_RR, s_RR, c = Mean_along_trials(5,'R','R')
m_BB, s_BB, c = Mean_along_trials(5,'B','B')
m_RL, s_RL, c = Mean_along_trials(5,'R','L')
m_LR, s_LR, c = Mean_along_trials(5,'L','R')

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

sS1 = []
sS2 = []
sS3 = []
sS4 = []
sS5 = []

sS1.append(m_LL[0])
sS1.append(m_RR[0])
sS1.append(m_BB[0])
sS1.append(m_RL[0])
sS1.append(m_LR[0])

sS2.append(m_LL[1])
sS2.append(m_RR[1])
sS2.append(m_BB[1])
sS2.append(m_RL[1])
sS2.append(m_LR[1])

sS3.append(m_LL[2])
sS3.append(m_RR[2])
sS3.append(m_BB[2])
sS3.append(m_RL[2])
sS3.append(m_LR[2])

sS4.append(m_LL[3])
sS4.append(m_RR[3])
sS4.append(m_BB[3])
sS4.append(m_RL[3])
sS4.append(m_LR[3])

sS5.append(m_LL[4])
sS5.append(m_RR[4])
sS5.append(m_BB[4])
sS5.append(m_RL[4])
sS5.append(m_LR[4])

CC = np.arange(5)

plt.figure(figsize=(10,8))
plt.errorbar(CC,mS1,sS1,fmt='.-',label='S001')
plt.errorbar(CC,mS2,sS2,fmt='.-',label='S002')
plt.errorbar(CC,mS3,sS3,fmt='.-',label='S003')
plt.errorbar(CC,mS4,sS4,fmt='.-',label='S004')
plt.errorbar(CC,mS5,sS5,fmt='.-',label='S005')
plt.xlabel('Condiciones ',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
labels = ['LL', 'RR', 'BB','RL','LR']
plt.xticks(CC,labels, fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('All conditions means along trials for all subjects')
plt.savefig('mean_along_trials_CCxAxis.png')
