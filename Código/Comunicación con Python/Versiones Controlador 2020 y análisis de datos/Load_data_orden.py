# -*- coding: utf-8 -*-
"""
Created on Thu Apr 02 15:13:19 2020

@author: Paula
"""

import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd

import statsmodels
from statsmodels.formula.api import ols


#%% Loading data

# Function for loading data specific data from either the block or trial files.
def Loading_data(subject_number,block, trial, *asked_data):
    # IMPORTANTE: DAR INPUTS COMO STRING
    # Hay que darle si o si numero de sujeto y bloque y el trial puede estar especificado o ser None. Recordar que los archivos que no tienen identificado el trial tienen guardada la informacion de todo el bloque: condicion usada, errores, percepcion del sujeto y si el trial fue valido o invalido. En cambio, al especificar el trial se tiene la informacion de cada trial particular, es decir, asincronias, datos crudos, respuestas y estimulos.

    # Depending on getting "None" or a number for input trial, defines a different filename to load.
    if trial is None:
        file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trials.npz")
        #file_to_load = glob.glob(r'Datos con Trials corregidos/S'+subject_number+"*-block"+str(block)+"-trials.npz")
        #file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/BUGRTACK_S'+subject_number+"*-block"+str(block)+"-trials.npz")    
    else:
        file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trial"+str(trial)+".npz")   
        #file_to_load = glob.glob(r'Datos con Trials corregidos/S'+subject_number+"*-block"+str(block)+"-trial"+str(trial)+".npz")  
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
    
#%%

def Find_cond(cond_vector,stim_cond,resp_cond):    
    # Search for the index of the specified condition in the inputs
    i = 0;
    while i < len(cond_vector):
        if cond_vector[i][0] == stim_cond:
           if cond_vector[i][1] == resp_cond:
               return i
           else:
               i = i+1;
        else:
            i=i+1;   
    
    
#%% After running this block you'll have an allsubjects_matrix which will contain all valid trials (already cleaned up from the transition part) for all conditions for all subjects.
# So it would respond with something like this:
#    allsubjects_matrix[i] is the matrix of subject i-1 in which each element is a matrix per condition for that subject.
#       allsubjects_matrix[i][j] is the matrix of subject i-1 in the condition j in which each element is a vector with a trial for that condition for that subject.
#           allsubjects_matrix[i][j][k] is the vector of subject i-1 in the condition j in the trial k, in which each element is a value of asynchrony.

# So for calling the trial 10 in condition BB for subject 002 you would have to call:   allsubjects_matrix[3][1][10]. Note that condition BB is in position 1 in the Condition_vector.                   

Condition_vector= [['L','L'],['R','R'],['B','B'],['R','L'],['L','R']]
total_number_subjects = 5    

# Won't take all beeps in a trial: gets last N_transit beeps assuring it has disregarded at least 5 at the beginning. That's why we need the asynchronies' vector to have a minimum length
N_transit = 40
min_len_asynch_vector = N_transit + 5 

# Define a threshold to find new outliers
threshold_outliers = 110; 

allsubjects_matrix = []

for i in range(1,total_number_subjects+1):
    
    subject_number =  '{0:0>3}'.format(i)
        
    onesubject_matrix = []
    
    for cond_pair in Condition_vector:
        block = Find_block(subject_number,cond_pair[0],cond_pair[1])
         # Loads the file
        file_to_load = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"*-block"+str(block)+"-trials.npz")
        #file_to_load = glob.glob(r'Datos con Trials corregidos/S'+subject_number+"*-block"+str(block)+"-trials.npz")
        #file_to_load = glob.glob('/home/paula/Tappingduino3/tappingduino-3-master/Datos/S'+subject_number+"*-block"+str(block)+"-trials.npz")    
        npz = np.load(file_to_load[0])
        
        # Will only work with valid trials so finds their indices
        trials = npz['trials']
        
        valid_index = []
        for i in range(len(trials)):
            if trials[i] == 1:
                valid_index.append(i)
        
        print(valid_index)
        trials_matrix = []
        # Search for outliers          
        for trial in valid_index:   
            asynch = Loading_data(subject_number,block,trial,'asynch')
            
            # Get rid of transitory stage
            if len(asynch[0])> min_len_asynch_vector:
                asynch_notTrans = asynch[0][-N_transit:]
                
                # Checks if it's an outlier based on whether it has any asynchrony bigger tan threshold_outliers from the mean of the trial
                trial_mean = np.mean(asynch_notTrans)
                dif_vector = []
                for k in range(len(asynch_notTrans)):
                    dif_vector.append(abs(trial_mean-asynch_notTrans[k]))

                if max(dif_vector)> threshold_outliers:
                    print('El trial %i de la condicion %s%s(B%i) del sujeto S%s es outlier' % (trial,cond_pair[0],cond_pair[1],block,subject_number))
                    
                # If all asynchronies are whithin the mean+/-threshold, then we append it to the matrix    
                else:
                    trials_matrix.append(asynch_notTrans)
                    
            else:
                print("Asynch vector is not long enough")
                break
            
        onesubject_matrix.append(trials_matrix)
    
    allsubjects_matrix.append(onesubject_matrix)
    
#%% 

