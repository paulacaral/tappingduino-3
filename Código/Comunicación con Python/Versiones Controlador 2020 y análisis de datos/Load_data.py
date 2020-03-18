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

    if trial is None:
        file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trials.npz")
        #file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/BUGRTACK_S'+subject_number+"*-block"+str(block)+"-trials.npz")    
    else:
        file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trial"+str(trial)+".npz")    
    
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

# Loads all asynchronies for a subject for an specific block and returns all plots for valid trials
def Loading_asynch(subject_number,block):
    file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trials.npz")
    #file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/BUGRTACK_S'+subject_number+"*-block"+str(block)+"-trials.npz")    
    npz = np.load(file_to_load[0])
    trials = npz['trials']
    
    valid_index = []
    for i in range(len(trials)):
        if trials[i] == 1:
            valid_index.append(i)
    
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
#%% Find number block that has certain condition for each subject

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
#%% GRAF 1
def Loading_asynch_cond(subject_number,stim_cond,resp_cond):
    block = Find_block(subject_number, stim_cond, resp_cond)
    file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trials.npz")
    #file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/BUGRTACK_S'+subject_number+"*-block"+str(block)+"-trials.npz")    
    npz = np.load(file_to_load[0])
    trials = npz['trials']
    
    valid_index = []
    for i in range(len(trials)):
        if trials[i] == 1:
            valid_index.append(i)

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
    plt.savefig('alltrials_S%s_%s%s.png' % (subject_number,stim_cond,resp_cond))
    return


#%% GRAF 2

def Mean_value_beep(subject_number,stim_cond,resp_cond):
    
    block = Find_block(subject_number,stim_cond,resp_cond)
    N_transit = 40
    min_len_asynch_vector = N_transit + 5
    
    file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trials.npz")
    #file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/S'+subject_number+"*-block"+str(block)+"-trials.npz")    
    npz = np.load(file_to_load[0])
    trials = npz['trials']
    
    valid_index = []
    for i in range(len(trials)):
        if trials[i] == 1:
            valid_index.append(i)
    
    alltrials = []
    for trial in valid_index:
        asynch = Loading_data(subject_number,block,trial,'asynch')
        if len(asynch[0])> min_len_asynch_vector:
            asynch_final = asynch[0][-N_transit:]
            alltrials.append(asynch_final)
        else:
            print("Asynch vector is not long enough")

    cant_beeps = np.arange(len(alltrials[0]))

    mean_values_all_beeps = []
    std_all_beeps = []
    for i in range(len(alltrials[0])):
        mean_value_beep = []
        for j in range(len(alltrials)):
            mean_value_beep.append(alltrials[j][i])
        mean_values_all_beeps.append(np.mean(mean_value_beep))
        std_all_beeps.append(np.std(mean_value_beep)) 
    
#    plt.figure(figsize=(10,8))
#    plt.errorbar(cant_beeps,mean_values_all_beeps,std_all_beeps,fmt='.',label='Mean all trials')
#    plt.xlabel('# beep',fontsize=15)
#    plt.ylabel('Asynchrony[ms]',fontsize=15)
#    plt.xticks(fontsize = 15)
#    plt.yticks(fontsize = 15)
#    plt.grid()  
#    plt.legend(fontsize=15)
#    plt.title('Sujeto %s, Condicion %s%s' % (subject_number,stim_cond,resp_cond),fontsize=15)
#    plt.savefig('mean_trials_beep_S%s_%s%s.png' % (subject_number,stim_cond,resp_cond))
    
    return mean_values_all_beeps, std_all_beeps, cant_beeps


#%% GRAF 2

m1_LL, s1_LL, c = Mean_value_beep('001','L','L')
m2_LL, s2_LL, c = Mean_value_beep('002','L','L')
m3_LL, s3_LL, c = Mean_value_beep('003','L','L')
m4_LL, s4_LL, c = Mean_value_beep('004','L','L')
m5_LL, s5_LL, c = Mean_value_beep('004','L','L')


