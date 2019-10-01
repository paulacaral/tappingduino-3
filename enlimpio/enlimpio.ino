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
#define noisePinR4 6
#define noisePinL4 7

#define beepDuration 100
//http://sphinx.mythic-beasts.com/~markt/ATmega-timers.html
boolean stimRight=true;	//pin11 - timer 1, channel A: right
boolean stimLeft=true;	//pin12 - timer 1, channel B: left
boolean fdbkRight=true;	//pin5 - timer 3, channel A: right
boolean fdbkLeft=true;	//pin2 - timer 3, channel B: left
boolean noiseRight=true;	//pin10 - timer 2, channel A: right
boolean noiseLeft=true;		//pin9 - timer 2, channel B: left
boolean noiseRight4=true;  //pin6 - timer 4, channel A: right
boolean noiseLeft4=true;   //pin7 - timer 4, channel B: left


unsigned long int prevStim_t=0,prevFdbk_t=0,prevNoise_t=0,prevNoise4_t=0,t=0;
boolean stim_flag=false;
boolean fdbk_flag=false;
boolean noise_flag=false;
boolean noise4_flag=false;

unsigned int stimFreq = 440;//(C6) // defines the frequency (i.e., pitch) of the tone (in Hz)
unsigned int fdbkFreq = 660;//(C6) // defines the frequency (i.e., pitch) of the tone (in Hz)
unsigned int noiseFreq = 784;

boolean volt;
unsigned int voltint;

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

// virtual (constant) ground
static const uint8_t  vgTable[] PROGMEM = {
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75,
0x75,0x75,0x75,0x75,0x75,0x75,0x75,0x75  
};



// TIMER1 will overflow at a 62.5KHz(Sampling frequency).
// Updates the OCR1A value and the accumulator.
// Computes the next sample to be sent to the PWM.

	static uint16_t phaseIncrementStim = 0;	// 16 bit delta
  static uint16_t phaseIncrementFdbk = 0; // 16 bit delta
  static uint16_t phaseIncrementNoise = 0; // 16 bit delta
  static uint16_t phaseIncrementNoise4 = 0; // 16 bit delta
	const uint32_t resolution = 2*68719;//68719;	// DDS resolution - NO PONER 65536

ISR(TIMER1_OVF_vect) {
	static uint8_t osc1A = 0;
	static uint8_t osc1B = 0;
	static uint16_t phaseAccumulatorStim = 0;	// 16 bit accumulator
	// wavetable lookup index (upper 8 bits of the accumulator)
	static uint8_t index1 = 0;

	// Send oscillator output to PWM
	OCR1A = osc1A;
	OCR1B = osc1B;

	// Update accumulator
	phaseAccumulatorStim += phaseIncrementStim;
	index1 = phaseAccumulatorStim >> 8;

	// Read oscillator value for next interrupt
	if (stimRight==true)
		osc1A = pgm_read_byte(&sineTable[index1]);
	else
		osc1A = pgm_read_byte(&vgTable[1]);

	if (stimLeft==true)
		osc1B = pgm_read_byte(&sineTable[index1]);
	else
		osc1B = pgm_read_byte(&vgTable[1]);
   
}


ISR(TIMER3_OVF_vect) {
  
  static uint8_t osc3A = 0;
  static uint8_t osc3B = 0;
  static uint16_t phaseAccumulatorFdbk = 0; // 16 bit accumulator
  // wavetable lookup index (upper 8 bits of the accumulator)
  static uint8_t index3 = 0;

  // Send oscillator output to PWM
  OCR3A = osc3A;
  OCR3B = osc3B;

  // Update accumulator
  phaseAccumulatorFdbk += phaseIncrementFdbk;
  index3 = phaseAccumulatorFdbk >> 8;

  // Read oscillator value for next interrupt
  if (fdbkRight==true)
    osc3A = pgm_read_byte(&sineTable[index3]);
  else
    osc3A = pgm_read_byte(&vgTable[1]);

  if (fdbkLeft==true)
    osc3B = pgm_read_byte(&sineTable[index3]);
  else
    osc3B = pgm_read_byte(&vgTable[1]);
    
}


ISR(TIMER2_OVF_vect){
  //OCR2A = 127;
  OCR2A = generateNoise();  
  OCR2B = generateNoise();
  }



/*
ISR(TIMER2_OVF_vect)
{
  static uint8_t osc2A = 0;
  static uint8_t osc2B = 0;
  static uint16_t phaseAccumulatorNoise = 0; // 16 bit accumulator
  // wavetable lookup index (upper 8 bits of the accumulator)
  static uint8_t index2 = 0;

  // Send oscillator output to PWM
  OCR2A = osc2A;
  OCR2B = osc2B;

  // Update accumulator
  phaseAccumulatorNoise += phaseIncrementNoise;
  index2 = phaseAccumulatorNoise >> 8;

  // Read oscillator value for next interrupt
  if (noiseRight==true)
    osc2A = pgm_read_byte(&sineTable[index2]);
  else
    osc2A = pgm_read_byte(&vgTable[1]);

  if (noiseLeft==true)
    osc2B = pgm_read_byte(&sineTable[index2]);
  else
    osc2B = pgm_read_byte(&vgTable[1]);
  
}
*/

