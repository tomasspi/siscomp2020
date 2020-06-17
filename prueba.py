import time
import sys
import os

def hola():
	time.sleep(2)
	print("CHAU ME FUI")
	sys.exit()

def chau():
	while True:
		time.sleep(2)
		print("termine")

while True:
	pid = str(os.getpid())
	print (pid)
	time.sleep(2)
	print("funciono")
	time.sleep(2)
	print("no funciono")