# GRÁFICO 1: Grafico de los trials válidos de un sujeto en una condición
def Plot_alltrials(subject_number, stim_cond, resp_cond):
    condition = Find_cond(Condition_vector,stim_cond,resp_cond)
    
    for trial_number in range(len(allsubjects_matrix[subject_number+1][condition])):
        plt.plot(allsubjects_matrix[subject_number+1][condition][trial_number],'.-', label = 'trial %d' % trial_number)
        
    plt.xlabel('# beep',fontsize=15)
    plt.ylabel('Asynchrony[ms]',fontsize=15)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid()  
    plt.legend()
    plt.title('Sujeto %s, Condicion %s%s' % (subject_number,stim_cond,resp_cond),fontsize=15)
    

    return


#%%

# GRÁFICO 2: Gráfico del promedio across trials para una condición.
def mean_acrosstrials(subject_number, stim_cond, resp_cond):
    condition = Find_cond(Condition_vector,stim_cond,resp_cond)

    long_trial = len(allsubjects_matrix[subject_number-1][condition][0])
    cant_trials = len(allsubjects_matrix[subject_number-1][condition])
    
    mean_across_trials = []
    std_across_trials = []
    for j in range(long_trial):
        column_to_mean = []
        for i in range(cant_trials):
            column_to_mean.append(allsubjects_matrix[subject_number-1][condition][i][j])
        mean_across_trials.append(np.mean(column_to_mean))
        std_across_trials.append(np.std(column_to_mean)/np.sqrt(len(column_to_mean))) 
        
    return mean_across_trials, std_across_trials, long_trial


# Corro la última función para hacer el gráfico 2. Para cada condición corro para todos los sujetos. Appendeo entonces primero por sujeto y luego por condición. los elementos de graf2_matrix_value serán matrices, una por cada condición. graf2_matrix_value[i] es una de esas matrices (ya seleccionamos en condición) y cada elemento de ella será el vector de mean_across_trials para un sujeto para la condición seleccionada. En graf2_matrix_err se tiene la misma lógica pero se van guardando las barras de error. Idem con graf2_matrix_mean pero con el valor promedio del vector.

graf2_matrix_value = []
graf2_matrix_err = []
graf2_matrix_mean = []
for cond_pair in Condition_vector:
    graf2_matrix_value_percond = []
    graf2_matrix_err_percond = []
    graf2_matrix_mean_percond = []
    for i in range(1,total_number_subjects+1):
        graf2_matrix_value_percond.append(mean_acrosstrials(i,cond_pair[0],cond_pair[1])[0])
        graf2_matrix_mean_percond.append(np.mean(mean_acrosstrials(i,cond_pair[0],cond_pair[1])[0]))
        graf2_matrix_err_percond.append(mean_acrosstrials(i,cond_pair[0],cond_pair[1])[1])
        long_trial = mean_acrosstrials(i,cond_pair[0],cond_pair[1])[2]
    graf2_matrix_value.append(graf2_matrix_value_percond)
    graf2_matrix_mean.append(graf2_matrix_mean_percond)
    graf2_matrix_err.append(graf2_matrix_err_percond)


# HAGO EL PLOT 2
cmap = plt.get_cmap('Dark2_r')
colors = [cmap(i) for i in np.linspace(0, 1, total_number_subjects)]
 
# X axis
beeps = np.arange(long_trial)

for cond_number in range(len(graf2_matrix_value)):
    plt.figure(figsize=(10,8))
    for subj_number, color in enumerate(colors, start=0):
        plt.errorbar(beeps,graf2_matrix_value[cond_number][subj_number],graf2_matrix_err[cond_number][subj_number],color = color, fmt='.-',label='S00%i' % int(subj_number+1))


    # Estos casos especiales del sujeto 1 y 3 despues se pueden sacar para la version general.
        if subj_number == 0:
            A = np.array(graf2_matrix_mean[cond_number])
            mean_NS001 =  A[np.r_[1:len(A)]]
            plt.axhline(np.mean(mean_NS001),linestyle='solid',color=color, label='Mean w/o S001')
            plt.axhline(graf2_matrix_mean[cond_number][subj_number],linestyle='dashed', color = color)
                                  
        if subj_number == 2:    
            A = np.array(graf2_matrix_mean[cond_number])
            mean_NS003 = A[np.r_[:2, 4:len(A)]]
            plt.axhline(np.mean(mean_NS003),linestyle='solid',color=color,label='Mean w/o S003')
            plt.axhline(graf2_matrix_mean[cond_number][subj_number],linestyle='dashed', color = color)
            
            
    plt.axhline(np.mean(graf2_matrix_mean[cond_number]),linestyle='solid',color='k', label='Mean all S')
    

    plt.xlabel('# beep',fontsize=15)
    plt.ylabel('Asynchrony[ms]',fontsize=15)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid()  
    plt.legend(fontsize=9)
    plt.title('Condition %s%s' % (Condition_vector[cond_number][0],Condition_vector[cond_number][1]),fontsize=15)   
#    plt.savefig('mean_across_trials_%s%s_sinOutliers.png' % (Condition_vector[cond_number][0],Condition_vector[cond_number][1]))    


#%% Analizo drift en los gráficos anteriores

max_dif_accept = 20

for cond_number in range(len(graf2_matrix_value)):
    for subj_number in range(len(graf2_matrix_value[0])):
        x_firsthalf = np.mean(graf2_matrix_value[cond_number][subj_number][0:15])
        x_secondhalf = np.mean(graf2_matrix_value[cond_number][subj_number][15:40])
        
        if abs(x_firsthalf-x_secondhalf)> max_dif_accept:
            print('El sujeto S00%i tiene drift en la condicion %s%s' % (subj_number+1, Condition_vector[cond_number][0],Condition_vector[cond_number][1]))


