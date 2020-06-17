from django.shortcuts import render
import requests
import sys
import subprocess as sb

def button(request):
    with open('static/log.txt', 'r') as f:
        lineas = f.read().splitlines()
        ultimas_linea = lineas[-1]
    return render(request, 'index.html', {'contenido': ultimas_linea})


def activado(request):
    sb.call(['python', '/home/facubos/Documentos/siscomp2020/Servidor_Website/activar.py'])
    data = 'Sistema de Seguridad ACTIVADO'
    print(data)
    return render(request, 'index.html', {'data':data})

def desactivado(request):
    sb.call(['python', '/home/facubos/Documentos/siscomp2020/Servidor_Website/desactivar.py'])
    data = 'Sistema de Seguridad DESACTIVADO'
    print(data)
    return render(request, 'index.html', {'data':data})

def ver_log(request):
    f = open('/home/facubos/Documentos/siscomp2020/security_log.log', 'r')
    contenido = f.read()
    f.close()
    return render(request, 'index.html', {'contenido': contenido})
