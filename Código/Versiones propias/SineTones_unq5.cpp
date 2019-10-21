/*************************************
 * Universidad Nacional de Quilmes	 *
 *       SineTones library               *
 * 					 *
 * 					 *
 * 					 *
 * 					 *
 * 					 *
 * Nombre: SineTones_unq.cpp		 *
 *************************************/ 

 
 
 
 #include <Arduino.h>
 #include "SineTones_unq5.h"
 
//---------------set variables and defines-------------------------------------
// PWM output 
#define pwmPin1A  11 //OC1A
#define pwmPin1B  12 //OC1B
#define pwmPin3A  5  //OC3A
#define pwmPin3B  2  //OC3B
#define pwmPin2A  10 //OC2A
#define pwmPin2B  9  //OC2B
//#define resolution 65536 //Resolución de pulsos (2^16)= 65536, 
//no se por que decía 68719;
#define LFSR_INIT  0xfeedfaceUL
#define LFSR_MASK  ((unsigned long)( 1UL<<31 | 1UL <<15 | 1UL <<2 | 1UL <<1  ))

#define mult 4

//sabe dios por que pasa esto (culpa de lujan)

// 16 bit delta
//uint16_t phaseIncrement = 0;
uint16_t phaseIncrement1r = 0, phaseIncrement1l = 0;
uint16_t phaseIncrement3r = 0, phaseIncrement3l = 0;

//Bools of channels on
boolean feedbackLeft  = true, feedbackRight = true, stimulusLeft  = true;
boolean stimulusRight = true, noiseLeft     = true, noiseRight    = true;

#define pinVG A10
int vg = 0;
//------------------------------------------------------------------------------

//-----------------Lookup table for waveform generation-------------------------
static const uint8_t  sineTable[] PROGMEM ={
0x80,0x83,0x86,0x89,0x8c,0x8f,0x92,0x95,0x98,0x9c,0x9f,0xa2,0xa5,0xa8,0xab,0xae,
0xb0,0xb3,0xb6,0xb9,0xbc,0xbf,0xc1,0xc4,0xc7,0xc9,0xcc,0xce,0xd1,0xd3,0xd5,0xd8,
0xda,0xdc,0xde,0xe0,0xe2,0xe4,0xe6,0xe8,0xea,0xec,0xed,0xef,0xf0,0xf2,0xf3,0xf5,
0xf6,0xf7,0xf8,0xf9,0xfa,0xfb,0xfc,0xfc,0xfd,0xfe,0xfe,0xff,0xff,0xff,0xff,0xff,
0xff,0xff,0xff,0xff,0xff,0xff,0xfe,0xfe,0xfd,0xfc,0xfc,0xfb,0xfa,0xf9,0xf8,0xf7,
0xf6,0xf5,0xf3,0xf2,0xf0,0xef,0xed,0xec,0xea,0xe8,0xe6,0xe4,0xe2,0xe0,0xde,0xdc,
0xda,0xd8,0xd5,0xd3,0xd1,0xce,0xcc,0xc9,0xc7,0xc4,0xc1,0xbf,0xbc,0xb9,0xb6,0xb3,
0xb0,0xae,0xab,0xa8,0xa5,0xa2,0x9f,0x9c,0x98,0x95,0x92,0x8f,0x8c,0x89,0x86,0x83,
0x80,0x7c,0x79,0x76,0x73,0x70,0x6d,0x6a,0x67,0x63,0x60,0x5d,0x5a,0x57,0x54,0x51,
0x4f,0x4c,0x49,0x46,0x43,0x40,0x3e,0x3b,0x38,0x36,0x33,0x31,0x2e,0x2c,0x2a,0x27,
0x25,0x23,0x21,0x1f,0x1d,0x1b,0x19,0x17,0x15,0x13,0x12,0x10,0x0f,0x0d,0x0c,0x0a,
0x09,0x08,0x07,0x06,0x05,0x04,0x03,0x03,0x02,0x01,0x01,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x01,0x02,0x03,0x03,0x04,0x05,0x06,0x07,0x08,
0x09,0x0a,0x0c,0x0d,0x0f,0x10,0x12,0x13,0x15,0x17,0x19,0x1b,0x1d,0x1f,0x21,0x23,
0x25,0x27,0x2a,0x2c,0x2e,0x31,0x33,0x36,0x38,0x3b,0x3e,0x40,0x43,0x46,0x49,0x4c,
0x4f,0x51,0x54,0x57,0x5a,0x5d,0x60,0x63,0x67,0x6a,0x6d,0x70,0x73,0x76,0x79,0x7c
};


