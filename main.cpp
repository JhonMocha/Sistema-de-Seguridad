#include <inttypes.h>
#include <Adafruit_Sensor.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>
#include <util/delay.h>
#include "uart.h"
#include <stdlib.h>
#include "DHT22.h"

String lect;

void interrupt_INT_PCINT_Init(){
  cli(); //DESHABILITA TODAS LAS INTERRUPCIONES 
  EICRA = 0b1111;
  // REGISTRO EICRA - PERMITE HACER LAS CONEXIONES EN LOS 2 PINES: INT0 - INT1
  // FORMA QUE SE VA A DAR LA INTERRUPCIÓN - FLANCO DE SUBIDA
  EIMSK = 0b00000001;
  // REGRISTO EIMSK- PERMITE HABILITAR O DESABILITAR LAS INTERRUPCIONES EXTERNAS
  // EIMSK=0b00000001 - PARA INT0
  // REGISTRO EIFR
  sei(); // HABILITA EL USO DE LAS INTERRUPCIONES GLOBALES
}

ISR(INT0_vect){
  // tone (8,654,100);
  serial_print_str("SE DECTETO MOVIMIENTO");
  PORTB ^=(1<<PORTB0);
  _delay_ms(10000);
  PORTB ^=(1<<PORTB0);
}


int main(void)
{
  char rec1[20] ;
  char printbuff[10];
	float temperatura;
	float humedad;
	uint8_t contador=200;
  uint8_t contador2=200;
	DHT22_init();
  DDRB = 0B00000001;    //SE DEFINE LAS ENTRADAS DEL PUERTO B
  ADMUX = 0B01000000;	   //AVCC- AREF y ADC1
  ADCSRA = 0B00000111; 	 //PRE-SCALER  128 - DISABLED ANALOG CONVERTER & CONVERSION NOT STARTED
  ADCSRB = 0B00000000; 	 //FREE RUNNING MODE
  DIDR0 = 0B00000010;	   //ENABLE ANALOG MODE ADC1
  interrupt_INT_PCINT_Init();
  serial_begin(9600);
  while(1){

    lect="";
    if(Serial_available()>0){
      lect=Serial_readStringUntil('\r');
    }

    ADCSRA = 0B11000111; // ENABLED ANALOG CONVERTER & START CONVERSION
    while(ADCSRA & (1<< ADSC)); // ADSC DISABLED?
    int r = 100-((50.0/512.0)*ADC);
    // int r = ADC;
    contador++;
		if(contador>=200){			//Para leer el DHT22 cada 200x10ms = 2000ms y no utilizar retardos bloqueantes de 2s
			contador=0;
			
			uint8_t status = DHT22_read(&temperatura, &humedad);
			if (status & (lect=="/Detalles del tiempo,humedad y temperatura"))
			{

				serial_print_str("Temperatura: ");
				dtostrf(temperatura, 2, 2, printbuff);
				serial_print_str(printbuff );
				serial_print_str(" °C");
				serial_print_str("\t\t\t\t");

        serial_print_str("");
				serial_print_str("Humedad: ");
				dtostrf(humedad, 2, 2, printbuff );
				serial_print_str(printbuff);
				serial_println_str(" %");
			}
			else
			{
				serial_println_str("Error");
			}
    }else {
      _delay_ms(10);
      
    }
    contador2++;
    if(contador2>=200){
      contador2=0;
      if (lect=="/Clima"){
        if (r<=30){
          dtostrf(r, 2, 4, rec1);
          serial_print_str("ESTADO: ");
          //serial_print_str(rec1);
          //serial_print_str("\t\t\t\t");
          serial_println_str("SOLEADO");
        }else if (r <= 60 && r > 30){
          dtostrf(r, 2, 4, rec1);
          serial_print_str("ESTADO: ");
          //serial_print_str(rec1);
          //serial_print_str("\t\t\t\t");
          serial_println_str("LLUVIA");
        }else {
          dtostrf(r, 2, 4, rec1);
          serial_print_str("ESTADO: ");
          //serial_print_str(rec1);
          //serial_print_str("\t\t\t\t");
          serial_println_str("INUNDACIÓN");
        }
      }
    }
    else 
    {
      _delay_ms(10);
    }
  }return 0;
}