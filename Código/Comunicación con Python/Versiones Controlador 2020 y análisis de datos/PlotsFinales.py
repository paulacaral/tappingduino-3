# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 14:13:56 2020

@author: Paula
"""

import numpy as np
import matplotlib.pyplot as plt
import glob


#%% Cargo el archivo que salió de LimpiezaDatos.py

npz = np.load('valid_subjects_data.npz')

subjects = npz['validsubjects'] # Vector con los numeros de sujetos "buenos"
subjects_data = npz['validsubjects_data'] # Matrix con toda la información de estos sujetos ordenada por: nro de sujeto > condicion > trial > numero de beep
acrosstrials_value = npz['acrosstrials_value'] # Matriz resultante de hacer el promedio across trials para cada sujeto en cada condicion. Ahora el orden es: condicion > sujeto > 1 trial promedio > numero de beep
acrosstrials_err = npz['acrosstrials_err'] # Matriz con los errores de los valores anteriores
alongtrials_value = npz['alongtrials_value'] # Matriz resultante de hacer el promedio along trials para cada sujeto en cada condicion. Ahora el orden es: condicion > sujeto > promedios de trials > numero de trial
alongtrials_err = npz['alongtrials_err'] # Matriz con los errores de los valores anteriores

Condition_vector= [['L','L'],['R','R'],['B','B'],['R','L'],['L','R']]
total_number_subjects = len(subjects)
long_trial = len(subjects_data[0][0][0])
cant_conds = len(Condition_vector)

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
               
            
def Plot_alltrials(subject_number, stim_cond, resp_cond):
    condition = Find_cond(Condition_vector,stim_cond,resp_cond)
    
    plt.figure(figsize=(10,8))
    for trial_number in range(len(subjects_data[subject_number-1][condition])):
        plt.plot(subjects_data[subject_number-1][condition][trial_number],'.-', label = 'trial %d' % trial_number)
        
    plt.xlabel('# beep',fontsize=15)
    plt.ylabel('Asincronia[ms]',fontsize=15)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid(True)  
    plt.legend()
    plt.title('Todos los trials validos del sujeto %s en la condicion %s%s' % (subject_number,stim_cond,resp_cond),fontsize=15)
    #plt.savefig('Asynch_S005_RL_T11.png')

    return
            
          

# DEFINO COLORES PARA LOS PLOTS
cmap = plt.get_cmap('Dark2_r')
colors = [cmap(i) for i in np.linspace(0, 1, total_number_subjects)]  

#%% PLOT FINAL 0: Distribucion de asincronias (histograma) para un sujeto en una condición (es para el esquema de la figura 1)

import seaborn as sns

y = []
for j in range(len(subjects_data[0][3])):
    for i in range(len(subjects_data[0][3][0])):
        y.append(subjects_data[0][3][j][i])
        
sns.distplot(y)
plt.xlabel('$e_n$[ms]',fontsize=18)  
plt.savefig('distrib_asinc_esquema.png')          
#%% PLOT FINAL i: asyn vs bip single trial de un sujeto muestra (SM) en BB.

SM_i = 1 # Notar que el numero "1" en la nueva matriz de data ya no se corresponde con el numero "real" del sujeto.
Cond_i = Find_cond(Condition_vector, 'B','B')
trial_i = 11                                                                

#plt.figure(figsize=(10,8))
plt.figure(figsize=(12,6))
asynch = subjects_data[SM_i-1][Cond_i][trial_i]
plt.plot(asynch,'.-',color=colors[0])
plt.xlabel('# bip',fontsize=22)
plt.ylabel('$e_n$[ms]',fontsize=22)
#plt.ylabel('Asincronia[ms]',fontsize=18)
plt.grid(True) 
plt.xticks(fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid(True)  
#plt.title('Asincronia en cada estimulo para el sujeto S%s en la condicion BB' % SM_i)
plt.savefig('SingleTrial_esquema.png')



#%% PLOT FINAL iii: Todos los trials de un SM en BB (Gráfico tipo 1). 

SM_ii = 1
                                                    
Plot_alltrials(SM_ii,'B','B')

#%% PLOT FINAL iv: Todos los sujetos un gráfico por cada condición (Gráficos tipo 2).
 
# X axis
beeps = np.arange(long_trial)

for cond_number in range(cant_conds):
    plt.figure(figsize=(10,8))
    
    for subj_number, color in enumerate(colors, start=0):
        plt.errorbar(beeps,acrosstrials_value[cond_number][subj_number],acrosstrials_err[cond_number][subj_number],color = color, fmt='.-',label='S00%i' % int(subj_number+1))

    # To add the mean value of all subjects for a given condition, uncomment this next line        
    #plt.axhline(np.mean(acrosstrials_value[cond_number]),linestyle='solid',color='k', label='Mean all S')    

    plt.xlabel('# beep',fontsize=15)
    plt.ylabel('Asincronia[ms]',fontsize=15)
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    plt.grid(True)  
    plt.legend()
    plt.title('Promedio across trials de cada sujeto para la condicion %s%s' % (Condition_vector[cond_number][0],Condition_vector[cond_number][1]),fontsize=15)   
#    plt.savefig('mean_across_trials_%s%s_sinOutliers.png' % (Condition_vector[cond_number][0],Condition_vector[cond_number][1]))   
                                                    
                                                    
#%% PLOT FINAL v y vi: Gráfico de asyn media, 5 condiciones en el eje x: una línea para el valor medio total con incertezas + 1 línea por cada sujeto sin incerteza (Gráfico 5 + Gráfico 7 sin incertezas). Idem std media (Gráfico 6 + Gráfico 8 sin incertezas).

alongtrials_mean = []
alongtrials_mean_err = []
alongtrials_std = []
alongtrials_std_err = []

for cond_number in range(cant_conds):
    
    alongtrials_mean_percond = []
    alongtrials_mean_err_percond = []
    alongtrials_std_percond = []
    alongtrials_std_err_percond = []

    for subj_number in range(total_number_subjects):
        alongtrials_mean_percond.append(np.mean(alongtrials_value[cond_number][subj_number]))
        alongtrials_mean_err_percond.append(np.std(alongtrials_value[cond_number][subj_number])/np.sqrt(len(alongtrials_value[cond_number][subj_number]))) 
        
        alongtrials_std_percond.append(np.mean(alongtrials_err[cond_number][subj_number]))
        alongtrials_std_err_percond.append(np.std(alongtrials_err[cond_number][subj_number])/np.sqrt(len(alongtrials_err[cond_number][subj_number])))
        
        
    alongtrials_mean.append(alongtrials_mean_percond)
    alongtrials_mean_err.append(alongtrials_mean_err_percond)

    alongtrials_std.append(alongtrials_std_percond)
    alongtrials_std_err.append(alongtrials_std_err_percond)
    
    
# En este último paso calculé el promedio de los vectores que contienen el valor promedio de cada trial,  para cada sujeto, para cada condicion. Y el valor de la desviacion estandar en las mismas condiciones (vector error del de promedios). A su vez, calculé la desviacion estandar de ambos vectores. Esto me permite hacer un gráfico del estilo Mean asynch vs Condiciones (una linea por sujeto) o bien Std asynch vs Condiciones (una linea por sujeto). 
# Los vectores de errores (alongtrials_mean_err y alongtrials_std_err) no hacen falta porque estas curvas van a ir sin errores para no entorpecer visualmente el gráfico. Pero bueno, quedan calculadas.

# Voy a transponer los vectores para que queden ordenados por sujeto (ya que para el plot quiero una linea por sujeto)

alongtrials_mean_tr = np.array(alongtrials_mean).transpose()                        
alongtrials_mean_err_tr = np.array(alongtrials_mean_err).transpose()                        

alongtrials_std_tr = np.array(alongtrials_std).transpose()                        
alongtrials_std_err_tr = np.array(alongtrials_std_err).transpose()                        
                          
# A esas curvas además quiero agregar la curva de promediar "across subjects" esos valores para cada condición, entonces:


alongtrials_mean_acrosssubjects = []
alongtrials_mean_acrosssubjects_err = []
alongtrials_std_acrosssubjects = []
alongtrials_std_acrosssubjects_err = []

for cond_number in range(cant_conds):
    alongtrials_mean_acrosssubjects.append(np.mean(alongtrials_mean[cond_number]))
    alongtrials_mean_acrosssubjects_err.append(np.std(alongtrials_mean[cond_number])/np.sqrt(len(alongtrials_mean[cond_number])))
    
    alongtrials_std_acrosssubjects.append(np.mean(alongtrials_std[cond_number]))
    alongtrials_std_acrosssubjects_err.append(np.std(alongtrials_std[cond_number])/np.sqrt(len(alongtrials_std[cond_number])))
    

# Ahora si grafico las curvas

# Eje x
CC = np.arange(5)

plt.figure(figsize=(10,8))
plt.errorbar(CC,alongtrials_mean_acrosssubjects,alongtrials_mean_acrosssubjects_err,color='k',fmt='*-',label='Promedio sobre todos los sujetos',capsize=10)

for subj_number, color in enumerate(colors, start=0):
    plt.plot(CC,alongtrials_mean_tr[subj_number],'*-',markersize=10, color=color,label = 'S00%i' % int(subj_number+1))

plt.xlabel('Condiciones ',fontsize=15)
plt.ylabel('Asincronia promedio[ms]',fontsize=15)
labels = ['LL', 'RR', 'BB','RL','LR']
plt.xticks(CC,labels, fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid(True)  
plt.legend(fontsize=15)
plt.title('Promedio along y across trials para cada sujeto en cada condicion')



plt.figure(figsize=(10,8))
plt.errorbar(CC,alongtrials_std_acrosssubjects,alongtrials_std_acrosssubjects_err,color='k',fmt='*-',label='Promedio sobre todos los sujetos',capsize=10)

for subj_number, color in enumerate(colors, start=0):
    plt.plot(CC,alongtrials_std_tr[subj_number],'*-',markersize=10, color=color,label = 'S00%i' % int(subj_number+1))

plt.xlabel('Condiciones ',fontsize=15)
plt.ylabel('Desviacion estandar promedio de asincronia[ms]',fontsize=15)
labels = ['LL', 'RR', 'BB','RL','LR']
plt.xticks(CC,labels, fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid(True)  
plt.legend(fontsize=15)
plt.title('Desviacion estandar along trials + promedio across trials para cada sujeto en cada condicion')


#%% Plot final vii y viii: Repeated measures two-way anova para asyn media y std media (Gráfico 5.1 y 6.1 + Tablas)

import pyvttbl as pt
from collections import namedtuple

# Hago el plot Asincronia promedio vs Par Stim-Fdbk para Stim Left y Stim Right

print('PARA LA ASINCRONIA PROMEDIO')

Par_ID = np.arange(2)

Y_SL = [alongtrials_mean_acrosssubjects[0],alongtrials_mean_acrosssubjects[4]] # LL y LR
Y_SL_err = [alongtrials_mean_acrosssubjects_err[0],alongtrials_mean_acrosssubjects_err[4]] # Sus errores


Y_SR = [alongtrials_mean_acrosssubjects[1],alongtrials_mean_acrosssubjects[3]] # RR y RL
Y_SR_err = [alongtrials_mean_acrosssubjects_err[1],alongtrials_mean_acrosssubjects_err[3]] # Sus errores

plt.figure(figsize=(10,8))
plt.errorbar(Par_ID,Y_SL,Y_SL_err,color='k',fmt='*-',label='Stim L',capsize=10)
plt.errorbar(Par_ID,Y_SR,Y_SR_err,fmt='*-',label='Stim R',capsize=10,color=colors[1])
plt.xlabel('Par Stim-Fdbk',fontsize=15)
plt.ylabel('Asincronia promedio[ms]',fontsize=15)
labels = ['Same', 'Diff']
plt.xticks(Par_ID,labels, fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)

# Corro el test repeated measures two way anova para estos datos

N = len(subjects)
Par = ['I','D'] # Factor par Stim - Fdbk, si son iguales(I) o diferentes (D)
Lateralidad_stim = ['SL','SR'] # Factor lateralidad tomando de referencia el estimulo


sub_id = [i+1 for i in xrange(N)]*(len(Par)*len(Lateralidad_stim))
Par_ID_tabla = np.concatenate([np.array([p]*N) for p in Par]*len(Lateralidad_stim)).tolist()
LatStim_LR = np.concatenate([np.array([l]*(N*len(Par))) for l in Lateralidad_stim]).tolist()

# Así como está entonces los tengo que ordenar como LL, LR, RR y RL (en ese orden)

mean_dataLL = alongtrials_mean[0] # LL
mean_dataRR = alongtrials_mean[1] # RR
mean_dataRL = alongtrials_mean[3] # RL
mean_dataLR = alongtrials_mean[4] # LR
                               
mean_data = np.concatenate([mean_dataLL,mean_dataLR,mean_dataRR,mean_dataRL])

Sub = namedtuple('Sub', ['Sub_id', 'mean_data','Par_ID', 'LatStim_LR'])               
df = pt.DataFrame()

for idx in xrange(len(sub_id)):
    df.insert(Sub(sub_id[idx],mean_data[idx], Par_ID_tabla[idx],LatStim_LR[idx])._asdict())


aov_mean = df.anova('mean_data', sub='Sub_id', wfactors=['Par_ID', 'LatStim_LR'])
print(aov_mean)




print('PARA LA DESVIACION ESTANDAR PROMEDIO')

# Lo mismo pero con desviacion estandar

Y_std_SL = [alongtrials_std_acrosssubjects[0],alongtrials_std_acrosssubjects[4]] # LL y LR
Y_std_SL_err = [alongtrials_std_acrosssubjects_err[0],alongtrials_std_acrosssubjects_err[4]] # Sus errores


Y_std_SR = [alongtrials_std_acrosssubjects[1],alongtrials_std_acrosssubjects[3]] # RR y RL
Y_std_SR_err = [alongtrials_std_acrosssubjects_err[1],alongtrials_std_acrosssubjects_err[3]] # Sus errores

plt.figure(figsize=(10,8))
plt.errorbar(Par_ID,Y_std_SL,Y_std_SL_err,color='k',fmt='*-',label='Stim L',capsize=10)
plt.errorbar(Par_ID,Y_std_SR,Y_std_SR_err,fmt='*-',label='Stim R',capsize=10,color=colors[1])
plt.xlabel('Par Stim-Fdbk',fontsize=15)
plt.ylabel('Desviacion estandar promedio de asincronias[ms]',fontsize=15)
labels = ['Same', 'Diff']
plt.xticks(Par_ID,labels, fontsize = 15)
plt.yticks(fontsize = 15)
plt.grid()  
plt.legend(fontsize=15)


# corro el test

std_dataLL = alongtrials_std[0] # LL
std_dataRR = alongtrials_std[1] # RR
std_dataRL = alongtrials_std[3] # RL
std_dataLR = alongtrials_std[4] # LR
                               
std_data = np.concatenate([std_dataLL,std_dataLR,std_dataRR,std_dataRL])

# Para ahorrarme tener que poner esto asi "a mano", podria cambiar el orden del vector de conditions.. pero eso cambia los gráficos. Preguntar.


Sub = namedtuple('Sub', ['Sub_id', 'std_data','Par_ID', 'LatStim_LR'])               
df = pt.DataFrame()

for idx in xrange(len(sub_id)):
    df.insert(Sub(sub_id[idx],std_data[idx], Par_ID_tabla[idx],LatStim_LR[idx])._asdict())


aov_std = df.anova('std_data', sub='Sub_id', wfactors=['Par_ID', 'LatStim_LR'])
print(aov_std)


#%% TEST DE STUDENT ENTRE (BB,RR) Y (BB,LL).

# Paired Student's t-test

from scipy.stats import ttest_rel, f_oneway

# Para los datos uso los vectores alongtrials_mean que ya les puse nombre antes para el test de anova. Solo me falta definir el de BB que no se usa en ese caso
mean_dataBB = alongtrials_mean[2] # BB

statBBLL, pBBLL = ttest_rel(mean_dataBB, mean_dataLL)
print('Statistics=%.3f, p=%.3f' % (statBBLL, pBBLL))

# Defino alpha
alpha = 0.05

if pBBLL > alpha:
	print('Accept null hypothesis that the means (between BB and LL) are equal.')
else:
	print('Reject the null hypothesis that the means (between BB and LL) are equal.')  


statBBRR, pBBRR = ttest_rel(mean_dataBB, mean_dataRR)
print('Statistics=%.3f, p=%.3f' % (statBBRR, pBBRR))

if pBBRR > alpha:
	print('Accept null hypothesis that the means (between BB and RR) are equal.')
else:
	print('Reject the null hypothesis that the means (between BB and RR) are equal.')  
  

