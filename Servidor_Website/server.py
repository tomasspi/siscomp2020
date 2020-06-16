# https://www.freecodecamp.org/news/how-to-make-your-own-python-dev-server-with-raspberry-pi-37651156379f/

from flask import Flask, render_template
import os.path as rp
import json

server = Flask(__name__)

@server.route('/')
def index():
	lista = ['/logs -> muestra logs del sistema', '/activar -> activar sistema', '/desactivar -> desactivar sistema' ]
	return render_template('index.html', my_list = lista)

current = rp.abspath(rp.dirname(__file__))
log_path = rp.join(current, "../security_log.log")

@server.route('/logs')
def logs():
	f = open(log_path)
	log = f.read()
	f.close()
	return render_template('print.html', log = log)

if __name__ == '__main__':
	server.run(debug = True, host = '0.0.0.0')
