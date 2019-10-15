//Un timer controla dos pines de salida
//Estímulo: seno -pin 11 (OC1A)- Van Vugt script adaptation. pin 12: OC1B 
//Feedback: un timer controla dos pines:  seno -pin 5 (OC3A) y pin2 (OC3B) - Van Vugt script adaptation. pin 3: OC3C, pin 2: OC3B 
//trial eterno (sin Matlab)
//Manda estímulo al pin 11 y al pin 12 (timer 1)
//y feedback al pin 5 y al pin 2 (timer 3)

#define stimPinR 11
#define stimPinL 12
#define fdbkPinR 5
#define fdbkPinL 2
#define noisePinR 10
#define noisePinL 9
#define pinVG A11

#define LFSR_INIT  0xfeedfaceUL
#define LFSR_MASK  ((unsigned long)( 1UL<<31 | 1UL <<15 | 1UL <<2 | 1UL <<1  ))

//http://sphinx.mythic-beasts.com/~markt/ATmega-timers.html
boolean stimRight=true;  //pin11 - timer 1, channel A: right
boolean stimLeft=true;  //pin12 - timer 1, channel B: left
boolean fdbkRight=true; //pin5 - timer 3, channel A: right
boolean fdbkLeft=true;  //pin2 - timer 3, channel B: left
boolean noise = false;

unsigned long int prevStim_t=0,prevFdbk_t=0,t=0;
boolean stim_flag=false;
boolean fdbk_flag=false;

unsigned int stimFreq = 5000;//(C6) // defines the frequency (i.e., pitch) of the tone (in Hz)
unsigned int fdbkFreq = 660;//(C6) // defines the frequency (i.e., pitch) of the tone (in Hz)

int vg = 0;
int read_vg = 0;
int amplitude = 1;

uint16_t phaseIncrementStim = 0;  // 16 bit delta
uint16_t phaseIncrementFdbk = 0; // 16 bit delta
uint16_t phaseAccumulatorStim = 0;  // 16 bit accumulator
uint16_t phaseAccumulatorFdbk = 0; // 16 bit accumulator


// DDS resolution
const uint32_t freq_samp = 31180; // 16MHz/513 porque ahora el pin está en modo 9 bits
const uint32_t resolution_DDS = pow(2,32)/freq_samp;


//AGREGO
#define STIM_DURATION 50 //stimulus duration (milliseconds)
#define FDBK_DURATION 50 //este lo agrego yo 
#define ANTIBOUNCE (0.5*isi)//minimum interval between responses (milliseconds)
boolean allow;
int fdbk, i;
unsigned int stim_number,fdbk_number;
unsigned int *event_number;
char *event_name;
unsigned long * event_time;
unsigned int event_counter; 

unsigned int isi=300,n_stim=3; //Entiendo que son valores iniciales por las dudas 
int perturb_size=0;  // estos los agrego paraque no tire error
unsigned int perturb_bip=0;
unsigned int event_type=0;
#define INPUTPIN 11
char message[20];


//////////// Set up lookup table for waveform generation
// sine wavefunction
static const uint8_t  sineTable[] PROGMEM = {
0x80,0x83,0x86,0x89,0x8c,0x8f,0x92,0x95,
0x98,0x9c,0x9f,0xa2,0xa5,0xa8,0xab,0xae,
0xb0,0xb3,0xb6,0xb9,0xbc,0xbf,0xc1,0xc4,
0xc7,0xc9,0xcc,0xce,0xd1,0xd3,0xd5,0xd8,
0xda,0xdc,0xde,0xe0,0xe2,0xe4,0xe6,0xe8,
0xea,0xec,0xed,0xef,0xf0,0xf2,0xf3,0xf5,
0xf6,0xf7,0xf8,0xf9,0xfa,0xfb,0xfc,0xfc,
0xfd,0xfe,0xfe,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xfe,0xfe,
0xfd,0xfc,0xfc,0xfb,0xfa,0xf9,0xf8,0xf7,
0xf6,0xf5,0xf3,0xf2,0xf0,0xef,0xed,0xec,
0xea,0xe8,0xe6,0xe4,0xe2,0xe0,0xde,0xdc,
0xda,0xd8,0xd5,0xd3,0xd1,0xce,0xcc,0xc9,
0xc7,0xc4,0xc1,0xbf,0xbc,0xb9,0xb6,0xb3,
0xb0,0xae,0xab,0xa8,0xa5,0xa2,0x9f,0x9c,
0x98,0x95,0x92,0x8f,0x8c,0x89,0x86,0x83,
0x80,0x7c,0x79,0x76,0x73,0x70,0x6d,0x6a,
0x67,0x63,0x60,0x5d,0x5a,0x57,0x54,0x51,
0x4f,0x4c,0x49,0x46,0x43,0x40,0x3e,0x3b,
0x38,0x36,0x33,0x31,0x2e,0x2c,0x2a,0x27,
0x25,0x23,0x21,0x1f,0x1d,0x1b,0x19,0x17,
0x15,0x13,0x12,0x10,0x0f,0x0d,0x0c,0x0a,
0x09,0x08,0x07,0x06,0x05,0x04,0x03,0x03,
0x02,0x01,0x01,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,
0x02,0x03,0x03,0x04,0x05,0x06,0x07,0x08,
0x09,0x0a,0x0c,0x0d,0x0f,0x10,0x12,0x13,
0x15,0x17,0x19,0x1b,0x1d,0x1f,0x21,0x23,
0x25,0x27,0x2a,0x2c,0x2e,0x31,0x33,0x36,
0x38,0x3b,0x3e,0x40,0x43,0x46,0x49,0x4c,
0x4f,0x51,0x54,0x57,0x5a,0x5d,0x60,0x63,
0x67,0x6a,0x6d,0x70,0x73,0x76,0x79,0x7c
};

