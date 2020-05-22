# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 11:58:54 2020

@author: Paula
"""


import numpy as np
import glob

#%%

def Corregir_validez_trials(subject_number,block,trial_to_modify,validation,error):
    filename = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal\S'+subject_number+"*-block"+str(block)+"-trials.npz")
    filedic = dict(np.load(filename[0]))
    filedic['trials'][trial_to_modify]=validation
    filedic['errors'][trial_to_modify]=error
    alltrials = []
    allerrors = []
    for i in range(len(filedic['trials'])):
        alltrials.append(filedic['trials'][i])
        allerrors.append(filedic['errors'][i])
    
    print(alltrials)
    print(allerrors)
    
    check = raw_input('if modifications are correct, type Y. Else, just click ENTER: ')
    if check == 'Y':
        np.savez(filename[0], **filedic)
        print('Modifications done')
    else:
        raise
        
        
#%%

def Corregir_signos_asynch(subject_number,cant_total_block):
    for block in range(cant_total_block):
        aux = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"-*-block"+str(block)+"-trial*.npz")
        for trial in range(len(aux)-1):
            filename = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"-*-block"+str(block)+"-trial"+str(trial)+".npz")
            filedic = dict(np.load(filename[0]))
            for i in range(len(filedic['asynch'])):
                filedic['asynch'][i]=-filedic['asynch'][i]
                
            np.savez(filename[0], **filedic)

#%%

def Check_signs(subject_number):
    for block in range(5):
        aux = glob.glob(r'C:\Users\Paula\Documents\Facultad\Tesis de licenciatura\tappingduino 3\Analisis de datos\Experimento Piloto Dic2019\DATOS - Piloto Dic 2019 - CorregidosTrialsFalsosVal/S'+subject_number+"-*-block"+str(block)+"-trial*.npz")
        for trial in range(len(aux)-1):
            a = Loading_data(subject_number,block,trial,'asynch')
            b = Loading_data_orig(subject_number,block,trial,'asynch')
            
            a_ = a[0]
            b_ = b[0]
            for i in range(len(a_)):
                if (a_[i] == -b_[i]):
                    pass
                else:
                    print('oops, chequea')
                    print(block)
                    print(trial)
                    break

            print('todo bien por acá')

