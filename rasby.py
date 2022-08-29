# COMUNICACION CON ARDUINO"
from serial import*
from time import*

# ENVIO DE CORREO 
import smtplib
from datetime import datetime 
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 

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
correo_origen = '********@gmail.com'  # COLOCAR CORREO DE ORIGEN - CONFIGURAR LA CUENTA PARA QUE PUEDA RECIBIR CORREOS
contrasena = '***********'            # COLOCAR LA CONTRASEÑA DEL CORREO ORRIGEN
correo_destino = '*******@gmail.com'  # COLOCAR CORREO DE DESTINO

# CAMARA
P = PiCamera()
#P.resolution = (1024,768)
P.start_preview()


sleep(5)
camara.capture("Direccion donde se quiere guardar la imagen")
camara.stop_preview()


atmega = Serial('/dev/ttyACM0',9600)

# SE USA EL MODO BCM
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Configurar el canal de salida GPIO
GPIO.setup(27, GPIO.OUT)# PIN #11 - COMO SALIDAD - ALARMA
GPIO.setup(18, GPIO.IN) # PIN #12 - COMO ENTRADA - PIR
GPIO.setup(23, GPIO.IN) # PIN #16 - COMO ENTRADA - Temperatura y Humedad

# SENSOR DE TEMPERATURA Y HUMEDAD 

sensor = Adafruit_DHT.DHT22
pin = 23  # PIN 16 - TEMPERATURA Y HUMEDAD 

# ENVIAR CORREO
def Enviar_correo():
    
    time.sleep(1)
    P.capture('/home/pi/Sistema-de-Seguridad/movement.jpg')
    time.sleep(4)
    msg= MIMEMultipart("related")
    msg['Subject']= 'ALERTA! SISTEMA DE SEGURIDAD' # ASUNTO DEL CORREO
    msg['From'] = correo_origen
    msg['To'] = correo_destino
    msg.preamble="Esto es el preambulo"

    msgAlternative= MIMEMultipart("alternative")
    msg.attach(msgAlternative)

    msgText=MIMEText("Alarma encendidad, se decteto movimiento en la finca")
    msgAlternative.attach(msgText)

    fp=open('/home/pi/Sistema-de-Seguridad/movement.jpg','rb')
    img=MIMEImage(fp.read())
    fp.close()


    img.add_header("Content-ID","<image1>")
    msg.attach(img)

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()  
    server.login(correo_origen,contrasena)
    server.sendmail(correo_origen,correo_destino,msg.as_string())
    print("Su Email ha sido enviado.")
    server.quit()

# DECTECTAR MOVIMIENTO
def movement(self):
    Enviar_correo()
    print("Se decteto movimiento")
    GPIO.output(27,GPIO.HIGH)
    time.sleep(5)
    GPIO.output(27,GPIO.LOW)

# COMUNICACION CON TELEGRAM
def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print ('Received: %s' % command)

    if command == '/Activar':
        telegram_bot.sendMessage (chat_id, str("Bienvenido al Sistema de Seguidad, ingrese comando a ejercutar: "))

    elif command == '/Detalles':
        telegram_bot.sendMessage(chat_id, str("Hora: ")+str(now.hour)+str(":")+str(now.minute))
        humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)
        if humedad is not None and temperatura is not None:
            temperatura1= round(temperatura,2)
            humedad1= round(humedad,2)
            telegram_bot.sendMessage(chat_id, str("Temperatura=")+str(temperatura1)+str("°C")+str(" ")+str("Humedad=")+str(humedad1)+str("%")) 
        else:
            print('Fallo la lectura del sensor.Intentar de nuevo')

    elif command == '/Clima':
        try:
            atmega.write(command.encode())
            atmega.write('\r'.encode())
            atmega.flushInput()
            print("Enviado")
            sleep(1)
            try:
                print("Recibiendo datos....")
                while not( atmega.in_waiting > 0):
                    print("datos recibidos")
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
        GPIO.output(27,GPIO.HIGH)
        telegram_bot.sendMessage (chat_id, str("ALARMA ENCENDIDA"))
    elif command =='/off':
        GPIO.output(27,GPIO.LOW)
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