#%% Analizo distribución de promedios en los gráficos anteriores

import seaborn as sns

for cond_number in range(len(graf2_matrix_mean)):
    plt.figure(figsize=(10,8))
    x = graf2_matrix_mean[cond_number]
    sns.distplot(x);
    perc_25 = np.percentile(x,25)
    perc_75 = np.percentile(x,75)
    iqr = perc_75 - perc_25
    lim_sup = perc_75 + 1.5*iqr
    lim_inf = perc_25 - 1.5*iqr
    
    for i in range(len(x)):
        if x[i] > lim_sup:
            plt.axvline(x[i], color = 'red', label = 'S00%i' % (i+1))
        elif x[i] < lim_inf:
            plt.axvline(x[i], color = 'red', label = 'S00%i' % (i+1))

    plt.axvline(perc_25)
    plt.axvline(perc_75)
    plt.xlabel('Mean asynchrony[ms]',fontsize=15)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid()  
    plt.legend()
    plt.title('Condition %s%s' % (Condition_vector[cond_number][0],Condition_vector[cond_number][1]),fontsize=15)   


#%% GRÁFICO 3: quiero promediar across subjects sobre la matrix que tiene dim (#beeps)x(#subjects), pero que ademas viene de ya haber realizado el promedio anterior (el del graf2). Entonces, voy a tomar la matriz graf2_matrix_value que es esto que quiero y voy a promediar verticalmente separando en condiciones.

                                                                             
graf3_matrix_value = []
graf3_matrix_err = []
for cond_number in range(len(graf2_matrix_value)):
    graf3_matrix_value_percond = []
    graf3_matrix_err_percond = []
    for beep_number in range(long_trial):
        graf3_matrix_value_perbeep = []
        for subj_number in range(len(graf2_matrix_value[0])):
            graf3_matrix_value_perbeep.append(graf2_matrix_value[cond_number][subj_number][beep_number])
        
        graf3_matrix_value_percond.append(np.mean(graf3_matrix_value_perbeep))
        graf3_matrix_err_percond.append(np.std(graf3_matrix_value_perbeep)/np.sqrt(len(graf3_matrix_value_perbeep)))
    
    graf3_matrix_value.append(graf3_matrix_value_percond)
    graf3_matrix_err.append(graf3_matrix_err_percond)

#
# HAGO EL PLOT 3

colors_cond = [cmap(i) for i in np.linspace(0, 1, len(Condition_vector))]

plt.figure(figsize=(10,8))
for cond_number, color_cond in enumerate(colors_cond, start = 0):
    plt.errorbar(beeps,graf3_matrix_value[cond_number],graf3_matrix_err[cond_number],color = color_cond, fmt='.-',label='%s%s' % (Condition_vector[cond_number][0],Condition_vector[cond_number][1]))
    

plt.xlabel('# beep',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=9)
plt.title('All conditions means across subjects',fontsize=15)
#plt.savefig('mean_across_subjects_sinOutliers.png')    



#%% GRÁFICO 4: quiero promediar along sobre la matrix que tiene dim (#beeps)x(#subjects), pero que ademas viene de ya haber realizado el promedio anterior (el del graf2). Entonces, voy a tomar la matriz graf2_matrix_value que es esto que quiero y voy a promediar horizontalmente separando en condiciones y sujetos.

                                                                             
graf4_matrix_value = []
graf4_matrix_err = []
for cond_number in range(len(graf2_matrix_value)):
    graf4_matrix_value_persubj = []
    graf4_matrix_err_persubj = []
    for subj_number in range(len(graf2_matrix_value[0])):
        graf4_matrix_value_persubj.append(np.mean(graf2_matrix_value[cond_number][subj_number]))
        graf4_matrix_err_persubj.append(np.std(graf2_matrix_value[cond_number][subj_number])/np.sqrt(len(graf2_matrix_value[cond_number][subj_number])))

    graf4_matrix_value.append(graf4_matrix_value_persubj)
    graf4_matrix_err.append(graf4_matrix_err_persubj)


# HAGO EL PLOT 4


# Eje x
CC = np.arange(len(Condition_vector))

colors_subj = [cmap(i) for i in np.linspace(0, 1, total_number_subjects)]

plt.figure(figsize=(10,8))
for subj_number, color_subj in enumerate(colors_subj, start = 0):
    graf4_matrix_value_persubj_plot = []
    graf4_matrix_err_persubj_plot = []
    for cond_number in range(len(graf4_matrix_value)):
        graf4_matrix_value_persubj_plot.append(graf4_matrix_value[cond_number][subj_number])
        graf4_matrix_err_persubj_plot.append(graf4_matrix_err[cond_number][subj_number])
        
    plt.errorbar(CC,graf4_matrix_value_persubj_plot,graf4_matrix_err_persubj_plot,color = color_subj, fmt='.-',label='S00%i' % int(subj_number+1),capsize=10)
    
# Agrego promedios por condicion
graf4_matrix_mean = []
for cond_number in range(len(graf4_matrix_value)):
        graf4_matrix_mean.append(np.mean(graf4_matrix_value[cond_number]))
plt.plot(CC,graf4_matrix_mean,'*',markersize=15)