ISR(TIMER1_OVF_vect) {
  // wavetable lookup index (upper 8 bits of the accumulator)
  uint8_t index1 = 0;
  
  // Update accumulator
  phaseAccumulatorStim += phaseIncrementStim;
  index1 = phaseAccumulatorStim >> 8;

  // Read oscillator value for next interrupt
  if (stimRight==true)
    OCR1A = pgm_read_byte(&sineTable[index1]);
  else
    OCR1A = vg;
  if (stimLeft==true)
    OCR1B = pgm_read_byte(&sineTable[index1]);
  else
    OCR1B = vg;  
}


ISR(TIMER3_OVF_vect) {
  // wavetable lookup index (upper 8 bits of the accumulator)
  uint8_t index3 = 0;
  // Update accumulator
  phaseAccumulatorFdbk += phaseIncrementFdbk;
  index3 = phaseAccumulatorFdbk >> 8;

  // Read oscillator value for next interrupt
  if (fdbkRight==true)
    OCR3A = pgm_read_byte(&sineTable[index3]);
  else
    OCR3A = vg;
  if (fdbkLeft==true)
    OCR3B = pgm_read_byte(&sineTable[index3]);
  else
    OCR3B = vg;    
}


ISR(TIMER2_OVF_vect){
  OCR2A = 127;
  if(noise==true)
    OCR2B = generateNoise(amplitude, vg);
  else
    OCR2B = vg;    
  }

void initTimers(void){
  // Stimulus
  // Set pins as output
  pinMode(stimPinR,OUTPUT);
  pinMode(stimPinL,OUTPUT);

  // 9-bit Fast PWM - non inverted PWM
  TCCR1A= _BV(COM1A1) | _BV(COM1B1) | _BV(WGM11);

  // Start timer without prescaler
   TCCR1B = _BV(WGM12) | _BV(CS10);
  // Enable overflow interrupt for OCR1A
  TIMSK1 = _BV(TOIE1);

  // Feedback
  // Set pins as output
  pinMode(fdbkPinR,OUTPUT);
  pinMode(fdbkPinL,OUTPUT);

  // 9-bit Fast PWM - non inverted PWM
  TCCR3A= _BV(COM3A1) | _BV(COM3B1) | _BV(WGM31);
  // Start timer without prescaler
  //  TCCR3B = _BV(WGM32) | _BV(CS32);
  TCCR3B = _BV(WGM32) | _BV(CS30);
  // Enable overflow interrupt for OCR1A and OCR1B
  TIMSK3 = _BV(TOIE3);


  //Noise
  // Set pins as output
  pinMode(noisePinR,OUTPUT);
  pinMode(noisePinL,OUTPUT);

  TIMSK2 = _BV(TOIE2); 
  //Dos Registros del timer2
  TCCR2A  = _BV(COM2A1) | _BV(COM2B1) | _BV(WGM21) | _BV(WGM20);
  //TCCR2B  = _BV(CS20)   ;
  TCCR2B  = _BV(CS21)  | _BV(WGM22);
  // Fast PWM 8bits non inverted, CTC, TOF2 on TOP (OCR2A)
}


// Función que genera el ruido blanco
unsigned int generateNoise(int amplitude, int vg_value){ 
   uint8_t aux=0;
   static unsigned long int lfsr = LFSR_INIT;  // See https://en.wikipedia.org/wiki/Linear_feedback_shift_register#Galois_LFSRs
   // 32 bit init, nonzero
   // If the output bit is 1, apply toggle mask. The value has 1 at bits corresponding to taps, 0 elsewhere.
   
   if(lfsr & 1) { 
    lfsr =  (lfsr >>1) ^ LFSR_MASK; 
    aux = vg_value+amplitude;
    }
   else{
    lfsr >>= 1;
    aux = vg_value-amplitude;
    }

  return(aux);
}


// Lectura de la tierra virtual desde un pin analógico
int readVirtualGround(void)
{
  return analogRead(pinVG);
}



/* Translates the desired output frequency to a phase increment to be used with the phase accumulator.*/
uint16_t setFrequency( uint16_t frequency ){
  uint32_t phaseIncr32 =  resolution_DDS * frequency;
  return (phaseIncr32 >> 16);
}

