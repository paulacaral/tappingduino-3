//Un timer controla dos pines de salida
//Estímulo: seno -pin 11 (OC1A)- Van Vugt script adaptation. pin 12: OC1B 
//Feedback: un timer controla dos pines:  seno -pin 5 (OC3A) y pin2 (OC3B) - Van Vugt script adaptation. pin 3: OC3C, pin 2: OC3B 
//trial eterno (sin Matlab)
//Manda estímulo al pin 11 y al pin 12 (timer 1)
//y feedback al pin 5 y al pin 2 (timer 3)

#define stimPinR 12
#define stimPinL 11
#define fdbkPinR 2
#define fdbkPinL 5
#define noisePinR 9
#define noisePinL 9
#define pinVG A11

#define LFSR_INIT  0xfeedfaceUL
#define LFSR_MASK  ((unsigned long)( 1UL<<31 | 1UL <<15 | 1UL <<2 | 1UL <<1  ))

//http://sphinx.mythic-beasts.com/~markt/ATmega-timers.html
boolean stimRight=true;  //pin12 - timer 1, channel B: right
boolean stimLeft=true;  //pin11 - timer 1, channel A: left
boolean fdbkRight=true; //pin2 - timer 3, channel B: right
boolean fdbkLeft=true;  //pin5 - timer 3, channel A: left
boolean noise = false;

unsigned long int t=0;
long int prevStim_t=0,prevFdbk_t=0;
boolean stim_flag=false;
boolean fdbk_flag=false;

unsigned int stimFreq = 440;//(C6) // defines the frequency (i.e., pitch) of the tone (in Hz)
unsigned int fdbkFreq = 660;//(C6) // defines the frequency (i.e., pitch) of the tone (in Hz)

int vg = 0;
int read_vg = 0;
int amplitude = 1;

uint16_t phaseIncrementStim = 0;  // 16 bit delta
uint16_t phaseIncrementFdbk = 0; // 16 bit delta
uint16_t phaseAccumulatorStim = 0;  // 16 bit accumulator
uint16_t phaseAccumulatorFdbk = 0; // 16 bit accumulator
int stim_counter, fdbk_counter;

// DDS resolution
//const uint32_t freq_samp = 31180; // 16MHz/513 porque ahora el pin está en modo 9 bits
const uint32_t freq_samp = 15610; // 16MHz/1025 porque ahora el pin está en modo 10 bits
const uint16_t resolution_DDS = pow(2,16)/freq_samp;


//AGREGO
uint16_t FDBK_DURATION_CYCLES = 23; // feedback duration (cycles)
uint16_t STIM_DURATION_CYCLES = 23; // stimulus duration (cycles)
#define STIM_DURATION 50 //stimulus duration (milliseconds)
#define FDBK_DURATION 50 //este lo agrego yo 
#define ANTIBOUNCE (0.5*isi)//minimum interval between responses (milliseconds)
boolean allow;
int fdbk, i;
unsigned int stim_number,fdbk_number;
unsigned int *event_number;
char *event_name;
unsigned long *event_time;
unsigned int event_counter; 

unsigned int isi=500,n_stim=3; //Entiendo que son valores iniciales por las dudas 
int perturb_size=0;  // estos los agrego paraque no tire error
unsigned int perturb_bip=0;
unsigned int event_type=0;
#define INPUTPIN A9
char message[20];
boolean SR=false, SL=false, FR=false, FL=false, NR=false, NL=false;

