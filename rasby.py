# COMUNICACION CON ARDUINO"
from serial import*
from time import*

# ENVIO DE CORREO 
import smtplib
from email.mime.text import MIMEText

# COMUNICACIÓN CON TELEGRAM
import time, datetime
import telepot
from telepot.loop import MessageLoop

# SENSOR DE TEMPERATURA DH22T
import Adafruit_DHT

# PINES DE LA RASBERRY
import sys
import subprocess
import RPi.GPIO as GPIO

# CAMARA
from picamera import PiCamera
from time import sleep

now = datetime.datetime.now()

# VARIABLES GLOBALES
correo_origen = 'cuentaenvio2@gmail.com'
contraseña = 'zomrmtuqgtmpdsez'
correo_destino = 'jmochaM@gmail.com'

atmega = Serial('/dev/ttyACM0',9600)
atmega.flushInput()

# SE USA EL MODO BCM
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Configurar el canal de salida GPIO
GPIO.setup(17, GPIO.OUT)# PIN #11 - COMO SALIDAD - ALARMA
GPIO.setup(18, GPIO.IN) # PIN #12 - COMO ENTRADA - PIR
GPIO.setup(23, GPIO.IN) # PIN #16 - COMO ENTRADA - Temperatura y Humedad

# SENSOR DE TEMPERATURA Y HUMEDAD 

sensor = Adafruit_DHT.DHT22
pin = 23  # PIN 16 - TEMPERATURA Y HUMEDAD 

# ENVIAR CORREO
def Enviar_correo():

    msg= MIMEText("Alarma encendida, se decteto movieminto en la finca")  # CORREO A ENVIAR 
    msg['Subject']= 'ALERTA! SISTEMA DE SEGURIDAD' # ASUNTO DEL CORREO
    msg['From'] = correo_origen
    msg['To'] = correo_destino

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()  
    server.login(correo_origen,contraseña)
    server.sendmail(correo_origen,correo_destino,msg.as_string())
    print("Su Email ha sido enviado.")
    server.quit()

# DECTECTAR MOVIMIENTO
def movement(self):
    Enviar_correo()
    print("Se decteto movimiento")
    # on(17)
    # time.sleep(10)
    # off(17)

# COMUNICACION CON TELEGRAM
def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print ('Received: %s' % command)

    if command == '/Activar':
        telegram_bot.sendMessage (chat_id, str("Bienvenido al Sistema de Seguidad, ingrese comando a ejercutar: "))

    elif command == '/Detalles del tiempo,humedad y temperatura':
        telegram_bot.sendMessage(chat_id, str("Hora: ")+str(now.hour)+str(":")+str(now.minute))
        humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)
        if humedad is not None and temperatura is not None:
            telegram_bot.sendMessage(chat_id, str("Temperatura=")+str(temperatura)+str("°C")+str(" ")+str("Humedad=")+str(humedad)+str("%"))
            print(f'Temperatura={temperatura:.2f}°C  Humedad={humedad:.2f}%')
            #print("Temperatura = {}°C humedad = {}% ".format(temperatura,humedad))  
        else:
        print('Fallo la lectura del sensor.Intentar de nuevo')

    elif command == '/Clima':
        try:
            atmega.write(command.encode())
            atmega.write('\r'.encode())
            atmega.flushInput()
            sleep(1)
            try:
                while not( atmega.in_waiting > 0):
                    sleep (1.5)
                    pass
                mens = atmega.readline().strip()
                print ('Received: %s' % mens)
                telegram_bot.sendMessage(chat_id, str(mens.decode()))
            except:
                print("no data recive")
        except(KeyboardInterrupt,SystemExit):
            print("")
            print("hasta la vista ")
            atmega.close()
    elif command =='/on':
        GPIO.output(17,GPIO.HIGH)
        telegram_bot.sendMessage (chat_id, str("ALARMA ENCENDIDA"))
    elif command =='/off':
        GPIO.output(17,GPIO.LOW)
        telegram_bot.sendMessage (chat_id, str("ALARMA APAGADA"))


telegram_bot = telepot.Bot('5493887556:AAEJue3IwpUpoQ_fWH-oUPWnOI9icTM0-rY')
print (telegram_bot.getMe())

MessageLoop(telegram_bot, action).run_as_thread()
print ('Up and Running....')


GPIO.add_event_detect(18, GPIO.RISING, callback=movement) #INTERRUPCION EN FLANCO DE SUBIDA


while 1:
    try:
        time.sleep(5)

    except(KeyboardInterrupt):
        print("\n Program Interrupted")
        GPIO.cleanup()
        exit()
    
    except:
        print('Ocurrio otro error o excepción')
        GPIO.cleanup()