// Function to start playing sound
void SoundSwitch(char tipo,uint16_t freq, boolean left, boolean right){
/* This function enables the timerOverflowInterrupt in the time mask depending on tipo: 
if tipo is 's', selects Timer 1 (stimulus)
if tipo is 'f' selects Timer 3 (feedback)
if tipo is 'n' selects Timer 2 (Noise)
the left and right bools as true or false selects the channels where the signals will come out
for 's' and 'f', freq is the frequency of the beep.
for 'n', freq is the amplitud in GenerateNoise, meaning the volume of the white noise.
*/
  switch(tipo){
    case 's':
      phaseIncrementStim = setFrequency(freq);
      
      if(right) stimRight = true;
      else stimRight = false;
      
      if(left)  stimLeft = true;
      else  stimLeft = false;
      
      break;
      
  
    case 'f':
      phaseIncrementFdbk = setFrequency(freq);
      
      if(right) fdbkRight    = true;
      else  fdbkRight = false;

      if(left)  fdbkLeft     = true;
      else  fdbkLeft = false;     

      break;

  
    case 'n':
      amplitude = freq;
      noise = true;
      break;
  }  
}


void PlaySoundWhile(char tipo, uint16_t freq, boolean left, boolean right, uint16_t cadaCuanto, uint16_t cuanto, uint64_t t){  

	boolean *flag;
	long int *prev_t;
	uint16_t *phaseAccumulator;	
	
	switch(tipo){
		case 's':
			flag   = &stim_flag;
			prev_t = &prevStim_t;
			phaseAccumulator = &phaseAccumulatorStim;
			
			//AGREGO
			event_name[event_counter] = 's';
			event_number[event_counter] = stim_number;
			event_time[event_counter] = t;
			//next step
			event_counter++;
			stim_number++;
			break;
	
		case 'f':
			flag   = &fdbk_flag;
			prev_t = &prevFdbk_t;
			phaseAccumulator = &phaseAccumulatorFdbk;
			event_name[event_counter] = 'f';
			event_number[event_counter] = fdbk_number;
			event_time[event_counter] = t;
			//next step
			event_counter++;
			fdbk_number++;
			break;
	}

	if ((t-*prev_t)>cadaCuanto && *flag==false) { //enciende el sonido
		*phaseAccumulator = 0;
		SoundSwitch(tipo, freq, left, right);
		*prev_t=t;
		*flag=true;
	}

	if (t-*prev_t>cuanto && *flag==true){ //apaga el sonido
		SoundSwitch(tipo, freq, false, false);
		*flag=false;
	}  
}


//---------------------------------------------------------------------
//print a line avoiding "carriage return" of Serial.println()
void serial_print_string(char *string) {
  Serial.print(string);
  Serial.print("\n");
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



void setup() {

  //AGREGO
  Serial.begin(9600); //USB communication with computer

  cli();
  
  initTimers();

  // Unica lectura de tierra virtual hasta que el loop sea el correcto (condicion para iniciar)
  read_vg = readVirtualGround();
  vg = (int) (read_vg*256/1024);

  //AGREGO
  allow = false;

  
  sei();
}



void loop() {

	t = millis();
	
	//AGREGO
	if(allow == false){
		get_parameters();
		allow = true;

		stim_number = 1;
		fdbk_number = 1;
		event_counter = 0;
		
		event_name = (char*) calloc(3*n_stim,sizeof(char));
		event_number = (unsigned int*) calloc(3*n_stim,sizeof(unsigned int));
		event_time = (unsigned long*) calloc(3*n_stim,sizeof(unsigned long));

	}

	else{
		//send stimulus
		//PlaySoundWhile('s',stimFreq, true, true, isi, STIM_DURATION, t);
		//SoundSwitch('s',stimFreq,true,true);
		if ((t-prevStim_t)> isi && stim_flag==false) { //enciende el sonido
			phaseAccumulatorStim = 0;
			SoundSwitch('s', stimFreq, true, true);
			prevStim_t=t;
			stim_flag=true;
		}

		if (t-prevStim_t>STIM_DURATION && stim_flag==true){ //apaga el sonido
			SoundSwitch('s', stimFreq, false, false);
			stim_flag=false;
		}		



		//read response
		if ((t - prevFdbk_t) > ANTIBOUNCE && fdbk_flag==false) {
			fdbk = digitalRead(INPUTPIN);
			if (fdbk == HIGH){
				SoundSwitch('f', fdbkFreq, true, true);
				prevFdbk_t=t;
				fdbk_flag=true;
			}
		}

		if (t-prevFdbk_t>FDBK_DURATION && fdbk_flag==true){ //apaga el sonido
			SoundSwitch('f', fdbkFreq, false, false);
			fdbk_flag=false;
		}


		//end trial
		//allow one more period (without stimulus)
		if (stim_number > n_stim && (t - prevStim_t) >= isi) {
			for (i=0; i<event_counter; i++) {
				sprintf(message,"%c %d: %ld;",
					event_name[i],event_number[i],event_time[i]);
				serial_print_string(message);
			}
			Serial.println("E");	//send END message
			allow = false;
			free(event_name);
			free(event_number);
			free(event_time);	
		}
		
		//turn on noise
		//SoundSwitch('n',1,true,true);
	}
  
}