static const uint8_t  sineTable3[] PROGMEM =
{
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

//------------------------------------------------------------------------------



uint8_t  index1r      = 0 , index1l      = 0;
uint16_t phaseAccum1r = 0 , phaseAccum1l = 0;

uint8_t index3r       = 0, index3l     = 0;
uint16_t phaseAccum3r = 0, phaseAccum3l= 0;


//----------------------Timers Interrupts Routines------------------------------
// TIMER1 overflow freq 62.5KHz.
ISR(TIMER1_OVF_vect){
  static uint8_t  osc1A        = 0, osc1B         = 0;

  // Send oscillator output to PWM
  OCR1A = osc1A; //timer 1 - Channel A - pin 11 - Right
  OCR1B = osc1B; //timer 1 - Channel B - pin 12 - Left

  // Update accumulator
  phaseAccum1r += phaseIncrement1r;
//  phaseAccum1l += phaseIncrement1l;
  index1r       = phaseAccum1r >> 8;
//  index1l       = phaseAccum1l >> 8;
  // Read oscillator value for next interrupt
  if (stimulusRight) 
    osc1A = pgm_read_byte( &sineTable[index1r] );
  else
   osc1A = (int) (vg*256/1024);
 // osc1A = 117;//pgm_read_byte( &sineTable3[1] );

  if (stimulusLeft) 
    osc1B = pgm_read_byte( &sineTable[index1r] );
  else
   osc1B = (int) (vg*256/1024);
   //osc1B = 117;//pgm_read_byte( &sineTable3[1] );

}

// TIMER3 overflow 62.5KHz.
ISR(TIMER3_OVF_vect){
  static uint8_t osc3A         = 0, osc3B       = 0;

  // Send oscillator output to PWM
  OCR3A = osc3A; // timer 3 - pin 5 - channel A - Right
  OCR3B = osc3B; // timer 3 - pin 2 - channel B - Left
  // Update accumulator
  phaseAccum3r += phaseIncrement3r;
//  phaseAccum3l += phaseIncrement3l;
  index3r       = phaseAccum3r >> 8;
//  index3l       = phaseAccum3l >> 8;
  // Read oscillator value for next interrupt
  if (feedbackLeft) 
    osc3A = pgm_read_byte( &sineTable[index3r] );
  else
    osc3A = 117;//pgm_read_byte( &sineTable3[1] );
  if (feedbackRight) 
    osc3B = pgm_read_byte( &sineTable[index3r] );
  else
    osc3B =117;// pgm_read_byte( &sineTable3[1] );*/
}

// TIMER2 overflow at 62.5kHz.
ISR(TIMER2_OVF_vect){//pseudorand noise
 
   uint8_t aux=0;
	static unsigned long int lfsr = LFSR_INIT;  

   if(lfsr & 1){
   lfsr =  (lfsr >>1) ^ LFSR_MASK;
   aux = 127+2;}
   else{
   lfsr >>= 1;
   aux = 127-2;}



   if(noiseRight) 
   	OCR2A = aux;
   if(noiseLeft)
   	OCR2B = aux;

}
//------------------------------------------------------------------------------

//----------------------------Function declarations ----------------------------
//initialize all timers at the same time, (1,2 and 3)
//whit their respectives pins
void initAllToneTimers(void){
  // Set pwm pins as output
  pinMode(pwmPin1A, OUTPUT);
  pinMode(pwmPin1B, OUTPUT);
  pinMode(pwmPin3A, OUTPUT);
  pinMode(pwmPin3B, OUTPUT);
  pinMode(pwmPin2A, OUTPUT);
  pinMode(pwmPin2B, OUTPUT);

  TIMSK1         |= _BV(TOIE1);  //se  puede pasar al init!
  //Dos Registros del timer1
  TCCR1A = _BV(COM1A1) | _BV(COM1B1) | _BV(WGM10);
  TCCR1B = _BV(CS10)   | _BV(WGM12);
  // Fast PWM 8bits non inverted, CTC, TOF1 on TOP (OCR1A)


  TIMSK3         |= _BV(TOIE3);
  //Dos Registros del timer3
  TCCR3A = _BV(COM3A1) | _BV(COM3B1) | _BV(WGM30);
  TCCR3B = _BV(CS30)   | _BV(WGM32);
  // Fast PWM 8bits non inverted, CTC, TOF3 on TOP (OCR3A)


  //Dos Registros del timer2
  TIMSK2 |= _BV(TOIE2);  
  TCCR2A  = _BV(COM2A1) | _BV(COM2B1) | _BV(WGM21) | _BV(WGM20);
  TCCR2B  = _BV(CS20)   ;//| _BV(WGM22);
  // Fast PWM 8bits non inverted, CTC, TOF2 on TOP (OCR2A)

  tickOff('n',500,true,true,3);
}


/* Translates the desired output frequency to a phase
 increment to be used with the phase accumulator.*/
uint16_t setFrequency( uint16_t frequency ){
  uint32_t phaseIncr64 =  ((uint32_t)frequency) <<16;//resolution * frequency;
  return (phaseIncr64 >> 16);
}

// function to turn tick on
void tickOn(char tipo,uint16_t freq, boolean left, boolean right){
/* This function enables the timerOverflowInterrupt in the time Mask 
Depending on tipo, if tipo is 's', selects Timer 1 (stimulus)
if tipo is 'f' selects Timer 3 (feedback)
if tipo is 'n' selects Timer.. (Noise)
the left and right bools as true or false selects the channels where
the signals will come out*/
  if (tipo=='s'){//Stimulus 
    phaseIncrement1r = setFrequency(freq);
    stimulusRight    = right;
    stimulusLeft     = left;
  }
  if (tipo=='f'){//Feedback
    phaseIncrement3r = setFrequency(mult*freq);
    feedbackRight    = right;
    feedbackLeft     = left;
  }
  if (tipo=='n'){//Noise

    noiseRight      = right;
    noiseLeft       = left;
  }
}

// function to turn tick off
void tickOff(char tipo,uint16_t freq, boolean left, boolean right, int vg_value) {
/* Disable the timerOverflowInterrupt based on 'tipo'*/
  if (tipo=='s'){//Stimulus
    if(right){ 
      stimulusRight    = false;}//!right;}
    if(left){ 
      stimulusLeft     = false;}//!left;}
    vg = vg_value;
  }
  if (tipo=='f'){
    if(right){
      feedbackRight    = false;}//!right;}
    if(left){
      feedbackLeft     = false;}//!left;}
    vg = vg_value;
  }
  if (tipo=='n'){

    noiseRight      = !right;
    noiseLeft       = !left;
  } //dejo el comp en la mitad, para tener 2.5v sirve?
}


long int prevStim_t=0,prevResp_t=0;
boolean stim_flag=false,resp_flag=false;

void tickOnWhile(char tipo,uint16_t freq, boolean left, boolean right,
		uint16_t cadaCuanto, uint16_t cuanto, uint64_t t){
	boolean *flag;
	long int *prev_t;
	if (tipo=='s'){
	flag   = &stim_flag;
	prev_t = &prevStim_t;
	}	
	if (tipo=='f'){
	flag   = &resp_flag;
	prev_t = &prevResp_t;
	}


      if ((t-*prev_t)>cadaCuanto && *flag==false) { //enciende el tono estimulo
       
        tickOn(tipo, freq ,left,right);
        *prev_t=t;
        *flag=true;
      }
      
      if (t-*prev_t>cuanto && *flag==true){ //apaga el tono estimulo

      vg = readVirtualGround();
      tickOff(tipo,freq,left,right,vg);
      *flag=false;
      }  
}








int readVirtualGround(void) {
  int pin = pinVG;
  return analogRead(pin);}
//------------------------------------------------------------------------------

/*******************************************************************************
* This is the end of library, made in Universidad nacional de quilmes          *
* Version = 0.0.1 may 25th of 2018											   *
*******************************************************************************/
