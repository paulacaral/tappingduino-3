//Synchronization
//Igual que hasta ahora pero manda una marca adicional de respuesta con
//cada marca de estimulo (para probar si los errores se producen cuando
//las marcas son simultaneas)


#include <Tone.h>
#include <stdlib.h>

#define STIMPIN 13	//stimulus output to pin 13
#define RESPPIN 12	//response feedback output to pin 12
#define INPUTPIN 11	//response interruptor between pin 4 and 5V
#define SYNCPIN1 9	//stimulus sync signal to EEG
#define SYNCPIN2 8	//response sync signal to EEG
#define EVNTPIN1 7	//six bits for event clasification to EEG
#define EVNTPIN2 6
#define EVNTPIN3 5
#define EVNTPIN4 4
#define EVNTPIN5 3
#define EVNTPIN6 2


#define STIM_DURATION 50	//stimulus duration (milliseconds)
#define ANTIBOUNCE (0.5*isi)//minimum interval between responses (milliseconds)
#define LOGIC_DURATION 10	//duration of logical signals to EEG (milliseconds)
#define ISOCHRONOUS 1		//code for perturbation type
#define STEPCHANGE 2
#define PHASESHIFT 3


//---------------------------------------------------------------------
//definition of global variables

//trial parameters
unsigned int isi=300,n_stim=3;
int perturb_size=0;
unsigned int perturb_bip=0;
unsigned int event_type=ISOCHRONOUS;

//general variables
int i,resp;
unsigned int stim_number,resp_number;
unsigned long t,prev_stim_t,prev_resp_t;
char *event_name;
unsigned int *event_number;
unsigned long *event_time;
unsigned int event_counter;

char message[20];
Tone stim_tone,resp_tone;
boolean allow,perturb_flag,perturb_mark_flag;


//---------------------------------------------------------------------
int memorialibre=0;
extern int __bss_end;
extern void *__brkval;

int get_free_memory() {
	int free_memory;

	if((int)__brkval == 0)
		free_memory = ((int)&free_memory) - ((int)&__bss_end);
	else
		free_memory = ((int)&free_memory) - ((int)__brkval);
	return free_memory;
}


//---------------------------------------------------------------------
//print a line avoiding "carriage return" of Serial.println()
void serial_print_string(char *string) {
	Serial.print(string);
	Serial.print("\n");
	return;
}


//---------------------------------------------------------------------
//decimal (8 bits) to binary conversion
//result: least significant bit (even/odd) to the right
void fast_d2b(unsigned char dec, unsigned char *c) {
	char i;
	for(i=0; i<8; i++)
		c[7-i] = (dec >> i) & 0x1;
	return;
}


//---------------------------------------------------------------------
//set bits for event classification
//EVENTPIN1 = most significant bit, EVENTPIN6 = least significant bit
void set_event_type(unsigned char event_type_dec, boolean perturb_mark_flag) {
	unsigned char event_type_bin[8];
	fast_d2b(event_type_dec,event_type_bin);
	//first pin: perturbation mark
	digitalWrite(EVNTPIN1,perturb_mark_flag==true?HIGH:LOW);
	//rest of pins: event classification
	digitalWrite(EVNTPIN2,event_type_bin[3]==1?HIGH:LOW);
	digitalWrite(EVNTPIN3,event_type_bin[4]==1?HIGH:LOW);
	digitalWrite(EVNTPIN4,event_type_bin[5]==1?HIGH:LOW);
	digitalWrite(EVNTPIN5,event_type_bin[6]==1?HIGH:LOW);
	digitalWrite(EVNTPIN6,event_type_bin[7]==1?HIGH:LOW);
	return;
}


//---------------------------------------------------------------------
//parse data from serial input
//input data format: eg "I500;N30;P-10;B15;E5;X"
void parse_data(char *line) {
	char field[10];
	int n,data;
	//scan input until next ';' (field separator)
	while (sscanf(line,"%[^;]%n",field,&n) == 1) {
		data = atoi(field+1);
		//parse data according to field header
		switch (field[0]) {
			case 'I':
				isi = data;
				break;
			case 'N':
				n_stim = data;
				break;
			case 'P':
				perturb_size = data;
				break;
			case 'B':
				perturb_bip = data;
			case 'E':
				event_type = data;
				break;
			default:
				break;
		}
		line += n;
		if (*line != ';')
			break;
		while (*line == ';')
			line++;
	}
	return;
}


//---------------------------------------------------------------------
void get_parameters() {
	char line[45],i,aux='0';
	i = 0;

	//directly read next available character from buffer
	//if flow ever gets here, then next available character should be 'I'
	aux = Serial.read();

	//read buffer until getting an X (end of message)
	while (aux != 'X') {
		//keep reading if input buffer is empty
		while (Serial.available() < 1) {}
		line[i] = aux;
		i++;
		aux = Serial.read();
	}
	line[i] = '\0';					//terminate the string

	//just in case, clear incoming buffer once read
	Serial.flush();
	//parse input chain into parameters
	parse_data(line);
	return;
}