plt.xlabel('# beep',fontsize=15)
plt.ylabel('Asynchrony[ms]',fontsize=15)
labels = ['LL', 'RR', 'BB','RL','LR']
plt.xticks(CC, labels,fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=9)
plt.title('All conditions means along trials for all subjects')
#plt.savefig('mean_across_subjects_sinOutliers.png')    
 

#%% GRÁFICOS 5 Y 6

# GRÁFICOS 5 y 6 - PASO 1: Gráfico del promedio along trials para una condición.
def mean_alongtrials(subject_number, stim_cond, resp_cond):
    condition = Find_cond(Condition_vector,stim_cond,resp_cond)

    long_trial = len(allsubjects_matrix[subject_number-1][condition][0])
    cant_trials = len(allsubjects_matrix[subject_number-1][condition])
    
    mean_along_trials = []
    std_along_trials = []
    for j in range(cant_trials):
        mean_along_trials.append(np.mean(allsubjects_matrix[subject_number-1][condition][j]))
        std_along_trials.append(np.std(allsubjects_matrix[subject_number-1][condition][j])/np.sqrt(len(allsubjects_matrix[subject_number-1][condition][j]))) 
        
    return mean_along_trials, std_along_trials, long_trial
  
    
# GRÁFICOS 5 y 6 - PASO 2: Con los vectores que obtenga para cada sujeto en cada condición de la función anterior, voy a promediar across trials.
 
graf5_paso2_matrix_mean = []
graf5_paso2_matrix_mean_err = []
graf5_paso2_matrix_std = []
graf5_paso2_matrix_std_err = []

for cond_pair in Condition_vector:
    graf5_paso2_mean_mean_percond = []
    graf5_paso2_err_mean_percond = []

    graf5_paso2_mean_std_percond = []
    graf5_paso2_err_std_percond = []

    for i in range(1,total_number_subjects+1):
        graf5_paso2_mean_mean_percond.append(np.mean(mean_alongtrials(i,cond_pair[0],cond_pair[1])[0]))
        graf5_paso2_err_mean_percond.append(np.std(mean_alongtrials(i,cond_pair[0],cond_pair[1])[0])/np.sqrt(len(mean_alongtrials(i,cond_pair[0],cond_pair[1])[0]))) # ESTE LO VOY A NECESITAR PARA EL GRAF 7
        
        graf5_paso2_mean_std_percond.append(np.mean(mean_alongtrials(i,cond_pair[0],cond_pair[1])[1]))
        graf5_paso2_err_std_percond.append(np.std(mean_alongtrials(i,cond_pair[0],cond_pair[1])[1])/np.sqrt(len(mean_alongtrials(i,cond_pair[0],cond_pair[1])[1]))) # ESTE LO VOY A NECESITAR PARA EL GRAF 8
        
        long_trial = mean_alongtrials(i,cond_pair[0],cond_pair[1])[2]
        
    graf5_paso2_matrix_mean.append(graf5_paso2_mean_mean_percond)
    graf5_paso2_matrix_std.append(graf5_paso2_mean_std_percond)
    graf5_paso2_matrix_mean_err.append(graf5_paso2_err_mean_percond)
    graf5_paso2_matrix_std_err.append(graf5_paso2_err_std_percond)
    
    
# GRÁFICOS 5 y 6 - PASO 3: Con los vectores que obtenga para cada condición en el paso anterior, promedio across subjects

graf5_paso3_matrix_mean_value = []
graf5_paso3_matrix_mean_err = []
graf5_paso3_matrix_std_value = []
graf5_paso3_matrix_std_err = []

for cond_number in range(len(graf5_paso2_matrix_mean)):
    graf5_paso3_matrix_mean_value.append(np.mean(graf5_paso2_matrix_mean[cond_number]))
    graf5_paso3_matrix_mean_err.append(np.std(graf5_paso2_matrix_mean[cond_number])/np.sqrt(len(graf5_paso2_matrix_mean[cond_number])))
    
    graf5_paso3_matrix_std_value.append(np.mean(graf5_paso2_matrix_std[cond_number]))
    graf5_paso3_matrix_std_err.append(np.std(graf5_paso2_matrix_std[cond_number])/np.sqrt(len(graf5_paso2_matrix_std[cond_number])))
    
# CASOS PARTICULARES SACANDO S001 Y S003

# Saco sujeto 1
                                        

graf5_paso3_matrix_mean_value_NS001 = []
graf5_paso3_matrix_mean_err_NS001 = []
graf5_paso3_matrix_std_value_NS001 = []
graf5_paso3_matrix_std_err_NS001 = []

for cond_number in range(len(graf5_paso2_matrix_mean)):
    A = np.array(graf5_paso2_matrix_mean[cond_number])
    graf5_paso2_matrix_mean_NS001 =  A[np.r_[1:len(A)]];

    B = np.array(graf5_paso2_matrix_std[cond_number])
    graf5_paso2_matrix_std_NS001 =  B[np.r_[1:len(B)]]; 

    graf5_paso3_matrix_mean_value_NS001.append(np.mean(graf5_paso2_matrix_mean_NS001))
    graf5_paso3_matrix_mean_err_NS001.append(np.std(graf5_paso2_matrix_mean_NS001)/np.sqrt(len(graf5_paso2_matrix_mean_NS001)))
    graf5_paso3_matrix_std_value_NS001.append(np.mean(graf5_paso2_matrix_std_NS001))
    graf5_paso3_matrix_std_err_NS001.append(np.std(graf5_paso2_matrix_std_NS001)/np.sqrt(len(graf5_paso2_matrix_std_NS001)))    
    
