import time
import RPi.GPIO as GPIO
from datetime import datetime
import os

flag = 1
accion = ""

def button_handler(pin):
	if flag == 1:
		time.sleep(1)
			
		status = GPIO.input(pin)
			
		accion = "Caja de seguridad ABIERTA"

		now = datetime.now()
		timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
		msg = "%s | %s\n\r" % (timestamp, accion)
		cmd = "./userspace w %s" % (msg)
		os.system(cmd)
		save = "./userspace r >> encripted_log.log"
		os.system(save)
		log.write(msg)

def desactivar_sistema(pin):
	flag = 0
	GPIO.remove_event_detect(pin_sensor)
	time.sleep(1)
	accion = "Se DESACTIVO el sistema de seguridad"
	now = datetime.now()
	timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
	msg = "%s | %s\n\r" % (timestamp, accion)
	log.write(msg)
	print("Se desactivo el sistema de seguridad")
	return

def activar_sistema(pin):
	flag = 1
	GPIO.add_event_detect(pin_sensor, GPIO.BOTH)
	GPIO.add_event_callback(pin_sensor, button_handler)
	time.sleep(1)
	accion = "Se ACTIVO el sistema de seguridad"
	now = datetime.now()
	timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
	msg = "%s | %s\n\r" % (timestamp, accion)
	log.write(msg)
	print("Se activo el sistema de seguridad")
	return

def activar():
	flag = 1
	print("Activado celular")
	accion = "Se ACTIVO el sistema de seguridad desde el celular"
	now = datetime.now()
	timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
	msg = "%s | %s\n\r" % (timestamp, accion)
	log.write(msg)
    return

def desactivar():
	flag = 0
	print("Desacivado celular")
	accion = "Se DESACTIVO el sistema de seguridad desde el celular"
	now = datetime.now()
	timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
	msg = "%s | %s\n\r" % (timestamp, accion)
	log.write(msg)
    return

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN)
GPIO.setup(11, GPIO.IN)
GPIO.setup(13, GPIO.IN)

GPIO.add_event_detect(11, GPIO.FALLING)
GPIO.add_event_callback(11, activar_sistema)

GPIO.add_event_detect(13, GPIO.FALLING)
GPIO.add_event_callback(13, desactivar_sistema)

log = open("security_log.log", "a")

pin_sensor = 12

while True:
	time.sleep(1)

GPIO.cleanup()


# para correr funciones desde shell ver esto: 
# https://www.it-swarm.dev/es/python/ejecutar-la-funcion-desde-la-linea-de-comando./970735373/
# https://www.it-swarm.dev/es/python/llamar-una-funcion-python-desde-un-script-de-shell/941240966/
