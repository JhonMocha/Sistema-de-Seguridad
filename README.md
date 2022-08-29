# Sistema-de-Seguridad

LOS ARCHIVOS PIR.py, Stemperatura.py son para probar los sensores en la raspberry

El archivo main.cpp es el código para arduino

El archivo rasby.py, es el código en general, para hacer funcionar todos los sensores

El archivo Security System Esquemático.pdf es el esquemático del proyecto


PASOS

CAMARA

PASO1
Rasbian actualizado con la ultima versión de todos los paquetes 
sudo apt update
sudo apt upgrade

PASO2
Habilitar SSH para permitir el acceso remoto para las primeras pruebas
sudo service ssh start

PASO3
Instalar camara 
sudo shutdown -h

PASO4
Conectar Cámara

PASO5
Habilitar camara
sudo raspi-config

Ve a <<Opciones de interfaz>> > <<Cámara>>. <<¿Desea que la interfaz de la cámara
esté habilitada?>>Si.

Sal de raspi-config y acepta el reinicio


INSTALAR Librerias de cámaras de Pyton
sudo apt install python-picamera
¡Listo!
