import requests
import re
import json
import random

datos = []
objetos = []
usuarios = ['usuario1', 'usuario2', 'usuario3', 'usuario4', 'usuario5', 'usuario6', 'usuario7', 'usuario8', 'usuario09', 'usuario10']

def leerArchivo():
    global datos, objetos
    print('Ingrese ruta del archivo: ')
    ruta = input()
    archivo = open(ruta, "r")
    datos = re.findall('[^.?!]+[.?!]+', archivo.read())
    archivo.close()
    for oracion in datos:
        objetos.append(json.dumps({"autor": random.choice(usuarios), "nota": oracion}))

def verDatos():
    global objetos
    contador = 1
    for oracion in objetos:
        oracionPrint = oracion.replace('\n', '\\n')
        print(str(contador) + '. ' + oracionPrint)
        contador = contador + 1

def enviarDatos(direccion):
    for oracion in datos:
        data = {
            "database": "baseSopes",
            "collection": "oracion",
            "Document": {
            "autor": random.choice(usuarios),
            "nota": oracion
          }
        }
        print(data)
        requests.post(direccion, json = data)


def menu():
    print('_______MENU_______ \n1. Leer archivo \n2. Ver datos \n3. Enviar datos \n4. Salir \n')
    opcion = input()

    if opcion == '1':
        print('_______LEER ARCHIVO_______')
        leerArchivo()
        print('\n')
        menu()
    elif opcion == '2':
        print('_______VER DATOS_______\n')
        verDatos()
        print('_______________________\n')
        menu()
    elif opcion == '3':
        print('_______ENVIAR DATOS_______\n')
        print('Ingrese direccion para realizar las peticiones:')
        direccion = input()
        enviarDatos(direccion)
        input()
        menu()
    elif opcion == '4':
        exit()
    else:
        print('Opcion invalida\n')
        input()
        menu()


menu()