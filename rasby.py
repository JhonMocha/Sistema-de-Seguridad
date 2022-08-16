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

# PINES DE LA RASBERRY
import sys
import subprocess
import RPi.GPIO as GPIO

now = datetime.datetime.now()

# VARIABLES GLOBALES
correo_origen = 'cuentaenvio2@gmail.com'
contraseña = 'zomrmtuqgtmpdsez'
correo_destino = 'jmochaM@gmail.com'

atmega = Serial('/dev/ttyACM0',9600)
atmega.flushInput()

# SE USA EL MODO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Configurar el canal de salida GPIO
GPIO.setup(17, GPIO.OUT)# PIN #11 - COMO SALIDAD - ALARMA
GPIO.setup(18, GPIO.IN) # PIN #12 - COMO ENTRADA - PIR

# VARIABLES 
Var1X=subprocess.check_output('python Stemperatura.py', shell=True)

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

# ALARMA
def on(pin):
    GPIO.output(pin,GPIO.HIGH)
    return

def off(pin):
    GPIO.output(pin,GPIO.LOW)
    return

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
        telegram_bot.sendMessage(chat_id, str(Var1X))
    elif command == '/Clima':
        try:
            atmega.write(command.encode('latin-1')) # PARA EVITAR ERRORES AL MOMENTO DE CODIFICAR SE USA "latin-1"
            lineBytes = atmega.readline()
            line=lineBytes.decode('latin-1').strip()
            mens=line
            print ('Received_ %s' % mens)
            telegram_bot.sendMessage(chat_id, str(mens))
        except(KeyboardInterrupt,SystemExit):
            print("")
            print("hasta la vista ")
            atmega.close()
    elif command =='/on':
        telegram_bot.sendMessage (chat_id, on(17))
        telegram_bot.sendMessage (chat_id, str("ALARMA ENCENDIDA"))
    elif command =='/off':
        telegram_bot.sendMessage (chat_id, off(17))
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
