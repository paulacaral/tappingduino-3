# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:04:30 2019

@author: paula
"""

import serial, time

#%%
arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)

#%% definitions

ISI = 500;		# interstimulus interval (milliseconds)
N_stim = 7;	# number of bips within a sequence


#%%
# fprintf(ardu,'ARDU;I%d;N%d;P%d;B%d;E%d;X',[ISI N_stim 100 10 3]);	% send parameters
message = ";I%d;N%d;P%d;B%d;E%d;X" % (ISI, N_stim, 100, 10, 3)
arduino.write(message)



data = []
aux = arduino.readline()
print(aux)
while (aux[0]!='E'):
    data.append(aux)
    aux = arduino.readline();
#%%
#arduino.readline()

#%%
#==============================================================================
# data = [];
# aux = fgetl(ardu);
# counter = 1;
# while (~strcmp(aux(1),'E'))
# 	data{counter} = aux;
# 	aux = fgetl(ardu);
# 	counter = counter + 1;
# end
#==============================================================================


data = []
aux = arduino.readline()
counter = 1;
while (aux[0]=='E'):
    data[counter] = aux;
    aux = arduino.readline();
    counter = counter + 1;
end