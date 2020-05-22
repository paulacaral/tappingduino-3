# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 17:33:01 2020

@author: Paula


El propósito de este script es agarrar los datos de todos los sujetos, pasarlos por distintos criterios de outliers (1 de trials y 2 de sujeto) y quedarse solo con la información que va a servir después para el análisis.
El primer criterio por el que pasan los datos es para encontrar trials outliers. Si algún valor de asincronía del trial está por fuera del intervalo (promedio del trial-umbral, promedio del trial + umbral), entonces el trial es outlier.
Con los trials que sobrevivieron a ese primer criterio, se calcula el promedio across trials para cada condición para cada sujeto y se estudian dos criterios para determinar si un sujeto es outlier.
1. Si el promedio de sus trials para una condición está fuera de la campana principal de distribución de promedios, entonces el sujeto es outlier.
2. Si el promedio de sus trials tiene un drift en una cierta condición, entonces el sujeto es outlier.

Finalmente, con los sujetos y trials que hayan sobrevivido a estos criterios armo una nueva matriz que tiene los datos totales de cada sujeto en cada condición, una matriz con los datos ya promediados across trials y otra con los datos ya promediados along trials. Además, guardo en un vector los números identificatorios de cada sujeto para poder rastrearlo en los datos "totales" si es necesario.
"""

import numpy as np
import matplotlib.pyplot as plt
import glob
import seaborn as sns

#%% DEFINO FUNCIONES

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
    
    
# Find number block that has certain condition for a subject

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
    

    
def mean_alongtrials(matrix,subject_number, stim_cond, resp_cond):
    condition = Find_cond(Condition_vector,stim_cond,resp_cond)

    long_trial = len(matrix[subject_number][condition][0])
    cant_trials = len(matrix[subject_number][condition])
    
    mean_along_trials = []
    std_along_trials = []
    for j in range(cant_trials):
        mean_along_trials.append(np.mean(matrix[subject_number][condition][j]))
        std_along_trials.append(np.std(matrix[subject_number][condition][j])/np.sqrt(len(matrix[subject_number][condition][j]))) 
        
    return mean_along_trials, std_along_trials, long_trial
  


def mean_acrosstrials(matrix, subject_number, stim_cond, resp_cond):
    condition = Find_cond(Condition_vector,stim_cond,resp_cond)

    long_trial = len(matrix[subject_number][condition][0])
    cant_trials = len(matrix[subject_number][condition])
    
    mean_across_trials = []
    std_across_trials = []
    for j in range(long_trial):
        column_to_mean = []
        for i in range(cant_trials):
            column_to_mean.append(matrix[subject_number][condition][i][j])
        mean_across_trials.append(np.mean(column_to_mean))
        std_across_trials.append(np.std(column_to_mean)/np.sqrt(len(column_to_mean))) 
        
    return mean_across_trials, std_across_trials, long_trial
    
    
#%% After running this block you'll have an allsubjects_matrix which will contain all valid trials (already cleaned up from the transition part) for all conditions for all subjects.
# So it would respond with something like this:
#    allsubjects_matrix[i] is the matrix of subject i-1 in which each element is a matrix per condition for that subject.
#       allsubjects_matrix[i][j] is the matrix of subject i-1 in the condition j in which each element is a vector with a trial for that condition for that subject.
#           allsubjects_matrix[i][j][k] is the vector of subject i-1 in the condition j in the trial k, in which each element is a value of asynchrony.

# So for calling the trial 10 in condition BB for subject 002 you would have to call:   allsubjects_matrix[3][2][10]. Note that condition BB is in position 2 in the Condition_vector.                   

Condition_vector= [['L','L'],['R','R'],['B','B'],['R','L'],['L','R']]
cant_cond = len(Condition_vector)
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
                    plt.figure()
                    plt.figure(figsize=(10,8))

                    plt.plot(asynch_notTrans,'.-', label = 'Trial %d' % trial)
                    plt.hlines(trial_mean,0,40,color='k',linestyle='solid',label='Asincronia promedio')
                    plt.hlines(trial_mean-threshold_outliers,0,40,color='gray',linestyle='dashed')
                    plt.hlines(trial_mean+threshold_outliers,0,40,color='gray',linestyle='dashed')
                    plt.xlabel('# bip',fontsize=18)
                    plt.ylabel('Asincronia[ms]',fontsize=18)
                    plt.xticks(fontsize = 18)
                    plt.yticks(fontsize = 18)
                    plt.grid(True)  
                    plt.legend(fontsize = 15)
                    #plt.title('Trial Outlier - Sujeto %s, Condicion %s%s' % (subject_number,cond_pair[0],cond_pair[1]),fontsize=15)

                    #plt.savefig('trials_outliers_S%s_%s%s_Trial%i.png' % (subject_number,cond_pair[0],cond_pair[1],trial))
                    
                # If all asynchronies are whithin the mean+/-threshold, then we append it to the matrix    
                else:
                    trials_matrix.append(asynch_notTrans)
                    
            else:
                print("Asynch vector is not long enough")
                break
            
        onesubject_matrix.append(trials_matrix)
    
    allsubjects_matrix.append(onesubject_matrix)
    
    
# En esta instancia tengo una matriz con todos los trials válidos de un sujeto, ya sin el transitorio y que pasaron por el criterio de outliers.
# Sobre esta matriz corro la rutina que forma los vectores para los gráficos 2, ya que sobre esa info aplico los criterios para saber si un sujeto es outlier (drifting y distribución de promedios).

#%%
# Para usar los criterios para saber si un sujeto es outlier, primero necesito calcular el promedio across trials para cada uno.
# Para eso, armo matrices: Primero fijo una condicion y corro la función "mean_acrosstrials" usando la matriz de allsubjects_matrix para todos los sujetos. Los elementos de acrosstrials_allmatrix_value serán matrices, una por cada condicion. Los elementos de acrosstrials_allmatrix_value[i] serán vectores, uno por cada sujeto (al elegir el indice [i] ya nos paramos en una cierta condicion), que contengan el promedio across trials para cada numero de beep.                                                                                                                                                                                                                                                                   acrosstrials_allmatrix_err sigue la misma lógica pero con los errores de acrosstrials_allmatrix_value, y acrosstrials_allmatrix_mean contiene los valores promedios de los vectores de acrosstrials_allmatrix_value[i].
    

acrosstrials_allmatrix_value = []
acrosstrials_allmatrix_err = []
acrosstrials_allmatrix_mean = []
for cond_pair in Condition_vector:
    acrosstrials_allmatrix_value_percond = []
    acrosstrials_allmatrix_err_percond = []
    acrosstrials_allmatrix_mean_percond = []
    for i in range(total_number_subjects):
        acrosstrials_allmatrix_value_percond.append(mean_acrosstrials(allsubjects_matrix,i,cond_pair[0],cond_pair[1])[0])
        acrosstrials_allmatrix_mean_percond.append(np.mean(mean_acrosstrials(allsubjects_matrix,i,cond_pair[0],cond_pair[1])[0]))
        acrosstrials_allmatrix_err_percond.append(mean_acrosstrials(allsubjects_matrix,i,cond_pair[0],cond_pair[1])[1])
        long_trial = mean_acrosstrials(allsubjects_matrix,i,cond_pair[0],cond_pair[1])[2]
    acrosstrials_allmatrix_value.append(acrosstrials_allmatrix_value_percond)
    acrosstrials_allmatrix_mean.append(acrosstrials_allmatrix_mean_percond)
    acrosstrials_allmatrix_err.append(acrosstrials_allmatrix_err_percond)

# Antes de pasar por los criterios de drifting y distribucion de promedios, creo un vector que tenga los numeros de sujetos (que por ahora son todos). Así, si alguno resulta outlier, puedo descontarlo de ese vector, que luego voy a usar de referencia para crear la matriz "final" de datos.

all_subjects_number = list(np.arange(1,total_number_subjects+1))



# CRITERIO DE DRIFTING

max_dif_accept = 20

for cond_number in range(cant_cond):
    for subj_number in range(total_number_subjects):
        x_firsthalf = np.mean(acrosstrials_allmatrix_value[cond_number][subj_number][0:15])
        x_secondhalf = np.mean(acrosstrials_allmatrix_value[cond_number][subj_number][15:40])
        
        if abs(x_firsthalf-x_secondhalf)> max_dif_accept:
            print('El sujeto S00%i tiene drift en la condicion %s%s' % (subj_number+1, Condition_vector[cond_number][0],Condition_vector[cond_number][1]))
            plt.plot(acrosstrials_allmatrix_value[cond_number][subj_number])
            plt.xlabel('# beep',fontsize=15)
            plt.ylabel('Asincronia[ms]',fontsize=15)
            plt.xticks(fontsize = 15)
            plt.yticks(fontsize = 15)
            plt.grid(True)  
            plt.title('Trial con Drifting - Sujeto %i, Condicion %s%s' % (subj_number+1,Condition_vector[cond_number][0],Condition_vector[cond_number][1]))
            # plt.savefig(...)
            
            all_subjects_number.remove(subj_number+1)


# CRITERIO DE DISTRIBUCION DE PROMEDIOS

for cond_number in range(cant_cond):
    plt.figure(figsize=(10,8))
    x = acrosstrials_allmatrix_mean[cond_number]
    sns.distplot(x);
    perc_25 = np.percentile(x,25)
    perc_75 = np.percentile(x,75)
    iqr = perc_75 - perc_25
    lim_sup = perc_75 + 1.5*iqr
    lim_inf = perc_25 - 1.5*iqr
    
    for i in all_subjects_number:
        if x[i-1] > lim_sup:
            plt.axvline(x[i-1], color = 'red', label = 'S00%i' % (i))
            all_subjects_number.remove(i)
        elif x[i-1] < lim_inf:
            plt.axvline(x[i-1], color = 'red', label = 'S00%i' % (i))
            all_subjects_number.remove(i)

    plt.axvline(perc_25)
    plt.axvline(perc_75)
    plt.xlabel('Asincronia promedio[ms]',fontsize=15)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid()  
    plt.legend()
    plt.title('Condicion %s%s' % (Condition_vector[cond_number][0],Condition_vector[cond_number][1]),fontsize=15)   
    # plt.savefig(...

#%% Ahora re armo la matriz pero usando solo los sujetos que no quedaron como outliers y la guardo en un npz junto con el vector de los sujetos no-outliers.

validsubjects_matrix = []

for i in all_subjects_number:
    validsubjects_matrix.append(allsubjects_matrix[i-1])


# Vuelvo a calcular los means across trial pero ahora con los sujetos buenos (es mas facil recalcular que appendear la matrix ya hecha porque está primero por condición y no por sujeto)
acrosstrials_validmatrix_value = []
acrosstrials_validmatrix_err = []
for cond_pair in Condition_vector:
    acrosstrials_validmatrix_value_percond = []
    acrosstrials_validmatrix_err_percond = []
    for i in range(len(validsubjects_matrix)):
        acrosstrials_validmatrix_value_percond.append(mean_acrosstrials(validsubjects_matrix,i,cond_pair[0],cond_pair[1])[0])
        acrosstrials_validmatrix_err_percond.append(mean_acrosstrials(validsubjects_matrix,i,cond_pair[0],cond_pair[1])[1])
        
    acrosstrials_validmatrix_value.append(acrosstrials_validmatrix_value_percond)
    acrosstrials_validmatrix_err.append(acrosstrials_validmatrix_err_percond)    
       
    
# y ahora calculo los promedios along trials   
 
alongtrials_validmatrix_value = []
alongtrials_validmatrix_err = []

for cond_pair in Condition_vector:
    alongtrials_validmatrix_value_percond = []
    alongtrials_validmatrix_err_percond = []

    for i in range(len(validsubjects_matrix)):
        alongtrials_validmatrix_value_percond.append(mean_alongtrials(validsubjects_matrix,i,cond_pair[0],cond_pair[1])[0])
        alongtrials_validmatrix_err_percond.append(mean_alongtrials(validsubjects_matrix,i,cond_pair[0],cond_pair[1])[1])
        
    alongtrials_validmatrix_value.append(alongtrials_validmatrix_value_percond)
    alongtrials_validmatrix_err.append(alongtrials_validmatrix_err_percond)
    
    
# y ahora guardo todo en un archivo
    
    
filename_validsubjects = 'valid_subjects_data'

np.savez_compressed(filename_validsubjects, validsubjects = all_subjects_number, validsubjects_data = validsubjects_matrix, acrosstrials_value = acrosstrials_validmatrix_value, acrosstrials_err = acrosstrials_validmatrix_err, alongtrials_value = alongtrials_validmatrix_value, alongtrials_err = alongtrials_validmatrix_err)