from picamera import PiCamera
from time import sleep

camara = PiCamera()
camara.start_preview()
sleep(5)
camara.capture("Direccion donde se quiere guardar la imagen")
camara.stop_preview()