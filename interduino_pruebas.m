%% Synchronization experiment "manager"
% Isochronous sequences

clear;


%% definitions

ISI = 500;		% interstimulus interval (milliseconds)
N_stim = 20;	% number of bips within a sequence


%% start communication with Arduino

%ardu = serial('COM3');							% windows
ardu = serial('/dev/tty.usbserial-A9007Qr6');	% mac os x
fopen(ardu);
pause(2);							% wait for fopen to complete


%%

fprintf(ardu,'ARDU;I%d;N%d;P%d;B%d;E%d;X',[ISI N_stim 100 10 3]);	% send parameters


%% main loop

data = [];
aux = fgetl(ardu);
counter = 1;
while (~strcmp(aux(1),'E'))
	data{counter} = aux;
	aux = fgetl(ardu);
	counter = counter + 1;
end