//////////// Set up lookup table for waveform generation
// sine wavefunction
const uint8_t  sineTable[] = {
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

const uint16_t  sineTable1024[] = {0x20C,
0x218,
0x225,
0x231,
0x23E,
0x24A,
0x256,
0x263,
0x26F,
0x27B,
0x287,
0x293,
0x29F,
0x2AB,
0x2B7,
0x2C2,
0x2CE,
0x2D9,
0x2E5,
0x2F0,
0x2FB,
0x306,
0x310,
0x31B,
0x325,
0x32F,
0x339,
0x343,
0x34D,
0x356,
0x35F,
0x368,
0x371,
0x379,
0x382,
0x38A,
0x392,
0x399,
0x3A1,
0x3A8,
0x3AF,
0x3B5,
0x3BB,
0x3C2,
0x3C7,
0x3CD,
0x3D2,
0x3D7,
0x3DC,
0x3E0,
0x3E4,
0x3E8,
0x3EB,
0x3EF,
0x3F2,
0x3F4,
0x3F6,
0x3F8,
0x3FA,
0x3FC,
0x3FD,
0x3FD,
0x3FE,
0x3FE,
0x3FE,
0x3FD,
0x3FD,
0x3FC,
0x3FA,
0x3F9,
0x3F7,
0x3F4,
0x3F2,
0x3EF,
0x3EC,
0x3E8,
0x3E4,
0x3E0,
0x3DC,
0x3D7,
0x3D2,
0x3CD,
0x3C8,
0x3C2,
0x3BC,
0x3B6,
0x3AF,
0x3A8,
0x3A1,
0x39A,
0x392,
0x38A,
0x382,
0x37A,
0x372,
0x369,
0x360,
0x357,
0x34D,
0x344,
0x33A,
0x330,
0x326,
0x31B,
0x311,
0x306,
0x2FB,
0x2F0,
0x2E5,
0x2DA,
0x2CF,
0x2C3,
0x2B8,
0x2AC,
0x2A0,
0x294,
0x288,
0x27C,
0x270,
0x263,
0x257,
0x24B,
0x23E,
0x232,
0x225,
0x219,
0x20C,
0x200,
0x1F3,
0x1E7,
0x1DA,
0x1CE,
0x1C1,
0x1B5,
0x1A8,
0x19C,
0x190,
0x184,
0x178,
0x16C,
0x160,
0x154,
0x148,
0x13C,
0x131,
0x125,
0x11A,
0x10F,
0x104,
0xF9,
0xEE,
0xE4,
0xDA,
0xCF,
0xC5,
0xBC,
0xB2,
0xA9,
0x9F,
0x96,
0x8E,
0x85,
0x7D,
0x75,
0x6D,
0x65,
0x5E,
0x57,
0x50,
0x49,
0x43,
0x3D,
0x37,
0x32,
0x2C,
0x27,
0x23,
0x1E,
0x1A,
0x16,
0x13,
0x10,
0xD,
0xA,
0x8,
0x6,
0x4,
0x3,
0x1,
0x1,
0x0,
0x0,
0x0,
0x1,
0x1,
0x2,
0x4,
0x5,
0x7,
0xA,
0xC,
0xF,
0x12,
0x16,
0x19,
0x1D,
0x22,
0x26,
0x2B,
0x30,
0x36,
0x3C,
0x42,
0x48,
0x4F,
0x55,
0x5C,
0x64,
0x6B,
0x73,
0x7B,
0x83,
0x8C,
0x95,
0x9E,
0xA7,
0xB0,
0xBA,
0xC3,
0xCD,
0xD8,
0xE2,
0xEC,
0xF7,
0x102,
0x10D,
0x118,
0x123,
0x12F,
0x13A,
0x146,
0x151,
0x15D,
0x169,
0x175,
0x181,
0x18E,
0x19A,
0x1A6,
0x1B2,
0x1BF,
0x1CB,
0x1D8,
0x1E4,
0x1F1,
0x1FF};
//media amplitudem
static const uint8_t  sineTable2[] PROGMEM = {
0x40,0x41,0x43,0x44,0x46,0x47,0x49,0x4A,0x4C,0x4E,0x4F,0x51,0x52,0x54,0x55,0x57,0x58,0x59,0x5B,0x5C,0x5E,0x5F,0x60,0x62,0x63,0x64,0x66,0x67,0x68,0x69,0x6A,0x6C,0x6D,0x6E,0x6F,0x70,0x71,0x72,0x73,0x74,0x75,0x76,0x76,0x77,0x78,0x79,0x79,0x7A,0x7B,0x7B,0x7C,0x7C,0x7D,0x7D,0x7E,0x7E,0x7E,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,0x7F,0x7E,0x7E,0x7E,0x7D,0x7D,0x7C,0x7C,0x7B,0x7B,0x7A,0x79,0x79,0x78,0x77,0x76,0x76,0x75,0x74,0x73,0x72,0x71,0x70,0x6F,0x6E,0x6D,0x6C,0x6A,0x69,0x68,0x67,0x66,0x64,0x63,0x62,0x60,0x5F,0x5E,0x5C,0x5B,0x59,0x58,0x57,0x55,0x54,0x52,0x51,0x4F,0x4E,0x4C,0x4A,0x49,0x47,0x46,0x44,0x43,0x41,0x40,0x3E,0x3C,0x3B,0x39,0x38,0x36,0x35,0x33,0x31,0x30,0x2E,0x2D,0x2B,0x2A,0x28,0x27,0x26,0x24,0x23,0x21,0x20,0x1F,0x1D,0x1C,0x1B,0x19,0x18,0x17,0x16,0x15,0x13,0x12,0x11,0x10,0xF,0xE,0xD,0xC,0xB,0xA,0x9,0x9,0x8,0x7,0x6,0x6,0x5,0x4,0x4,0x3,0x3,0x2,0x2,0x1,0x1,0x1,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x1,0x1,0x1,0x2,0x2,0x3,0x3,0x4,0x4,0x5,0x6,0x6,0x7,0x8,0x9,0x9,0xA,0xB,0xC,0xD,0xE,0xF,0x10,0x11,0x12,0x13,0x15,0x16,0x17,0x18,0x19,0x1B,0x1C,0x1D,0x1F,0x20,0x21,0x23,0x24,0x26,0x27,0x28,0x2A,0x2B,0x2D,0x2E,0x30,0x31,0x33,0x35,0x36,0x38,0x39,0x3B,0x3C,0x3E};


ISR(TIMER1_OVF_vect) {
  // wavetable lookup index (upper 8 bits of the accumulator)
  uint8_t index1 = 0;
  uint16_t aux1;
  //float aux1;
  
  // Update accumulator
  phaseAccumulatorStim += phaseIncrementStim;
  index1 = phaseAccumulatorStim >> 8;
  if(index1 <= (phaseIncrementStim >>8))  stim_counter++; // counter aumenta cuando index1 resetea

  OCR1A = vg;
  OCR1B = vg;

  
// if (t-prevStim_t<STIM_DURATION){
  if (stim_counter< STIM_DURATION_CYCLES){
  
   if(stim_flag==true){
    aux1 = (sineTable1024[index1]-511)*1+vg;//pgm_read_byte(&sineTable2[index1]);
    //Serial.println(sineTable5[index1]);
  // Read oscillator value for next interrupt
    
    if (stimLeft==true)  OCR1A = aux1;

    if (stimRight==true)   OCR1B = aux1;
  
  }  
 }

else  stim_flag=false;

}


ISR(TIMER3_OVF_vect) {
  // wavetable lookup index (upper 8 bits of the accumulator)
  uint8_t index3 = 0;
  uint16_t aux3;
  
  // Update accumulator
  phaseAccumulatorFdbk += phaseIncrementFdbk;
  index3 = phaseAccumulatorFdbk >> 8;
  if(index3 <= (phaseIncrementFdbk >>8))  fdbk_counter++; // counter aumenta cuando index1 resetea

  OCR3A = vg;
  OCR3B = vg;

//  if (t-prevFdbk_t<FDBK_DURATION){
  if (fdbk_counter< FDBK_DURATION_CYCLES){
    
    if(fdbk_flag==true){
      aux3 = pgm_read_byte(&sineTable[index3]);
    // Read oscillator value for next interrupt
   
      if (fdbkLeft==true)  OCR3A = aux3;
  
      if (fdbkRight==true)   OCR3B = aux3;
    
    }  
   }
  
  else  fdbk_flag=false;
  
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
 //TCCR1A= _BV(COM1A1) | _BV(COM1B1) | _BV(WGM11);

 // 10-bit Fast PWM - non inverted PWM
  TCCR1A= _BV(COM1A1) | _BV(COM1B1) | _BV(WGM11) | _BV(WGM10);

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
  uint16_t phaseIncr16 =  resolution_DDS * frequency;
  return phaseIncr16;//(phaseIncr32 >> 16);
}

uint16_t setCycles( uint16_t frequency ){
  return 0.05*frequency;
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
      phaseAccumulatorStim = 0;
      phaseIncrementStim = setFrequency(freq);
      stim_counter = 0;
      STIM_DURATION_CYCLES = setCycles(freq);
      stimRight = right;
      stimLeft = left;      
      break;
      
  
    case 'f':
      phaseAccumulatorFdbk = 0;
      phaseIncrementFdbk = setFrequency(freq);
      fdbk_counter = 0;
      FDBK_DURATION_CYCLES = setCycles(freq);
      fdbkRight = right;
      fdbkLeft = left;
      break;

  
    case 'n':
      amplitude = freq;
      if(right && left ==1)
        noise = true;
      else noise = false;
      break;
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
      case 'n':
        n_stim = data;
        break;
      case 'P':
        perturb_size = data;
        break;
      case 'B':
        perturb_bip = data;
        break;
      case 'E':
        event_type = data;
        break;
      case 'S':
        switch (field[1]){
          case 'R':
            SR = true;
            SL = false;
            break;
          case 'L':
            SR = false;
            SL = true;
            break;
          case 'B':
            SR = true;
            SL = true;
            break;
          case 'N':
            SR = false;
            SL = false;
            break;
        }
        break;
      case 'F':
        switch (field[1]){
          case 'R':
            FR = true;
            FL = false;
            break;
          case 'L':
            FR = false;
            FL = true;
            break;
          case 'B':
            FR = true;
            FL = true;
            break;
          case 'N':
            FR = false;
            FL = false;
            break;
        }
        break;

       case 'N':
        switch (field[1]){
          case 'B':
            NR = true;
            NL = true;
            break;
          case 'N':
            NR = false;
            NL = false;
            break;
        }
       
       case 'A':
        amplitude = data;
        break; 
        
      default:
        break;
    }
    line += n+1;
//    if (*line != ';')
  //    break;
//    while (*line == ';')
//      line++;
  }
  return;
}


