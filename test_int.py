import time
import RPi.GPIO as GPIO
from datetime import datetime

flag = 1

def button_handler(pin):
	time.sleep(1)                    
	status = GPIO.input(pin)         
	print("state", status)           
	now = datetime.now()                  
	timestamp = now.strftime("%d/%m/%Y %H:%M:%S")   
	msg = "%s | %s\n\r" % (timestamp, status)      
	log.write(msg)                                

def sistema(pin):
	if (flag == 0):
		desactivar_sistema(12)
	else:
		activar_sistema(12)

def desactivar_sistema (pin):
	flag = 1
	GPIO.remove_event_detect(pin, GPIO.BOTH)     	
	time.sleep(1)                    
	status = GPIO.input(pin)         #Ver esto si le ponemos el estado o directo lo sacamos y ponemos un print en el log de que se 
	print("state", status)           #desactivo y mostramos el timestamp
	now = datetime.now()                  
	timestamp = now.strftime("%d/%m/%Y %H:%M:%S")   
	msg = "%s | %s\n\r" % (timestamp, status)      
	log.write(msg)  
	print("Se desactivo el sistema de seguridad")
	return

def activar_sistema (pin):
	flag = 0
	GPIO.add_event_detect(pin, GPIO.BOTH)
	GPIO.add_event_callback(pin, button_handler)     	
	time.sleep(1)                    
	status = GPIO.input(pin)         #Ver esto si le ponemos el estado o directo lo sacamos y ponemos un print en el log de que se 
	print("state", status)           #activo y mostramos el timestamp
	now = datetime.now()                  
	timestamp = now.strftime("%d/%m/%Y %H:%M:%S")   
	msg = "%s | %s\n\r" % (timestamp, status)      
	log.write(msg)  
	print("Se activo el sistema de seguridad")
	return


GPIO.setmode(GPIO.BOARD)            
GPIO.setup(12, GPIO.IN)
GPIO.setmode(GPIO.BOARD)      #Este boton activa y desactiva localmente      
GPIO.setup(11, GPIO.IN)               
# GPIO.add_event_detect(12, GPIO.FALLING)     
# GPIO.add_event_callback(12, button_handler)

GPIO.add_event_detect(11, GPIO.BOTH)     
GPIO.add_event_callback(11,sistema)

log = open("security_log.log", "a")                   

while True:    
	print("One")           
	time.sleep(1)        
	print("Two")         
	time.sleep(1)       

GPIO.cleanup() 


# para correr funciones desde shell ver esto: 
# https://www.it-swarm.dev/es/python/ejecutar-la-funcion-desde-la-linea-de-comando./970735373/
# https://www.it-swarm.dev/es/python/llamar-una-funcion-python-desde-un-script-de-shell/941240966/