plt.figure(figsize=(10,8))
plt.errorbar(c,m1_LL,s1_LL,fmt='.',label='S001')
plt.errorbar(c,m2_LL,s2_LL,fmt='.',label='S002')
plt.errorbar(c,m3_LL,s3_LL,fmt='.',label='S003')
plt.errorbar(c,m4_LL,s4_LL,fmt='.',label='S004')
plt.errorbar(c,m5_LL,s5_LL,fmt='.',label='S005')
plt.xlabel('# beep',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('Condition LL',fontsize=15)
plt.savefig('CondLL_allsubjects.png')    


##################################################


m1_RR, s1_RR, c = Mean_value_beep('001','R','R')
m2_RR, s2_RR, c = Mean_value_beep('002','R','R')
m3_RR, s3_RR, c = Mean_value_beep('003','R','R')
m4_RR, s4_RR, c = Mean_value_beep('004','R','R')
m5_RR, s5_RR, c = Mean_value_beep('004','R','R')


plt.figure(figsize=(10,8))
plt.errorbar(c,m1_RR,s1_RR,fmt='.',label='S001')
plt.errorbar(c,m2_RR,s2_RR,fmt='.',label='S002')
plt.errorbar(c,m3_RR,s3_RR,fmt='.',label='S003')
plt.errorbar(c,m4_RR,s4_RR,fmt='.',label='S004')
plt.errorbar(c,m5_RR,s5_RR,fmt='.',label='S005')
plt.xlabel('# beep',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('Condition RR',fontsize=15)
plt.savefig('CondRR_allsubjects.png')  


################################################


m1_BB, s1_BB, c = Mean_value_beep('001','B','B')
m2_BB, s2_BB, c = Mean_value_beep('002','B','B')
m3_BB, s3_BB, c = Mean_value_beep('003','B','B')
m4_BB, s4_BB, c = Mean_value_beep('004','B','B')
m5_BB, s5_BB, c = Mean_value_beep('004','B','B')


plt.figure(figsize=(10,8))
plt.errorbar(c,m1_BB,s1_BB,fmt='.',label='S001')
plt.errorbar(c,m2_BB,s2_BB,fmt='.',label='S002')
plt.errorbar(c,m3_BB,s3_BB,fmt='.',label='S003')
plt.errorbar(c,m4_BB,s4_BB,fmt='.',label='S004')
plt.errorbar(c,m5_BB,s5_BB,fmt='.',label='S005')
plt.xlabel('# beep',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('Condition BB',fontsize=15)
plt.savefig('CondBB_allsubjects.png')  


################################################


m1_RL, s1_RL, c = Mean_value_beep('001','R','L')
m2_RL, s2_RL, c = Mean_value_beep('002','R','L')
m3_RL, s3_RL, c = Mean_value_beep('003','R','L')
m4_RL, s4_RL, c = Mean_value_beep('004','R','L')
m5_RL, s5_RL, c = Mean_value_beep('004','R','L')


plt.figure(figsize=(10,8))
plt.errorbar(c,m1_RL,s1_RL,fmt='.',label='S001')
plt.errorbar(c,m2_RL,s2_RL,fmt='.',label='S002')
plt.errorbar(c,m3_RL,s3_RL,fmt='.',label='S003')
plt.errorbar(c,m4_RL,s4_RL,fmt='.',label='S004')
plt.errorbar(c,m5_RL,s5_RL,fmt='.',label='S005')
plt.xlabel('# beep',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('Condition RL',fontsize=15)
plt.savefig('CondRL_allsubjects.png')  


################################################


m1_LR, s1_LR, c = Mean_value_beep('001','L','R')
m2_LR, s2_LR, c = Mean_value_beep('002','L','R')
m3_LR, s3_LR, c = Mean_value_beep('003','L','R')
m4_LR, s4_LR, c = Mean_value_beep('004','L','R')
m5_LR, s5_LR, c = Mean_value_beep('004','L','R')


plt.figure(figsize=(10,8))
plt.errorbar(c,m1_LR,s1_LR,fmt='.',label='S001')
plt.errorbar(c,m2_LR,s2_LR,fmt='.',label='S002')
plt.errorbar(c,m3_LR,s3_LR,fmt='.',label='S003')
plt.errorbar(c,m4_LR,s4_LR,fmt='.',label='S004')
plt.errorbar(c,m5_LR,s5_LR,fmt='.',label='S005')
plt.xlabel('# beep',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('Condition LR',fontsize=15)
plt.savefig('CondLR_allsubjects.png')  



#%% GRAF 3

def Mean_subjects_per_cond(total_number_subjects,stim_cond,resp_cond):
    
    mean_all_subjects_matrix = [] 
    for i in range(1,total_number_subjects+1):
        m, s, c = Mean_value_beep('{0:0>3}'.format(i),stim_cond,resp_cond)
        mean_all_subjects_matrix.append(m)    
     
    mean_all_subjects = []
    std_all_subjects = []
    for i in range(len(mean_all_subjects_matrix[0])):
        column_to_mean = []
        for j in range(len(mean_all_subjects_matrix)):
            column_to_mean.append(mean_all_subjects_matrix[j][i])
        mean_all_subjects.append(np.mean(column_to_mean))
        std_all_subjects.append(np.std(column_to_mean)) 
    
#    plt.figure(figsize=(10,8))
#    plt.errorbar(c,mean_all_subjects,std_all_subjects,fmt='.',label='Mean all subjects')
#    plt.xlabel('# beep',fontsize=15)
#    plt.ylabel('Asynchrony[ms]',fontsize=15)
#    plt.xticks(fontsize = 15)
#    plt.yticks(fontsize = 15)
#    plt.grid()  
#    plt.legend(fontsize=15)
#    plt.title('Condicion %s%s' % (stim_cond,resp_cond),fontsize=15)
#    plt.savefig('mean_cond_subjects_%s%s.png' % (stim_cond,resp_cond))
    
    return mean_all_subjects, std_all_subjects, c
    
#%% GRAF 3

m_LL, s_LL, c = Mean_subjects_per_cond(5,'L','L')
m_RR, s_RR, c = Mean_subjects_per_cond(5,'R','R')
m_BB, s_BB, c = Mean_subjects_per_cond(5,'B','B')
m_RL, s_RL, c = Mean_subjects_per_cond(5,'R','L')
m_LR, s_LR, c = Mean_subjects_per_cond(5,'L','R')

plt.figure(figsize=(10,8))
plt.errorbar(c,m_LL,s_LL,fmt='.',label='LL')
plt.errorbar(c,m_RR,s_RR,fmt='.',label='RR')
plt.errorbar(c,m_BB,s_BB,fmt='.',label='BB')
plt.errorbar(c,m_RL,s_RL,fmt='.',label='RL')
plt.errorbar(c,m_LR,s_LR,fmt='.',label='LR')
plt.xlabel('# beep',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('All conditions means across subjects',fontsize=15)
plt.savefig('mean_allcond_subjects.png')    
    
     
#%% GRAF 4

def Mean_beeps_per_cond(total_number_subjects,stim_cond,resp_cond):
    
    mean_all_subjects_matrix = [] 
    for i in range(1,total_number_subjects+1):
        m, s, c = Mean_value_beep('{0:0>3}'.format(i),stim_cond,resp_cond)
        mean_all_subjects_matrix.append(m)    
     
    mean_all_subjects = []
    std_all_subjects = []
    for i in range(len(mean_all_subjects_matrix)):
        column_to_mean = []
        for j in range(len(mean_all_subjects_matrix[0])):
            column_to_mean.append(mean_all_subjects_matrix[i][j])
        mean_all_subjects.append(np.mean(column_to_mean))
        std_all_subjects.append(np.std(column_to_mean)) 
    
#    plt.figure(figsize=(10,8))
#    plt.errorbar(c,mean_all_subjects,std_all_subjects,fmt='.',label='Mean all subjects')
#    plt.xlabel('# beep',fontsize=15)
#    plt.ylabel('Asynchrony[ms]',fontsize=15)
#    plt.xticks(fontsize = 15)
#    plt.yticks(fontsize = 15)
#    plt.grid()  
#    plt.legend(fontsize=15)
#    plt.title('Condicion %s%s' % (stim_cond,resp_cond),fontsize=15)
#    plt.savefig('mean_cond_subjects_%s%s.png' % (stim_cond,resp_cond))
    
    return mean_all_subjects, std_all_subjects, c


#%% GRAF 4

m_LL, s_LL, c = Mean_beeps_per_cond(5,'L','L')
m_RR, s_RR, c = Mean_beeps_per_cond(5,'R','R')
m_BB, s_BB, c = Mean_beeps_per_cond(5,'B','B')
m_RL, s_RL, c = Mean_beeps_per_cond(5,'R','L')
m_LR, s_LR, c = Mean_beeps_per_cond(5,'L','R')

CC = np.arange(1,6)
plt.figure(figsize=(10,8))
plt.errorbar(CC,m_LL,s_LL,fmt='.',label='LL')
plt.errorbar(CC,m_RR,s_RR,fmt='.',label='RR')
plt.errorbar(CC,m_BB,s_BB,fmt='.',label='BB')
plt.errorbar(CC,m_RL,s_RL,fmt='.',label='RL')
plt.errorbar(CC,m_LR,s_LR,fmt='.',label='LR')
plt.xlabel('# Sujeto ',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('Asincronia promedio para cada sujeto en cada condicion')
plt.savefig('mean_per_sub_per_cond.png')

#%% Mean value per trial for an specific condition for an specific subject

def Mean_value_trial(subject_number,stim_cond,resp_cond,trial):
    # This function calculates the asynchronies mean value for an specific trial of a condition block of a subject. The first (N_total - N_transit) asynchronies are disregarded.
    block = Find_block(subject_number,stim_cond,resp_cond)
    N_transit = 40
    min_len_asynch_vector = N_transit + 5
    asynch = Loading_data(subject_number,block,trial,'asynch')
    if len(asynch[0])> min_len_asynch_vector:
        asynch_final = asynch[0][-N_transit:]
        print(len(asynch_final))
        return np.mean(asynch_final)
    else:
        print("Asynch vector is not long enough")

#%% Mean value of mean value of all trials for an specific condition for an specific subject

def Mean_value_block(subject_number,stim_cond,resp_cond):
    # This function calculates the mean value of all trials: takes the mean value of asynchronies for each trial and calculates the mean value between all of them. Will only take into account valid trials
    
    block = Find_block(subject_number,stim_cond,resp_cond)
    file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trials.npz")
    #file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/S'+subject_number+"*-block"+str(block)+"-trials.npz")    
    npz = np.load(file_to_load[0])
    trials = npz['trials']
    
    valid_index = []
    for i in range(len(trials)):
        if trials[i] == 1:
            valid_index.append(i)
    
    mean_value_per_trial = []
    
    for trial in valid_index:
        mean_value_per_trial.append(Mean_value_trial(subject_number,stim_cond,resp_cond,trial))
    
    return np.mean(mean_value_per_trial)
    
#%% Mean value for a condition for all subjects

def Mean_value_condition(total_number_subjects,stim_cond,resp_cond):
    mean_values_all_subjects = []
    for i in range(1,total_number_subjects+1):
        mean_values_all_subjects.append(Mean_value_block('{0:0>3}'.format(i),stim_cond,resp_cond))
        
    return np.mean(mean_values_all_subjects)    
    