#
## Saco sujeto 3                          

graf5_paso3_matrix_mean_value_NS003 = []
graf5_paso3_matrix_mean_err_NS003 = []
graf5_paso3_matrix_std_value_NS003 = []
graf5_paso3_matrix_std_err_NS003 = []

for cond_number in range(len(graf5_paso2_matrix_mean)):
    A = np.array(graf5_paso2_matrix_mean[cond_number])
    graf5_paso2_matrix_mean_NS003 =  A[np.r_[:2, 4:len(A)]];
                                             
    B = np.array(graf5_paso2_matrix_std[cond_number])
    graf5_paso2_matrix_std_NS003 =  B[np.r_[:2, 4:len(B)]];   
    
    
    graf5_paso3_matrix_mean_value_NS003.append(np.mean(graf5_paso2_matrix_mean_NS003))
    graf5_paso3_matrix_mean_err_NS003.append(np.std(graf5_paso2_matrix_mean_NS003)/np.sqrt(len(graf5_paso2_matrix_mean_NS003)))
    graf5_paso3_matrix_std_value_NS003.append(np.mean(graf5_paso2_matrix_std_NS003))
    graf5_paso3_matrix_std_err_NS003.append(np.std(graf5_paso2_matrix_std_NS003)/np.sqrt(len(graf5_paso2_matrix_std_NS003)))  
#    
    
# HAGO EL PLOT 5

colors_subj = [cmap(i) for i in np.linspace(0, 1, total_number_subjects)]

# Eje x
CC = np.arange(5)

