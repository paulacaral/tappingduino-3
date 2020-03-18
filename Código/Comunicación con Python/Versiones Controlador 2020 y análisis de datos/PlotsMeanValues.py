# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 09:25:03 2020

@author: Paula
"""

import numpy as np
import matplotlib.pyplot as plt
import glob

#%%

stim_cond = 'L'
resp_cond = 'L'
total_number_subjects = 5

mean_values_all_subjects = []
for i in range(1,(total_number_subjects+1)):
    mean_values_all_subjects.append(Mean_value_block('{0:0>3}'.format(i),stim_cond,resp_cond))
    
plt.plot(mean_values_all_subjects,'.',label='condition %s %s' % (stim_cond, resp_cond))
plt.xlabel('Sujeto',fontsize=12)
plt.ylabel('Mean Value Asynchrony[ms]',fontsize=12)
plt.legend()
plt.grid() 