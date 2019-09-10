/*
 * Este archivo es prueba_librerias_Ulises.ino pero cambiando el include de 
 * #include <SineTonesUNQ.h>
 * a #include <SineTones_unq.h>
 */

#include <SineTones_unq4.h>



long int prevStim_t=0,prevResp_t=0,prevn_t=0,t=0;
boolean stim_flag=false;
boolean resp_flag=false;
boolean n_flag=false;

// variables for tone condition
int tone_freq1 = 495;//1046.5; // defines the frequency of the tone (in Hz)
int tone_freq3 = 1800;//1046.5; // defines the frequency of the tone (in Hz)


int pos = 0;
int vg_value = 0;





void setup() {
  
 Serial.begin(9600);
  // Initialise fast PWM
  cli();
//  pinMode(pinVG,INPUT);
  initOneToneTimer('s');
  initOneToneTimer('f');
  initOneToneTimer('n');
  //tickOn('n',500,true,true);
  //initAllToneTimers();// inicializa los timers para los tone
  /*existe una que es initToneTimer(char) donde el char puede ser
  's' de stimulus, 'f' de feedback, o 'n' de noise. que inicializa 
  solo un timer, por si no se quisieran utilizar los 3 en algún
  trial*/
  //tickOff('s',500,true,true,3);
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
//    vg_value = readVirtualGround(pinVG);
  
  
      t=millis();
      //if (t%1000 == 0)
          //Serial.println(vg_value);

      if ((t-prevStim_t)>600 && stim_flag==false) { //enciende el tono estimulo
       
        tickOn('s',tone_freq1,true,false);

        //tickOn('s',tone_freq3,true,true);
        prevStim_t=t;
        stim_flag=true;
      }

      if (t-prevStim_t>50 && stim_flag==true){ //apaga el tono estimulo
       
      //tickOff('s',tone_freq1,false,true);
     vg_value = readVirtualGround();
      tickOff('s',tone_freq1,true,true,vg_value);

      //tickOff('f',tone_freq3,true,true);
      stim_flag=false;
      }    


      if ((t-prevResp_t)>550 && resp_flag==false) { //enciende el tono feedback
       
        tickOn('f',tone_freq3,true,true);
        //tickOn('f',tone_freq3,true,true);
        prevResp_t=t;
        resp_flag=true;
      }

      if (t-prevResp_t>50 && resp_flag==true){ //apaga el tono feedback
       
      //tickOff('s',tone_freq1,false,true);
      tickOff('f',tone_freq3,true,true,53);
      
      //tickOff('f',tone_freq3,true,true);
      resp_flag=false;
      }    
      


      if ((t-prevn_t)>3000 && n_flag==false) { //enciende el tono feedback

        tickOn('n',tone_freq3,true,true);
        //tickOn('f',tone_freq3,true,true);
        prevn_t=t;
        n_flag=true;
      }

      if (t-prevn_t>500 && n_flag==true){ //apaga el tono feedback
       
      //tickOff('s',tone_freq1,false,true);
      tickOff('n',tone_freq3,true,true,53);
      
      //tickOff('f',tone_freq3,true,true);
      n_flag=false;
      }    


     
  }