plt.figure(figsize=(10,8))
plt.errorbar(CC,graf5_paso3_matrix_mean_value,graf5_paso3_matrix_mean_err,color='k',fmt='*-',label='Mean sobre todos los sujetos',capsize=10)
plt.errorbar(CC,graf5_paso3_matrix_mean_value_NS001,graf5_paso3_matrix_mean_err_NS001,fmt='*-',label='Mean sin S001',capsize=10,color=colors_subj[0])
plt.errorbar(CC,graf5_paso3_matrix_mean_value_NS003,graf5_paso3_matrix_mean_err_NS003,color=colors_subj[2],fmt='*-',label='Mean sin S003',capsize=10)
plt.xlabel('Condiciones ',fontsize=15)
plt.ylabel('Mean asynchrony[ms]',fontsize=15)
labels = ['LL', 'RR', 'BB','RL','LR']
plt.xticks(CC,labels, fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('asyn_mean_ave_percond')
#plt.savefig('asyn_mean_ave_percond_sinOutliers.png')

# Otra visualización graf 5

Cond_Stim = np.arange(2)

Y_FL = [graf5_paso3_matrix_mean_value[0],graf5_paso3_matrix_mean_value[3]]
Y_FL_err = [graf5_paso3_matrix_mean_err[0],graf5_paso3_matrix_mean_err[3]]


Y_FR = [graf5_paso3_matrix_mean_value[4],graf5_paso3_matrix_mean_value[1]]
Y_FR_err = [graf5_paso3_matrix_mean_err[4],graf5_paso3_matrix_mean_err[1]]

plt.figure(figsize=(10,8))
plt.errorbar(Cond_Stim,Y_FL,Y_FL_err,color='k',fmt='*-',label='Fdbk L',capsize=10)
plt.errorbar(Cond_Stim,Y_FR,Y_FR_err,fmt='*-',label='Fdbk R',capsize=10,color=colors_subj[0])
plt.xlabel('Condicion Stim',fontsize=15)
plt.ylabel('Mean asynchrony[ms]',fontsize=15)
labels = ['L', 'R']
plt.xticks(Cond_Stim,labels, fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.savefig('Graf5_PorCondsSeparadas.png')


# Otra más

     




# HAGO EL PLOT 6

plt.figure(figsize=(10,8))
plt.errorbar(CC,graf5_paso3_matrix_std_value,graf5_paso3_matrix_std_err,color='k',fmt='*-',label='Mean sobre todos los sujetos',capsize=10)
plt.errorbar(CC,graf5_paso3_matrix_std_value_NS001,graf5_paso3_matrix_std_err_NS001,fmt='*-',label='Mean sin S001',capsize=10,color=colors_subj[0])
plt.errorbar(CC,graf5_paso3_matrix_std_value_NS003,graf5_paso3_matrix_std_err_NS003,color=colors_subj[2],fmt='*-',label='Mean sin S003',capsize=10)
plt.xlabel('Condiciones ',fontsize=15)
plt.ylabel('Mean Standard Deviation [ms]',fontsize=15)
labels = ['LL', 'RR', 'BB','RL','LR']
plt.xticks(CC,labels, fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('asyn_std_ave_percond')
#plt.savefig('asyn_std_ave_percond_sinOutliers.png')


Par_ID = np.arange(2)

Y_SL_std = [graf5_paso3_matrix_std_value[0],graf5_paso3_matrix_std_value[4]]
Y_SL_std_err = [graf5_paso3_matrix_std_err[0],graf5_paso3_matrix_std_err[4]]


Y_SR_std = [graf5_paso3_matrix_std_value[1],graf5_paso3_matrix_std_value[3]]
Y_SR_std_err = [graf5_paso3_matrix_std_err[1],graf5_paso3_matrix_std_err[3]]

plt.figure(figsize=(10,8))
plt.errorbar(Par_ID,Y_SL_std,Y_SL_std_err,color='k',fmt='*-',label='Stim L',capsize=10)
plt.errorbar(Par_ID,Y_SR_std,Y_SR_std_err,fmt='*-',label='Stim R',capsize=10,color=colors_subj[0])
plt.xlabel('Par Stim-Fdbk',fontsize=15)
plt.ylabel('Mean STD asynchrony[ms]',fontsize=15)
labels = ['Same', 'Diff']
plt.xticks(Par_ID,labels, fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
#plt.savefig('STD_NUEVOSFACT.png')

#%% GRÁFICOS 7 Y 8: Mostrar el paso anterior a los gráficos 5 y 6, es decir, sin promediar across subjects. Esto sería tomar la matrix graf5_paso2_matrix_mean y graficar esos datos pero usando una línea por sujeto y las condiciones en el eje X. Para esto hay que "rotar los datos". Análogamente el graf 8 es lo mismo pero para el caso de std y no del mean.

graf7_matrix_mean_mean = []
graf7_matrix_mean_err = []
graf7_matrix_std_mean = []
graf7_matrix_std_err = []


for subj_number in range(len(graf5_paso2_matrix_mean[0])):
    
    graf7_matrix_mean_mean_percond = []
    graf7_matrix_mean_err_percond = []
    graf7_matrix_std_mean_percond = []
    graf7_matrix_std_err_percond = []
    for cond_number in range(len(graf5_paso2_matrix_mean)):
        graf7_matrix_mean_mean_percond.append(graf5_paso2_matrix_mean[cond_number][subj_number])
        graf7_matrix_mean_err_percond.append(graf5_paso2_matrix_mean_err[cond_number][subj_number])
        graf7_matrix_std_mean_percond.append(graf5_paso2_matrix_std[cond_number][subj_number])
        graf7_matrix_std_err_percond.append(graf5_paso2_matrix_std_err[cond_number][subj_number])

    graf7_matrix_mean_mean.append(graf7_matrix_mean_mean_percond)
    graf7_matrix_mean_err.append(graf7_matrix_mean_err_percond)
    graf7_matrix_std_mean.append(graf7_matrix_std_mean_percond)
    graf7_matrix_std_err.append(graf7_matrix_std_err_percond)



# HAGO EL PLOT 7

colors_subj = [cmap(i) for i in np.linspace(0, 1, total_number_subjects)]


plt.figure(figsize=(10,8))
for subj_number, color_subj in enumerate(colors_subj, start=0):
    plt.errorbar(CC,graf7_matrix_mean_mean[subj_number],graf7_matrix_mean_err[subj_number],fmt='*-',capsize=10, color=color_subj,label = 'S00%i' % int(subj_number+1))
plt.xlabel('Condiciones ',fontsize=15)
plt.ylabel('Mean asynchrony[ms]',fontsize=15)
labels = ['LL', 'RR', 'BB','RL','LR']
plt.xticks(CC,labels, fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('asyn_mean_eachSubj')
#plt.savefig('asyn_mean_eachSubj.png')


# HAGO EL PLOT 8
plt.rcParams.update({'lines.markeredgewidth': 1})

plt.figure(figsize=(10,8))
for subj_number, color_subj in enumerate(colors_subj,start=0):
    plt.errorbar(CC,graf7_matrix_std_mean[subj_number],graf7_matrix_std_err[subj_number],fmt='*-',capsize=10, color=color_subj,label = 'S00%i' % int(subj_number+1))

plt.xlabel('Condiciones ',fontsize=15)
plt.ylabel('Asynchrony Standard Deviation[ms]',fontsize=15)
labels = ['LL', 'RR', 'BB','RL','LR']
plt.xticks(CC,labels, fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)
plt.title('asyn_std_eachSubj')
#plt.savefig('asyn_std_eachSubj.png')



#%% REHAGO GRAF 2 CON INFO QUE SALE DEL GRAF5 PASO2, POR ESO REPITO ACÁ ABAJO

# HAGO EL PLOT 2
cmap = plt.get_cmap('Dark2_r')
colors = [cmap(i) for i in np.linspace(0, 1, total_number_subjects)]
 
# X axis
beeps = np.arange(long_trial)

for cond_number in range(len(graf2_matrix_value)):
    plt.figure(figsize=(10,8))
    for subj_number, color in enumerate(colors, start=0):
        plt.errorbar(beeps,graf2_matrix_value[cond_number][subj_number],graf2_matrix_err[cond_number][subj_number],color = color, fmt='.-',label='S00%i' % int(subj_number+1))

    # Estos casos especiales del sujeto 1 y 3 despues se pueden sacar para la version general.
        if subj_number == 0:
            A = np.array(graf2_matrix_mean[cond_number])
            mean_NS001 =  A[np.r_[1:len(A)]]
            plt.axhline(np.mean(mean_NS001),linestyle='solid',color=color, label='Mean w/o S001')
            plt.axhline(graf2_matrix_mean[cond_number][subj_number],linestyle='dashed', color = color)
            plt.axhline(graf5_paso2_matrix_mean[cond_number][subj_number],linestyle='dotted',linewidth=5, color = color)                    
        if subj_number == 2:    
            A = np.array(graf2_matrix_mean[cond_number])
            mean_NS003 = A[np.r_[:2, 4:len(A)]]
            plt.axhline(np.mean(mean_NS003),linestyle='solid',color=color,label='Mean w/o S003')
            plt.axhline(graf2_matrix_mean[cond_number][subj_number],linestyle='dashed', color = color)
            plt.axhline(graf5_paso2_matrix_mean[cond_number][subj_number],linestyle='dotted', linewidth=5,color = color)     
            
    plt.axhline(np.mean(graf2_matrix_mean[cond_number]),linestyle='solid',color='k', label='Mean all S')
    

    plt.xlabel('# beep',fontsize=15)
    plt.ylabel('Asynchrony[ms]',fontsize=15)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid()  
    plt.legend(fontsize=9)
    plt.title('Condition %s%s' % (Condition_vector[cond_number][0],Condition_vector[cond_number][1]),fontsize=15)   
    #plt.savefig('mean_across_trials_%s%s_sinOutliers_dosPromedios.png' % (Condition_vector[cond_number][0],Condition_vector[cond_number][1]))  
    
    
    
#%%

# Paired Student's t-test

from scipy.stats import ttest_rel, f_oneway

# generate two independent samples
dataLL = graf5_paso2_matrix_mean[0] # LL
dataRR = graf5_paso2_matrix_mean[1] # RR
# compare samples
stat, p = ttest_rel(dataLL, dataRR)
print('Statistics=%.3f, p=%.3f' % (stat, p))

alpha = 0.05
if p > alpha:
	print('Accept null hypothesis that the means (between LL and RR) are equal.')
else:
	print('Reject the null hypothesis that the means (between LL and RR) are equal.')
    
    
# generate two independent samples
data3 = graf5_paso2_matrix_mean[3] # RL
data4 = graf5_paso2_matrix_mean[4] # LR
# compare samples
stat, p = ttest_rel(data3, data4)
print('Statistics=%.3f, p=%.3f' % (stat, p))

if p > alpha:
	print('Accept null hypothesis that the means (between RL and LR) are equal.')
else:
	print('Reject the null hypothesis that the means (between RL and LR) are equal.')   
    
    
## HAGO LO MISMO PERO AHORA ENTRE BB Y RR

dataBB = graf5_paso2_matrix_mean[2]

statBBLL, pBBLL = ttest_rel(dataBB, dataLL)
print('Statistics=%.3f, p=%.3f' % (statBBLL, pBBLL))

if pBBLL > alpha:
	print('Accept null hypothesis that the means (between BB and LL) are equal.')
else:
	print('Reject the null hypothesis that the means (between BB and LL) are equal.')  


statBBRR, pBBRR = ttest_rel(dataBB, dataRR)
print('Statistics=%.3f, p=%.3f' % (statBBRR, pBBRR))

if pBBRR > alpha:
	print('Accept null hypothesis that the means (between BB and RR) are equal.')
else:
	print('Reject the null hypothesis that the means (between BB and RR) are equal.')  
  
#%%
    
# ONE WAY ANOVA

stat_anova, p_anova = f_oneway(graf5_paso2_matrix_mean[0],graf5_paso2_matrix_mean[1],graf5_paso2_matrix_mean[2],graf5_paso2_matrix_mean[3],graf5_paso2_matrix_mean[4])
print('Statistics=%.3f, p=%.3f' % (stat_anova, p_anova))

alpha = 0.05
if p > alpha:
	print('Accept null hypothesis that the means are equal.')
else:
	print('Reject the null hypothesis that the means are equal.')  



#%% TWO WAY ANOVA
import statsmodels
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Uso un ejemplo de internet que tiene datos análogos a los mios, entonces armo un csv con el mismo formato.

#data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/tooth_growth_csv')

data = pd.read_csv(r'C:\Users\Paula\Downloads\PruebaTWOWAY - PruebaTWOWAY.csv')


#formula = 'len ~ C(supp) + C(dose) + C(supp):C(dose)'
formula = 'asynch ~ C(stim) + C(fdbk) + C(stim):C(fdbk)'
model = ols(formula, data).fit()
aov_table = statsmodels.stats.anova.anova_lm(model, typ=2)
print(aov_table)


# Interpretación de resultados
# La columna PR(>F) es el p-value de cada estadístico calculado. Tenemos 3 estadísticos, uno para el factor estimulo, otro para el factor feedback y otro para el factor "interaccion". Para interpretarlo entonces decimos que, por ejemplo, si el p-value del estadistico para estimulo es mayor que nuestra significancia, entonces el factor estimulo no tiene impacto en el resultado, es decir, los sujetos performan igual independientemente de donde venga el estimulo.
# De manera análoga, si el p-value del factor de feedback es aceptado por la significancia, entonces de dónde venga el feedback tampoco tiene impacto en la performance de los sujetos
# Finalmente, el caso de interacción que es C(stim):C(fdbk) de nuevo nos dice que el efecto de la combinación de factores es insignificante, ya que su pvalue es mayor que la significancia.
# Caso contrario, si alguno de estos p-values fuese menos que la significancia, entonces podríamos decir que ese factor tiene un efecto significante en los resultados.




#%% REPEATED MEASURES TWO WAY ANOVA

import pyvttbl as pt
from collections import namedtuple

N = 5
Stim = ['SL','SR']
Fdbk = ['FL','FR']


sub_id = [i+1 for i in xrange(N)]*(len(Stim)*len(Fdbk))
Stim_LR = np.concatenate([np.array([s]*N) for s in Stim]*len(Fdbk)).tolist()
Fdbk_LR = np.concatenate([np.array([f]*(N*len(Stim))) for f in Fdbk]).tolist()

# Así como está entonces me quedan LL, RL, LR y RR (en ese orden)

data1 = graf5_paso2_matrix_mean[0] # LL
data2 = graf5_paso2_matrix_mean[1] # RR
    
# generate two independent samples
data3 = graf5_paso2_matrix_mean[3] # RL
data4 = graf5_paso2_matrix_mean[4] # LR
                               
rt = np.concatenate([data1,data3,data4,data2])

# Para ahorrarme tener que poner esto asi "a mano", podria cambiar el orden del vector de conditions.. pero eso cambia los gráficos. Preguntar.


Sub = namedtuple('Sub', ['Sub_id', 'rt','Stim_LR', 'Fdbk_LR'])               
df = pt.DataFrame()

for idx in xrange(len(sub_id)):
    df.insert(Sub(sub_id[idx],rt[idx], Stim_LR[idx],Fdbk_LR[idx])._asdict())


aov = df.anova('rt', sub='Sub_id', wfactors=['Stim_LR', 'Fdbk_LR'])
print(aov)


#%% REPEATED MEASURES TWO WAY ANOVA - NUEVOS FACTORES


N = 5
Par = ['I','D'] # Factor par Stim y Fdbk, si son iguales(I) o diferentes (D)
Lateralidad_stim = ['SL','SR'] # Factor lateralidad tomando de referencia el estimulo


sub_id = [i+1 for i in xrange(N)]*(len(Par)*len(Lateralidad_stim))
Par_ID = np.concatenate([np.array([p]*N) for p in Par]*len(Lateralidad_stim)).tolist()
LatStim_LR = np.concatenate([np.array([l]*(N*len(Par))) for l in Lateralidad_stim]).tolist()

# Así como está entonces me quedan LL, LR, RR y RL (en ese orden)

data1 = graf5_paso2_matrix_mean[0] # LL
data2 = graf5_paso2_matrix_mean[1] # RR
    
# generate two independent samples
data3 = graf5_paso2_matrix_mean[3] # RL
data4 = graf5_paso2_matrix_mean[4] # LR
                               
rt = np.concatenate([data1,data4,data2,data3])

# Para ahorrarme tener que poner esto asi "a mano", podria cambiar el orden del vector de conditions.. pero eso cambia los gráficos. Preguntar.


Sub = namedtuple('Sub', ['Sub_id', 'rt','Par_ID', 'LatStim_LR'])               
df = pt.DataFrame()

for idx in xrange(len(sub_id)):
    df.insert(Sub(sub_id[idx],rt[idx], Par_ID[idx],LatStim_LR[idx])._asdict())


aov = df.anova('rt', sub='Sub_id', wfactors=['Par_ID', 'LatStim_LR'])
print(aov)


#%%

N = 5
Par = ['I','D'] # Factor par Stim y Fdbk, si son iguales(I) o diferentes (D)
Lateralidad_stim = ['SL','SR'] # Factor lateralidad tomando de referencia el estimulo


sub_id = [i+1 for i in xrange(N)]*(len(Par)*len(Lateralidad_stim))
Par_ID = np.concatenate([np.array([p]*N) for p in Par]*len(Lateralidad_stim)).tolist()
LatStim_LR = np.concatenate([np.array([l]*(N*len(Par))) for l in Lateralidad_stim]).tolist()

# Así como está entonces me quedan LL, LR, RR y RL (en ese orden)

data1 = graf5_paso2_matrix_std[0] # LL
data2 = graf5_paso2_matrix_std[1] # RR
    
# generate two independent samples
data3 = graf5_paso2_matrix_std[3] # RL
data4 = graf5_paso2_matrix_std[4] # LR
                               
rt = np.concatenate([data1,data4,data2,data3])

# Para ahorrarme tener que poner esto asi "a mano", podria cambiar el orden del vector de conditions.. pero eso cambia los gráficos. Preguntar.


Sub = namedtuple('Sub', ['Sub_id', 'rt','Par_ID', 'LatStim_LR'])               
df = pt.DataFrame()

for idx in xrange(len(sub_id)):
    df.insert(Sub(sub_id[idx],rt[idx], Par_ID[idx],LatStim_LR[idx])._asdict())


aov = df.anova('rt', sub='Sub_id', wfactors=['Par_ID', 'LatStim_LR'])
print(aov)




#%%
S_COND = np.arange(2)

Y_FL = [-10,-20]
Y_FR = [-20,-30]



#plt.figure(figsize=(10,8))
plt.plot(S_COND,Y_FL,'*-',label='Fdbk L')
plt.plot(S_COND,Y_FR,'*-',label='Fdbk R')
plt.xlabel('Condicion Stim',fontsize=15)
plt.ylabel('Mean asynchrony[ms]',fontsize=15)
labels = ['L', 'R']
plt.xticks(S_COND,labels, fontsize = 15)
plt.yticks(fontsize = 15)
#plt.axis([-0.1,1.1,-25,-5])
plt.grid()  
plt.legend(fontsize=15)
#plt.savefig('Graf5_PorPares.png')