#include <Arduino.h>
#include <inttypes.h>
#include <Arduino.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>
#include <util/delay.h>
#include <stdlib.h>
String lect;
char rec1[20] ;

void setup() {
  DDRB = 0B00000001;    //SE DEFINE LAS ENTRADAS DEL PUERTO B
  ADMUX = 0B01000000;	   //AVCC- AREF y ADC1
  ADCSRA = 0B00000111; 	 //PRE-SCALER  128 - DISABLED ANALOG CONVERTER & CONVERSION NOT STARTED
  ADCSRB = 0B00000000; 	 //FREE RUNNING MODE
  DIDR0 = 0B00000010;	   //ENABLE ANALOG MODE ADC1
  Serial.begin(9600);
 
}

void loop() {
  lect="";
  if(Serial.available()>0){
    lect=Serial.readStringUntil('\r');
  }
  ADCSRA = 0B11000111; // ENABLED ANALOG CONVERTER & START CONVERSION
  while(ADCSRA & (1<< ADSC)); // ADSC DISABLED?
  int r = 100-((50.0/512.0)*ADC);
  if (lect == "/Clima"){
    if (r<=30){
      dtostrf(r, 2, 4, rec1);
      Serial.println("ESTADO: SOLEADO");
    }else if (r <= 60 && r > 30){
      dtostrf(r, 2, 4, rec1);
      Serial.println("ESTADO: LLUVIA");
    }else {
      dtostrf(r, 2, 4, rec1);
      Serial.println("ESTADO: INUNDACIÓN");
    }
  }  
  delay(250);
}