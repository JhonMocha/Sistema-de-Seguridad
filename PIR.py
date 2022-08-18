# from machine import Pin 
import RPi.GPIO as GPIO
import time
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Pir = Pin(0,Pin.IN) # Entrada GP0

def movement(self):
    print("Se decteto movimiento")

GPIO.setup(18, GPIO.IN) # PIN #12 COMO ENTRADA
GPIO.add_event_detect(18, GPIO.RISING, callback=movement) #INTERRUPCION EN FLANCO DE SUBIDA 

# Pir.irq(trigger=Pin.IRQ_RISING, handler=movement) #INTERRUPCION EN FLANCO DE SUBIDA 

while True:
    pass

# Si sale Error probar con IRQ_FALLING,