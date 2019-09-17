/*
 * Este archivo es prueba_librerias_Ulises.ino pero cambiando el include de 
 * #include <SineTonesUNQ.h>
 * a #include <SineTones_unq.h>
 */
// PWM output 
#define pwmPin1A  11 //OC1A
#define pwmPin1B  12 //OC1B
#define pwmPin3A  5  //OC3A
#define pwmPin3B  2  //OC3B
#define pwmPin2A  10 //OC2A
#define pwmPin2B  9  //OC2B
#include <SineTones_unq5.h>



//long int prevStim_t=0,prevResp_t=0;
long int prevn_t=0,t=0;
//boolean stim_flag=false;
//boolean resp_flag=false;
boolean n_flag=false;

// variables for tone condition
int tone_freq1 = 440;//495;//1046.5; // defines the frequency of the tone (in Hz)
int tone_freq3 = 660;//1800;//1046.5; // defines the frequency of the tone (in Hz)

int pos = 0;
int vg_value = 0;





void setup() {
  pinMode(pwmPin1A, OUTPUT);
  pinMode(pwmPin1B, OUTPUT);
  pinMode(pwmPin2A, OUTPUT);
  pinMode(pwmPin2B, OUTPUT);
  pinMode(pwmPin3A, OUTPUT);
  pinMode(pwmPin3B, OUTPUT); // estos pinmodes estan tambien en la librería en el initAllToneTimers
  //se puede poner en cualquiera de los 2. NO CAMBIA NADA RODRIGO!!!!!
  vg_value = readVirtualGround();
  analogWrite(pwmPin1A,vg_value>>4);
  analogWrite(pwmPin1B,vg_value>>4);
  analogWrite(pwmPin2A,vg_value>>4);
  analogWrite(pwmPin2B,vg_value>>4);
  analogWrite(pwmPin3A,vg_value>>4);
  analogWrite(pwmPin3B,vg_value>>4);//Esto tampoco hace falta pero Rodrigo quería

  
  Serial.begin(9600);
  cli();
  //pinMode(pinVG,INPUT);
  initAllToneTimers();// inicializa los timers para los tone
  tickOn('n',500,true,true);
  /*existe una que es initToneTimer(char) donde el char puede ser
  's' de stimulus, 'f' de feedback, o 'n' de noise. que inicializa 
  solo un timer, por si no se quisieran utilizar los 3 en algún
  trial*/
  //tickOff('s',500,true,true,3);
  //tickOn('n',500,true,true);


  sei();
  }


void loop(){
  
      t=millis();
      
      tickOnWhile('s',tone_freq1,true,true,500,50,t); 
      tickOnWhile('f',tone_freq3,true,true,600,50,t);          

  
  }
