/*************************************
 * Universidad Nacional de Quilmes	 *
 *       SineTones library           *
 * 									 *
 * 									 *
 * 									 *
 * 									 *
 * 									 *
 * Nombre: SineTones_unq.h			 *
 *************************************/ 
 
#ifndef _SINETONES_UNQ_H

	#define _SINETONES_UNQ_H

	int readVirtualGround(void);
	void initAllToneTimers(void);
	// -------- Prototipos de funciones Publicas ---------------
	void initOneToneTimer(char);
	
	uint16_t setFrequency( uint16_t);

	void tickOn(char, uint16_t, boolean, boolean);
	void tickOff(char, uint16_t, boolean, boolean, int);
#endif

/*------------------------------------------------------------*-
---- END OF FILE --------------------------------------------
-*------------------------------------------------------------*/
