#include <SineTonesUNQ.h>


long int prevStim_t=0,prevResp_t=0,t=0;
boolean stim_flag=false;
boolean resp_flag=false;

// variables for tone condition
int tone_freq1 = 495;//1046.5; // defines the frequency of the tone (in Hz)
int tone_freq3 = 1800;//1046.5; // defines the frequency of the tone (in Hz)


int pos = 0;

void setup() {
 //Serial.begin(38400);
  // Initialise fast PWM
  cli();
 
  initAllToneTimers();// inicializa los timers para los tone
  /*existe una que es initToneTimer(char) donde el char puede ser
  's' de stimulus, 'f' de feedback, o 'n' de noise. que inicializa 
  solo un timer, por si no se quisieran utilizar los 3 en algún
  trial*/
  
  //tickOn('n',500,true,true);
  /*la función tickOn prende el tono de ruido, feed
   * o stimulus. a la frecuencia freq, y en los 
   * chanels right o left respectivamente.
   * el ruido se activa siempre en los dos canales,
   * y se le puede poner cualquier frecuencia porque
   * la ignora
   */
 
  sei();
  }


void loop(){
      t=millis();
      if ((t-prevStim_t)>600 && stim_flag==false) { //enciende el tono estimulo
       
        tickOn('s',tone_freq1,true,false);
        //tickOn('s',tone_freq3,true,true);
        prevStim_t=t;
        stim_flag=true;
      }

      if (t-prevStim_t>50 && stim_flag==true){ //apaga el tono estimulo
       
      //tickOff('s',tone_freq1,false,true);
      tickOff('s',tone_freq1,true,false);
      
      //tickOff('f',tone_freq3,true,true);
      stim_flag=false;
      }    


      if ((t-prevResp_t)>550 && resp_flag==false) { //enciende el tono feedback
       
        tickOn('f',tone_freq1,false,true);
        //tickOn('f',tone_freq3,true,true);
        prevResp_t=t;
        resp_flag=true;
      }

      if (t-prevResp_t>50 && resp_flag==true){ //apaga el tono feedback
       
      //tickOff('s',tone_freq1,false,true);
      tickOff('f',tone_freq3,false,true);
      
      //tickOff('f',tone_freq3,true,true);
      resp_flag=false;
      }    
      
     
  }