ISR(TIMER4_OVF_vect) {
  static uint8_t osc4A = 0;
  static uint8_t osc4B = 0;
  static uint16_t phaseAccumulatorNoise4 = 0; // 16 bit accumulator
  // wavetable lookup index (upper 8 bits of the accumulator)
  static uint8_t index4 = 0;

  // Send oscillator output to PWM
  OCR4A = osc4A;
  OCR4B = osc4B;

  // Update accumulator
  phaseAccumulatorNoise4 += phaseIncrementNoise4;
  index4 = phaseAccumulatorNoise4 >> 8;

  // Read oscillator value for next interrupt
  if (noiseRight4==true)
    osc4A = pgm_read_byte(&sineTable[index4]);
  else
    osc4A = pgm_read_byte(&vgTable[1]);

  if (noiseLeft4==true)
    osc4B = pgm_read_byte(&sineTable[index4]);
  else
    osc4B = pgm_read_byte(&vgTable[1]);
}


// Configures TIMER1 to fast PWM non inverted mode.
// Prescaler set to 1, which means that timer overflows
// every 16MHz/256 = 62.5KHz
void initPWMstim(void) {
	// Set pins as output
	pinMode(stimPinR,OUTPUT);
	pinMode(stimPinL,OUTPUT);

	// 8-bit Fast PWM - non inverted PWM
//	TCCR1A= _BV(COM1A1) | _BV(COM1B1) | _BV(WGM10);
  TCCR1A= _BV(COM1A1) | _BV(COM1B1) | _BV(WGM11);//| _BV(WGM10);
  //"_BV" viene de Bit Value porque convierte valores de bit number a byte value, que es lo que se puede configurar en los registros.
	// Start timer without prescaler
	TCCR1B = _BV(WGM12) | _BV(CS10);
//  TCCR1B = _BV(WGM12) | _BV(CS12);
	// Enable overflow interrupt for OCR1A
	TIMSK1 = _BV(TOIE1);
}


void initPWMfdbk(void) {
  // Set pins as output
  pinMode(fdbkPinR,OUTPUT);
  pinMode(fdbkPinL,OUTPUT);

  // 8-bit Fast PWM - non inverted PWM
//  TCCR3A= _BV(COM3A1) | _BV(COM3B1) | _BV(WGM30); //COM3A1 habilita channel A y COM3B1 el channel B. Hay que hacerlo en orden
  TCCR3A= _BV(COM3A1) | _BV(COM3B1) | _BV(WGM31);//| _BV(WGM30); //COM3A1 habilita channel A y COM3B1 el channel B. Hay que hacerlo en orden
  // Start timer without prescaler
  TCCR3B = _BV(WGM32) | _BV(CS30);
//  TCCR3B = _BV(WGM32) | _BV(CS32);
  // Enable overflow interrupt for OCR1A and OCR1B
  TIMSK3 = _BV(TOIE3);
}


