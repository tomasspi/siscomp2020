from datetime import datetime   #Para timestamp
import RPi.GPIO as GPIO         #Para manejar GPIO
import time                     #Para anti-rebote
import os                       #Para llamas al sistema

pin_sensor = 12          #Pin del sensor de la puerta
sistema_activado = 1     #Bandera para activar/desactivar el sistema
accion = ""              #Acción realizada
log = "security_log.log" #Path del log (mismo directorio que este archivo)

def get_timestamp():
    """ Obtiene el timestamp con formato DD-MM-YYYY HH:MM:SS
    """
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
    return timestamp

def escribir_logs(timestamp, accion):
    """Escribe los logs: uno no encriptado y otro encriptado.

    Keyword arguments:
    timestamp -- Timestamp de la acción
    accion    -- Acción realizada
    """
    #Crea el mensaje del log
    msg = "%s | %s\n\r" % (timestamp, accion)
    #print(msg)

    #Genera y ejecuta el comando para escribir el log
    cmd = 'echo "%s" >> %s' % (msg, log)
    os.system(cmd)

    #Genera el comando para encriptar el log utilizando el módulo realizado
    cmd = "./userspace w %s" % (msg)
    os.system(cmd)
    cmd = "./userspace r >> encrypted_log.log"
    os.system(cmd)

def sensor_handler(pin):
    """Handler de la interrupción del pin 12. Genera el timestamp con la acción
    realizada.

    Keyword arguments:
    pin -- pin leído (12)
    """
    if sistema_activado == 1:
        time.sleep(1)   #Anti-rebote

        timestamp = get_timestamp()
        accion = "Caja de seguridad ABIERTA"

        escribir_logs(timestamp, accion)


def activar_sistema(pin):
    """Handler de la interrupción del pin 11. Activa el sistema de seguridad
    y genera el timestamp con la acción realizada.

    Keyword arguments:
    pin -- pin leído (11)
    """
    time.sleep(1)           #Anti-rebote
    sistema_activado = 1    #Activa el sistema

    GPIO.add_event_detect(pin_sensor, GPIO.BOTH)        #Detecta ambos flancos
    GPIO.add_event_callback(pin_sensor, sensor_handler) #Asigna el handler

    accion = "Sistema de seguridad ACTIVADO"
    timestamp = get_timestamp()

    escribir_logs(timestamp, accion)


def desactivar_sistema(pin):
    """Handler de la interrupción del pin 13. Desactiva el sistema de seguridad
    y genera el timestamp con la acción realizada.

    Keyword arguments:
    pin -- pin leído (13)
    """
    time.sleep(1)
    sistema_activado = 0
    GPIO.remove_event_detect(pin_sensor) #Desactiva la detección de interrupciones

    accion = "Sistema de seguridad DESACTIVADO"
    timestamp = get_timestamp()

    escribir_logs(timestamp, accion)


#------

GPIO.setmode(GPIO.BOARD)    #Habilita el módulo GPIO de la Raspberry

#Configura pines 11, 12 y 13 como entrada
GPIO.setup(11, GPIO.IN)
GPIO.setup(12, GPIO.IN)
GPIO.setup(13, GPIO.IN)

GPIO.add_event_detect(11, GPIO.FALLING)         #Detecta por flanco de bajada
GPIO.add_event_callback(11, activar_sistema)    #Asigna el handler del pin 11

GPIO.add_event_detect(13, GPIO.FALLING)         #Detecta por flanco de bajada
GPIO.add_event_callback(13, desactivar_sistema) #Asigna el handler del pin 13

#Bucle para esperar interrupciones
while True:
    time.sleep(1)
    print("Esperando...")

GPIO.cleanup()  #Pone los pin utilizados a la Configuración default
