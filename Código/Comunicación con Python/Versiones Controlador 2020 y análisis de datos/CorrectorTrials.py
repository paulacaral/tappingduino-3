# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 11:58:54 2020

@author: Paula
"""


import numpy as np
import matplotlib.pyplot as plt
import os
import glob

#%%

def Corregir_validez_trials(subject_number,block,trial_to_modify,validation,error):
    filename = glob.glob(r'C:\Users\Paula\Desktop\S'+subject_number+"*-block"+str(block)+"-trials.npz")
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
    else:
        raise
        