void initPWMnoise(void) {
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


void initPWMnoise4(void) {
  // Set pins as output
  pinMode(noisePinR4,OUTPUT);
  pinMode(noisePinL4,OUTPUT);

  // 8-bit Fast PWM - non inverted PWM
  //TCCR4A= _BV(COM4A1) | _BV(COM4B1) | _BV(WGM40); //COM3A1 habilita channel A y COM3B1 el channel B. Hay que hacerlo en orden
  TCCR4A= _BV(COM4A1) | _BV(COM4B1) | _BV(WGM41);//| _BV(WGM40);
  // Start timer without prescaler
  TCCR4B = _BV(WGM42) | _BV(CS40);
  // Enable overflow interrupt for OCR1A and OCR1B
  TIMSK4 = _BV(TOIE4);
}



// Translates the desired output frequency to a phase
// increment to be used with the phase accumulator.
// The 16 bit shift is required to remove the 2^16
// scale factor of the resolution.
void setFrequencyStim(uint16_t frequency) {
	uint64_t phaseIncr64 = resolution*frequency;
	phaseIncrementStim = phaseIncr64 >> 16; 
}


void setFrequencyFdbk(uint16_t frequency) {
  uint64_t phaseIncr64 = resolution*frequency;
  phaseIncrementFdbk = phaseIncr64 >> 16; 
}


void setFrequencyNoise(uint16_t frequency) {
  uint64_t phaseIncr64 = resolution*frequency;
  phaseIncrementNoise = phaseIncr64 >> 16; 
}

void setFrequencyNoise4(uint16_t frequency) {
  uint64_t phaseIncr64 = resolution*frequency;
  phaseIncrementNoise4 = phaseIncr64 >> 16; 
}

// function to turn tick on
void tickOnStim(){
	stimLeft = true; 
	stimRight = true;
	setFrequencyStim(stimFreq);
}

// function to turn tick off
void tickOffStim(){
	stimLeft = false; 
	stimRight = false;
}

// function to turn tick on
void tickOnFdbk(){
  fdbkLeft = true; 
  fdbkRight = true;
  setFrequencyFdbk(fdbkFreq);
}

// function to turn tick off
void tickOffFdbk(){
  fdbkLeft = false; 
  fdbkRight = false;
}

// function to turn tick on
void tickOnNoise(){
  noiseLeft = true; 
  noiseRight = true;
  setFrequencyNoise(noiseFreq);
}
// function to turn tick off
void tickOffNoise(){
  noiseLeft = false; 
  noiseRight = false;
}


// function to turn tick on
void tickOnNoise4(){
  noiseLeft4 = true; 
  noiseRight4 = true;
  setFrequencyNoise4(noiseFreq);
}
// function to turn tick off
void tickOffNoise4(){
  noiseLeft4 = false; 
  noiseRight4 = false;
}


/* initialize with any 32 bit non-zero  unsigned long value. */
#define LFSR_INIT  0xfeedfaceUL
/* Choose bits 32, 30, 26, 24 from  http://arduino.stackexchange.com/a/6725/6628
 *  or 32, 22, 2, 1 from 
 *  http://www.xilinx.com/support/documentation/application_notes/xapp052.pdf
 *  or bits 32, 16, 3,2  or 0x80010006UL per http://users.ece.cmu.edu/~koopman/lfsr/index.html 
 *  and http://users.ece.cmu.edu/~koopman/lfsr/32.dat.gz
 */  
#define LFSR_MASK  ((unsigned long)( 1UL<<31 | 1UL <<15 | 1UL <<2 | 1UL <<1  ))

unsigned int generateNoise(){ 

   uint8_t aux=0;
   
   // See https://en.wikipedia.org/wiki/Linear_feedback_shift_register#Galois_LFSRs
   static unsigned long int lfsr = LFSR_INIT;  /* 32 bit init, nonzero */
   /* If the output bit is 1, apply toggle mask.
                                    * The value has 1 at bits corresponding
                                    * to taps, 0 elsewhere. */
   if(lfsr & 1) { 
    lfsr =  (lfsr >>1) ^ LFSR_MASK ; 
    aux = 117+10;
    }
   else{
    lfsr >>= 1;
    aux = 117-10;
    }
  return(aux);
   
}






void setup() {


	cli();

	// Set pins as output
//	pinMode(fdbkPinR,OUTPUT);
//	pinMode(fdbkPinL,OUTPUT);
 // pinMode(noisePinR,OUTPUT);
	//pinMode(noisePinL,OUTPUT);

    
//	analogWrite(fdbkPinR,0);
//	analogWrite(fdbkPinL,0);
//	analogWrite(noisePinR,117);
//	analogWrite(noisePinL,117);

	initPWMstim();
  initPWMfdbk();
  initPWMnoise();
  initPWMnoise4();

  
	sei();
}




void loop() {

	t = millis();



	if ((t-prevStim_t)>500 && stim_flag==false) { //enciende el tono estimulo
		tickOnStim();
		prevStim_t = t;
		stim_flag = true;
	}

	if (t-prevStim_t>beepDuration && stim_flag==true){ //apaga el tono estimulo
		tickOffStim();
		stim_flag = false;
	}




 if ((t-prevFdbk_t)>800 && fdbk_flag==false) { //enciende el tono estimulo
   tickOnFdbk();
    prevFdbk_t = t;
    fdbk_flag = true;
  }

  if (t-prevFdbk_t>beepDuration && fdbk_flag==true){ //apaga el tono estimulo
    tickOffFdbk();
    fdbk_flag = false;
  }



/*
   if ((t-prevNoise_t)>700 && noise_flag==false) { //enciende el tono estimulo
    tickOnNoise();
    prevNoise_t = t;
    noise_flag = true;
  }

  if (t-prevNoise_t>50 && noise_flag==true){ //apaga el tono estimulo
    tickOffNoise();
    noise_flag = false;
  }
 
  
*/
   /*
   if ((t-prevNoise4_t)>1100 && noise4_flag==false) { //enciende el tono estimulo
   tickOnNoise4();
    prevNoise4_t = t;
    noise4_flag = true;
  }

  if (t-prevNoise4_t>beepDuration && noise4_flag==true){ //apaga el tono estimulo
    tickOffNoise4();
    noise4_flag = false;
  }
*/

  /*
  volt=(boolean)generateNoise();
  digitalWrite (noisePinR, volt);
  digitalWrite (noisePinL, volt);
  */

  /*
  voltint=generateNoise();
  analogWrite (noisePinR, voltint);
  analogWrite (noisePinL, voltint);
  */

  //generateNoise();

  
}
