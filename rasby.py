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

now = datetime.datetime.now()

# VARIABLES GLOBALES
correo_origen = 'cuentaenvio2@gmail.com'
contraseña = 'zomrmtuqgtmpdsez'
correo_destino = 'jmochaM@gmail.com'

atmega = Serial('/dev/ttyACM0',9600)
sleep(2)

def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print 'Received: %s' % command

    if command == '/Activar':
        telegram_bot.sendMessage (chat_id, str("Bienvenido al Sistema de Seguidad, ingrese comando a ejercutar: "))

    elif command == '/Detalles del tiempo,humedad y temperatura':
        telegram_bot.sendMessage(chat_id, str("Hora: ")+str(now.hour)+str(":")+str(now.minute))
        try:
            atmega.write(command.encode())
            atmega.write('\r'.encode())
            atmega.flushInput()
            #print ("enviado")
            sleep(3)
            try:
                #print ("recibiendo datos: ")
                while not( atmega.in_waiting > 0):
                    #print ("datos recibidos")
                    sleep (1.5)
                    pass
                #print ()
                mens = atmega.readline().strip()
                telegram_bot.sendMessage(chat_id, str(mens.decode()))
                #print (mens.decode())
            except:
                print("no data recive")
        except(KeyboardInterrupt,SystemExit):
            print("")
            print("hasta la vista ")
            atmega.close()
    elif command == '/Clima':
        try:
            atmega.write(command.encode())
            atmega.write('\r'.encode())
            atmega.flushInput()
            #print ("enviado")
            sleep(3)
            try:
                #print ("recibiendo datos: ")
                while not( atmega.in_waiting > 0):
                    #print ("datos recibidos")
                    sleep (1.5)
                    pass
                #print ()
                mens = atmega.readline().strip()
                telegram_bot.sendMessage(chat_id, str(mens.decode()))
                #print (mens.decode())
            except:
                print("no data recive")
        except(KeyboardInterrupt,SystemExit):
            print("")
            print("hasta la vista ")
            atmega.close()
    else:
        try:
            atmega.write(command.encode())
            atmega.write('\r'.encode())
            atmega.flushInput()
            #print ("enviado")
            sleep(3)
            try:
                #print ("recibiendo datos: ")
                while not( atmega.in_waiting > 0):
                    #print ("datos recibidos")
                    sleep (1.5)
                    pass
                #print ()
                mens = atmega.readline().strip()
                telegram_bot.sendMessage(chat_id, str(mens.decode()))
                #print (mens.decode())
            except:
                print("no data recive")
        except(KeyboardInterrupt,SystemExit):
            print("")
            print("hasta la vista ")
            atmega.close()

telegram_bot = telepot.Bot('5493887556:AAEJue3IwpUpoQ_fWH-oUPWnOI9icTM0-rY')
print (telegram_bot.getMe())

MessageLoop(telegram_bot, action).run_as_thread()
print 'Up and Running....'

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

while 1:
    try:
        atmega.flushInput()
        sleep(3)
        try:
            while not( atmega.in_waiting > 0):
                sleep (1.5)
                pass
            mens = atmega.readline().decode().strip()
        except:
            print("no data recive")
    except(KeyboardInterrupt,SystemExit):
        print("")
        print("hasta la vista ")
        atmega.close()
    
    if (mens == "SE DECTETO MOVIMIENTO"):
        Enviar_correo()

    time.sleep(10)