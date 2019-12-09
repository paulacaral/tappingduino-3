# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:04:30 2019

@author: paula
"""

import serial, time
import numpy as np
import matplotlib.pyplot as plt
import random
import os

#%% Description

#==============================================================================
# Saves:  - a file per block containing information about all trials in it: their condition and whether if they were valid or not
#         - a file per trial containing the raw data from it
#         - a file per trial containing extracted data from it
#==============================================================================

#%% Communicate with arduino

arduino = serial.Serial('/dev/ttyACM0', 9600)
#arduino = serial.Serial('/COM4', 9600)

#%% mensaje de prueba

message = ";S%c;F%c;N%c;A%d;I%d;n%d;X" % ('L', 'B','B', 1, 500, 50)
arduino.write(message)

#%% definitions

ISI = 500;		# interstimulus interval (milliseconds)
n_stim = 10;	# number of bips within a sequence

# all possible conditions for stimulus and feedback
all_conditions = [['L','L'], ['L','R'], ['L','N'], ['R','L'], ['R','R'], ['R','N'], ['B','L'], ['B','R'], ['B','N']];

# condition dictionary so we can choose the condition without going through number position
condition_dictionary = {"LL": 0,"LR": 1,"LN": 2,"RL": 3,"RR": 4,"RN": 5,"BL": 6,"BR": 7,"BN": 8};

# conditions chosen for the experiment
conditions_chosen_index = [
  condition_dictionary["LL"],
  condition_dictionary["LR"],
  condition_dictionary["RL"],
  condition_dictionary["RR"]
];

# total number of blocks
N_blocks = 2;
# number of trials per condition per block
N_trials_per_block_per_cond = 2;

#%% names

filename_names = "Dic_names_pseud.dat"

try:
    f_names = open(filename_names,"r")

    if os.stat(filename_names).st_size == 0:
        #print('esta vacio')        
        next_subject_number = '001';
        f_names.close();
    else:
        #print('tiene algo')
        content = f_names.read();
       #print(content[-3:]);
        last_subject_number = int(content [-3:]);
        next_subject_number = '{0:0>3}'.format(last_subject_number + 1);
        #print(next_subject_number)
        f_names.close()
        
except IOError:
    print('El archivo no esta donde deberia, ubicalo en la carpeta correcta y volve a correr esta celda')       

# set subject name for filename
name = raw_input("Ingrese su nombre: ") 

f_names = open(filename_names,"a")
f_names.write('\n'+name+'\tS'+next_subject_number)
f_names.close()

 
#%% run blocks

for (block in range(N_blocks)):
    
    condition_vector = [] # vector that will contain each condition the specified amount of times (it's important to restart it here!)
    for i in range(N_trials_per_block_per_cond):
        for j in conditions_chosen_index:
            condition_vector.append(all_conditions[j])
    # total number of trials per block
    N_trials_per_block = len(condition_vector)
    
    random.shuffle(condition_vector) # shuffle condition_vector to get aleatory order in the conditions

    Stim_conds = [] # vector that will contain all stimulus conditions
    Fdbk_conds = [] # vector that will contain all feedback conditions
    for i in range(len(condition_vector)):
        Stim_conds.append(condition_vector[i][0])
        Fdbk_conds.append(condition_vector[i][1])
    
    # run one block
    raw_input("Press Enter to start block")    
    
    # set time for file name
    timestr = time.strftime("%Y_%m_%d-%H.%M.%S")
    
    # trial counter
    trial = 0
    
    conditions = [] # vector that will contain exact message sent to arduino to register the conditions played in each trial
    valid_trial = [] # vector that will contain 1 if the trial was valid or 0 if it wasn't
    
    # generate filename for file that will contain all conditions used in the trial along with the valid_trials vector    
    filename_block = 'S'+next_subject_number+"-"+timestr+"-"+"block"+str(block)+"-trials" 
    
    while (trial < N_trials_per_block):
        raw_input("Press Enter to start trial (%d/%d)" % (trial,N_trials_per_block));
    
        # generate raw data file 
        filename_raw = 'S'+next_subject_number+"-"+timestr+"-"+"block"+str(block)+"-"+"trial"+str(trial)+"-raw.dat"
        f_raw = open(filename_raw,"w+")
     
        # generate extracted data file name (will save raw data, stimulus time, feedback time and asynchrony)
        filename_data = 'S'+next_subject_number+"-"+timestr+"-"+"block"+str(block)+"-"+"trial"+str(trial)
            
        # wait random number of seconds before actually starting the trial
        wait = random.randrange(10,20,1)/10.0
        time.sleep(wait)
        
        # define stimulus and feedback condition for this trial
        Stim = Stim_conds[trial];
        Resp = Fdbk_conds[trial];
          
        # send message with conditions to arduino
        message = ";S%c;F%c;N%c;A%d;I%d;n%d;X" % (Stim, Resp,'B', 3, ISI, n_stim)
        arduino.write(message)
        conditions.append(message)
        
        # read information from arduino
        data = []
        aux = arduino.readline()
        while (aux[0]!='E'):
            data.append(aux);
            f_raw.write(aux); # save raw data
            aux = arduino.readline();
            
        # Separates data in type, number and time
        e_total = len(data)
        e_type = []
        e_number = []
        e_time = []
        for event in data:
            e_type.append(event.split()[0])
            e_number.append(int(event.split()[1]))
            e_time.append(int(event.split()[2]))
        
        # Separates number and time according to if it comes from stimulus or response
        stim_number = []
        resp_number = []
        stim_time = []
        resp_time = []
        for events in range(e_total):
            if e_type[events]=='S':
                stim_number.append(e_number[events])
                stim_time.append(e_time[events])
                
            if e_type[events]=='R':
                resp_number.append(e_number[events])
                resp_time.append(e_time[events])
    
        # determine number of stimulus and responses registered
        N_stim = len(stim_time)
        N_resp = len(resp_time)
    
        # close raw data file    
        f_raw.close()
        
        # ---------------------------------------------------------------
        # Asynchronies calculation
    
        # vector that will contain asynchronies if they are calculated
        asynchrony = []
        
        if N_resp > 0: # if there were any responses
        
            j = 0 # stimulus counter
            i = N_resp-1 # responses counter
            
            # find first stimulus with a response
            while j < N_stim:
                diff = stim_time[j]-resp_time[0]
                if abs(diff)<200:
                    first_stim_responded_index = j
                    break;
                else:
                    j = j+1
            
            # find response to last stimulus (last response that should be considerated)
            while i > 0:
                diff = stim_time[N_stim-1]-resp_time[i]
                if abs(diff)<200:
                    last_resp_index = i+1
                    break;
                else:
                    i = i-1
            
            # new vectors of stimulus and responses that only contain those that have a pair of the other type        
            stim_paired = stim_time[first_stim_responded_index:]
            resp_paired = resp_time[0:last_resp_index]
            N_stim_paired = len(stim_paired)
            N_resp_paired = len(resp_paired)
            
             
            if N_stim_paired == N_resp_paired:
                        
                # the trial is valid! then:
                valid_trial.append(1)
                
                # Calculate and save asynchronies
                for k in range(N_stim_paired):
                    asynchrony.append(stim_paired[k]-resp_paired[k])
    
               
            #==============================================================================
            # Plot all pair of stimulus and feedback
                my_labels = {"stim" : "Stimulus", "resp" : "Feedback"}
                for j in range(N_stim_paired):
                    plt.axvline(x=stim_paired[j],color='y',linestyle='dashed',label=my_labels["stim"])
                    my_labels["stim"] = "_nolegend_"
                
                for k in range(N_resp_paired):
                    plt.axvline(x=resp_paired[k],color='c',label=my_labels["resp"])
                    my_labels["resp"] = "_nolegend_"
                    
                plt.axis([min(resp_paired)-50,max(stim_paired)+50,0,1])
                  
                plt.xlabel('Tiempo[ms]',fontsize=12)
                plt.ylabel(' ')
                plt.grid()    
                plt.legend(fontsize=12)
                #plt.show()  
            #==============================================================================
            
        
            #==============================================================================
            # Plot asynchronies
                plt.figure()
                plt.plot(asynchrony,'.')
                plt.xlabel('# beep',fontsize=12)
                plt.ylabel('Asynchrony[ms]',fontsize=12)
                plt.grid()    
                #plt.show()   
            #==============================================================================
        
                # go to next trial
                trial = trial + 1;
            
            else:
                # trial is not valid! then:
                valid_trial.append(0)
                
                # appends conditions for this trial at the end of the conditions vectors, so that it can repeat at the end
                Stim_conds.append(Stim_conds[trial])
                Fdbk_conds.append(Fdbk_conds[trial])
        
                # Warn subject the trial will be repeated
                print("Te salteaste un estimulo, hay que repetir el trial")
                
                # go to next trial
                trial = trial + 1;
                # add 1 to number of trials per block since will have to repeat one
                N_trials_per_block = N_trials_per_block + 1;
    
                    
        else: # if there were no responses
            
            # trial is not valid! then:
            valid_trial.append(0)
            
            # appends conditions for this trial at the end of the conditions vectors, so that it can repeat at the end
            Stim_conds.append(Stim_conds[trial])
            Fdbk_conds.append(Fdbk_conds[trial])
          
            # warn subject the trial will be repeated
            print("No hubo respuestas, hay que repetir el trial")
          
            # go to next trial
            trial = trial + 1;
            # add 1 to number of trials per block since will have to repeat one
            N_trials_per_block = N_trials_per_block + 1;
    
        # SAVE DATA FROM TRIAL (VALID OR NOT)
        np.savez_compressed(filename_data, raw=data, stim=stim_time, resp=resp_time, asynch=asynchrony)
            
    # SAVE DATA FROM BLOCK (VALID AND INVALID TRIALS AND THEIR CONDITIONS)    
    np.savez_compressed(filename_block,trials=valid_trial,conditions=conditions)
    
    print("Fin del bloque!")


#%% Loading data

npztrial = np.load(filename_block+".npz")
# sorted(npztrial) # Me muestra todo lo que tiene adentro
npztrial["trials"]
npztrial["conditions"]


trial1 = np.load(filename_data+".npz")

trial1["raw"]
trial1["stim"]
trial1["resp"]
trial1["asynch"]