//---------------------------------------------------------------------
//get keyword before reading parameters
void get_keyword() {
	boolean allow = false;
	char keywrd[5] = "EEEE";

	//read input buffer until keyword "ARDU;"
	while (allow == false) {
		while (Serial.available() < 1) {
			//allow user to tap while waiting for data from computer
			resp = digitalRead(INPUTPIN);
			if (resp == HIGH)
				resp_tone.play(NOTE_D5,STIM_DURATION);
		}
		//read input buffer one at a time
		if (keywrd[0] == 'A' && keywrd[1] == 'R'
			&& keywrd[2] == 'D' && keywrd[3] == 'U' && keywrd[4] == ';') {
			//only combination allowed, in this specific order
			allow = true;
		}
		else {
			//move buffer one step up
			keywrd[0] = keywrd[1];
			keywrd[1] = keywrd[2];
			keywrd[2] = keywrd[3];
			keywrd[3] = keywrd[4];
			keywrd[4] = Serial.read();
		}
	}
	return;
}


//---------------------------------------------------------------------
void setup() {
	Serial.begin(9600);				//USB communication with computer
	stim_tone.begin(STIMPIN);		//stimulus output
	resp_tone.begin(RESPPIN);		//feedback output
	pinMode(INPUTPIN,INPUT);//input pin pulled-down to GND by actual resistor
	digitalWrite(INPUTPIN,LOW);		//just in case
	pinMode(SYNCPIN1,OUTPUT);
	pinMode(SYNCPIN2,OUTPUT);
	pinMode(EVNTPIN1,OUTPUT);
	pinMode(EVNTPIN2,OUTPUT);
	pinMode(EVNTPIN3,OUTPUT);
	pinMode(EVNTPIN4,OUTPUT);
	pinMode(EVNTPIN5,OUTPUT);
	pinMode(EVNTPIN6,OUTPUT);
	allow = false;
}


//---------------------------------------------------------------------
//main loop
void loop() {
	if (allow == false) {

		//constantly check buffer for keyword
		get_keyword();
		//ok, keyword found
		allow = true;
		get_parameters();

		prev_stim_t = 0;
		prev_resp_t = 0;
		stim_number = 1;
		resp_number = 1;
		event_counter = 0;
		perturb_flag = false;
		perturb_mark_flag = false;

		event_name = (char*) calloc(3*n_stim,sizeof(char));
		event_number = (unsigned int*) calloc(3*n_stim,sizeof(unsigned int));
		event_time = (unsigned long*) calloc(3*n_stim,sizeof(unsigned long));

		//reset logic signals to EEG
		digitalWrite(SYNCPIN1,LOW);
		digitalWrite(SYNCPIN2,LOW);
		set_event_type(0,perturb_mark_flag);

/*
		memorialibre = get_free_memory();
		Serial.print("memoria libre: ");
		Serial.print(memorialibre);
		Serial.println(" bytes");
*/

	}
	//start trial
	else {
		t = millis();

		//turn on stimulus
		if ((t - prev_stim_t) >= isi && stim_number <= n_stim) {
			stim_tone.play(NOTE_A4,STIM_DURATION);
			//turn on stimulus sync signal to EEG
			digitalWrite(SYNCPIN1,HIGH);


//para probar simultaneidad de marcas
			digitalWrite(SYNCPIN2,HIGH);



			//turn on pins for event clasification
			set_event_type(event_type,perturb_mark_flag);
			if (perturb_mark_flag == true)
				perturb_mark_flag = false;
			//store event data
			event_name[event_counter] = 'S';
			event_number[event_counter] = stim_number;
			event_time[event_counter] = t;
			//next step
			event_counter++;
			stim_number++;
			prev_stim_t = t;
		}

		//read response
		if ((t - prev_resp_t) > ANTIBOUNCE) {
			resp = digitalRead(INPUTPIN);
			if (resp == HIGH) {
				resp_tone.play(NOTE_D5,STIM_DURATION);
				//turn on response sync signal to EEG
				digitalWrite(SYNCPIN2,HIGH);
				//store event data
				event_name[event_counter] = 'R';
				event_number[event_counter] = resp_number;
				event_time[event_counter] = t;
				//next step
				resp_number++;
				event_counter++;
				prev_resp_t = t;
			}
		}

		//turn off sync signals and event clasification
		if ((t - prev_stim_t) > LOGIC_DURATION) {
			digitalWrite(SYNCPIN1,LOW);
			set_event_type(0,false);




//para probar simultaneidad de marcas
			digitalWrite(SYNCPIN2,LOW);




		}
		if ((t - prev_resp_t) > LOGIC_DURATION) {
			digitalWrite(SYNCPIN2,LOW);
		}


		//perturbation
		if (stim_number == perturb_bip && perturb_flag == false
			&& (event_type == STEPCHANGE || event_type == PHASESHIFT)){
			//step change or first perturbation of phase shift
			isi += perturb_size;
			perturb_flag = true;
			perturb_mark_flag = true;
		}
		if (stim_number == perturb_bip + 1 && perturb_flag == true
			&& event_type == PHASESHIFT) {
			//second perturbation of phase shift
			isi += -perturb_size;
			perturb_flag = false;
		}


		//end trial
		//allow one more period (without stimulus)
		if (stim_number > n_stim && (t - prev_stim_t) >= isi) {
			for (i=0; i<event_counter; i++) {
				sprintf(message,"%c %d: %ld;",
					event_name[i],event_number[i],event_time[i]);
				serial_print_string(message);
			}
			Serial.println("E");	//send READY message
			allow = false;
			free(event_name);
			free(event_number);
			free(event_time);
		}
	}
}

