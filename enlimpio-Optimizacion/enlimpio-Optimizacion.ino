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
boolean stimRight=true;	//pin11 - timer 1, channel A: right
boolean stimLeft=true;	//pin12 - timer 1, channel B: left
boolean fdbkRight=true;	//pin5 - timer 3, channel A: right
boolean fdbkLeft=true;	//pin2 - timer 3, channel B: left
boolean noise = false;

unsigned long int prevStim_t=0,prevFdbk_t=0,prevNoise_t=0,prevNoise4_t=0,t=0;
boolean stim_flag=false;
boolean fdbk_flag=false;

unsigned int stimFreq = 440;//(C6) // defines the frequency (i.e., pitch) of the tone (in Hz)
unsigned int fdbkFreq = 660;//(C6) // defines the frequency (i.e., pitch) of the tone (in Hz)

int vg = 0;
int read_vg = 0;
int amplitud = 1;

uint16_t phaseIncrementStim = 0;  // 16 bit delta
uint16_t phaseIncrementFdbk = 0; // 16 bit delta
uint16_t phaseAccumulatorStim = 0;  // 16 bit accumulator
uint16_t phaseAccumulatorFdbk = 0; // 16 bit accumulator


// DDS resolution - NO PONER 65536
const uint32_t resolution = 2*68719;//68719;  // el 2 multiplicando es por el modo del timer usado

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
    OCR2B = generateNoise(amplitud, vg);
  else
    OCR2B = vg;    
  }

void initTimers(void){
  // Stimulus
  // Set pins as output
  pinMode(stimPinR,OUTPUT);
  pinMode(stimPinL,OUTPUT);

  // 8-bit Fast PWM - non inverted PWM
  //  TCCR1A= _BV(COM1A1) | _BV(COM1B1) | _BV(WGM10);
  TCCR1A= _BV(COM1A1) | _BV(COM1B1) | _BV(WGM11);//| _BV(WGM10);
  //"_BV" viene de Bit Value porque convierte valores de bit number a byte value, que es lo que se puede configurar en los registros.
  // Start timer without prescaler
  //  TCCR1B = _BV(WGM12) | _BV(CS12);
  TCCR1B = _BV(WGM12) | _BV(CS10);
  // Enable overflow interrupt for OCR1A
  TIMSK1 = _BV(TOIE1);

  // Feedback
  // Set pins as output
  pinMode(fdbkPinR,OUTPUT);
  pinMode(fdbkPinL,OUTPUT);

  // 8-bit Fast PWM - non inverted PWM
  //  TCCR3A= _BV(COM3A1) | _BV(COM3B1) | _BV(WGM30); //COM3A1 habilita channel A y COM3B1 el channel B. Hay que hacerlo en orden
  TCCR3A= _BV(COM3A1) | _BV(COM3B1) | _BV(WGM31);//| _BV(WGM30); //COM3A1 habilita channel A y COM3B1 el channel B. Hay que hacerlo en orden
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
unsigned int generateNoise(int amplitud, int vg_value){ 
   uint8_t aux=0;
   static unsigned long int lfsr = LFSR_INIT;  // See https://en.wikipedia.org/wiki/Linear_feedback_shift_register#Galois_LFSRs
   // 32 bit init, nonzero
   // If the output bit is 1, apply toggle mask. The value has 1 at bits corresponding to taps, 0 elsewhere.
   
   if(lfsr & 1) { 
    lfsr =  (lfsr >>1) ^ LFSR_MASK; 
    aux = vg_value+amplitud;
    }
   else{
    lfsr >>= 1;
    aux = vg_value-amplitud;
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
  uint32_t phaseIncr64 =  resolution * frequency;
  return (phaseIncr64 >> 16);
}

// Function to start playing sound
void PlaySound(char tipo,uint16_t freq, boolean left, boolean right){
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
      phaseAccumulatorStim = 0;
      if(right){ 
        stimRight    = true;
      }
      if(left){ 
        stimLeft     = true;
      }
      break;
  
    case 'f':
      phaseIncrementFdbk = setFrequency(freq);
      phaseAccumulatorFdbk = 0;
      if(right){ 
        fdbkRight    = true;
      }
      if(left){ 
        fdbkLeft     = true;
      }
      break;
  
    case 'n':
      amplitud = freq;
      noise = true;
      break;
  }  
}

// Function to turn sound off
void StopSound(char tipo,uint16_t freq, boolean left, boolean right) {
/* Disable the timerOverflowInterrupt based on 'tipo'*/
  switch(tipo){
    case 's':
      if(right){ 
        stimRight    = false;
      }
      if(left){ 
        stimLeft     = false;
      }
      break;
  
    case 'f':
      if(right){
        fdbkRight    = false;
      }
      if(left){
        fdbkLeft     = false;
      }
      break;
  }
}


void PlaySoundWhile(char tipo,uint16_t freq, boolean left, boolean right, uint16_t cadaCuanto, uint16_t cuanto, uint64_t t){  
  boolean *flag;
  long int *prev_t;
  switch(tipo){
    case 's':
      flag   = &stim_flag;
      prev_t = &prevStim_t;
      break;

    case 'f':
      flag   = &fdbk_flag;
      prev_t = &prevFdbk_t;
      break;
  }

  if ((t-*prev_t)>cadaCuanto && *flag==false) { //enciende el sonido
    PlaySound(tipo, freq ,left,right);
    *prev_t=t;
    *flag=true;
  }
      
  if (t-*prev_t>cuanto && *flag==true){ //apaga el sonido
    StopSound(tipo,freq,left,right);
    *flag=false;
  }  
}



void setup() {

	cli();
  
  initTimers();

  // Unica lectura de tierra virtual hasta que el loop sea el correcto (condicion para iniciar)
  read_vg = readVirtualGround();
  vg = (int) (read_vg*256/1024);
  
	sei();
}



void loop() {

	t = millis();

  PlaySoundWhile('s',stimFreq, true, true, 500, 50, t);

  PlaySoundWhile('f',fdbkFreq, true, true, 600, 50, t);

  PlaySound('n',1,true,true);
  
}
