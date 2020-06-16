# https://www.freecodecamp.org/news/how-to-make-your-own-python-dev-server-with-raspberry-pi-37651156379f/

from flask import Flask, render_template

server = Flask(__name__)

@server.route('/')
def index():
	lista = ['/logs -> muestra logs del sistema', '/activar -> activar sistema', '/desactivar -> desactivar sistema' ]
	return render_template('index.html', my_list = lista)

@server.route('/logs')
def logs():
	f = open("log.log")
	log = f.read()
	print (log)
	f.close()

if __name__ == '__main__':
	server.run(debug = True, host = '0.0.0.0')