//---------------------------------------------------------------------

void get_parameters() {
  char line[45];
  char i,aux='0';
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
  line[i] = '\0';         //terminate the string

  //just in case, clear incoming buffer once read
  //Serial.flush();
  //parse input chain into parameters
  parse_data(line);
  return;
}

//---------------------------------------------------------------------
void save_data(char ename, unsigned int enumber, unsigned long etime){
      //store event data
      event_name[event_counter] = ename;
      event_number[event_counter] = enumber;
      event_time[event_counter] = etime;
      event_counter++;

      switch(ename){
        case 'S':
          stim_number++;
          break;

        case 'F':
          fdbk_number++;
          break;
      }    
}


void setup() {

  Serial.begin(9600); //USB communication with computer
  pinMode(INPUTPIN,INPUT);
  
  cli();
  
  initTimers();
  
  // Unica lectura de tierra virtual hasta que el loop sea el correcto (condicion para iniciar)
  read_vg = readVirtualGround();
  vg = (int) (read_vg*1024/1024);
  //vg = (int) (read_vg*512/1024);

  allow = false;

  sei();
}



void loop() {

  if(allow == false){
    //just in case, clear incoming buffer once read
    Serial.flush();
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
    t = millis();

    //turn on noise
    SoundSwitch('n',amplitude,NL,NR);
    
    //send stimulus
    if ((t-prevStim_t)> isi && stim_flag==false) { //enciende el sonido
      SoundSwitch('s', stimFreq, SL, SR);
      prevStim_t=t;
      stim_flag=true;
      save_data('S', stim_number, t);
    }

    //read response
    if ((t - prevFdbk_t) > ANTIBOUNCE && fdbk_flag==false) {
      fdbk = digitalRead(INPUTPIN);
      if (fdbk == HIGH){
        SoundSwitch('f', fdbkFreq, FL, FR);
        prevFdbk_t=t;
        fdbk_flag=true;
        save_data('F', fdbk_number, t);
      }
    }

    //end trial
    //allow one more period (without stimulus)
    if (stim_number > n_stim && (t - prevStim_t) >= isi) {
      /*
      for (i=0; i<event_counter; i++) {
        sprintf(message,"%c %d %ld",event_name[i],event_number[i],event_time[i]);
        serial_print_string(message);
      }
      Serial.println("E");  //send END message
      */
      allow = false;

      //turn off noise 
      SoundSwitch('s',1,false,false);
      SoundSwitch('f',1,false,false);
      SoundSwitch('n',1,false,false);

      free(event_name);
      free(event_number);
      free(event_time); 
    }

  }
  
}
