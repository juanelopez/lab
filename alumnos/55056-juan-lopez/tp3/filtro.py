#!/usr/bin/env python3
import os
import multiprocessing
import time
import sys
import threading
import queue
import colores
import getopt
import socketserver
def lector_encabezado(lista):
    encabezado = []
    formato = lista[0]
    if(formato != b'P6'):
        print("Numero magico incorrecto")
        print("Se esperaba como numero magico P6 pero se recibio ", formato)
        sys.exit(4)
    encabezado.append(formato)
    encabezado.append(b'\n')
    lista.pop(0)
    comentario = []
    for i in range(0, len(lista)):
        if(lista[0][0] == 35):  # 35 es # en ascii
            comentario.append(lista[i])
            encabezado.append(lista[i])
            encabezado.append(b'\n')
            lista.pop(0)
        if(lista[i] == b'255'):  # revisar
            break
    size = (lista[0]).split(b' ')
    encabezado.append(size[0])
    encabezado.append(b' ')
    encabezado.append(size[1])
    encabezado.append(b'\n')
    lista.pop(0)
    cant_colores = lista[0]
    encabezado.append(cant_colores)
    encabezado.append(b'\n')
    lista.pop(0)
    return encabezado


def escritor_encabezado(encabezado, q1):  # Envia el encabezado para escribirlo
    q1.put(encabezado)
    enviado = "enviado"
    return enviado


def image_data(lista, q1):  # envia los datos de la imagen para escribirlo
    q1.put("enviando")
    q1.put(lista)

def terminar(q1):  # Termina todo al completar la escritura
    q1.put('DONE')
    return "DONE"


def usage():  # Muestra el mensaje de ayuda para ver las opciones
    fdh = os.open("help", os.O_RDONLY)
    help = os.read(fdh, 1024)
    os.write(1, help)
    os.close(fdh)


def filtrado(color,intensidad,cantidad_lectura,archivo,self):

    #archivo = "dog.ppm"
    #cantidad_lectura=1024
    try:
        fd = os.open(archivo, os.O_RDONLY)
    except:
        print("El archivo no existe")
        sys.exit(2)
    extension = os.path.splitext(archivo)
    if(extension[1] != ".ppm"):
        print("Formato del archivo incorrecto")
        print("Se esperaba una archivo del formato archivo.ppm (portable pixmap) pero se recibio el archivo: ", archivo)
        sys.exit(3)
    leido = os.read(fd, cantidad_lectura)
    lista = leido.split(b'\n')# Pasa a una lista el encabezado y parte de la image data
    encabezado = lector_encabezado(lista)# Llama a la funcion que lee el encabezado del ppm

    temp = b''
    for enc in encabezado:
        temp = temp+enc
    long_enc = len(temp)
    temp = leido[long_enc:] #retira el encabezado de lo leido dejando solo la image data
    o = []
    while temp:
        o.append(temp[:1])
        temp = temp[1:]
    if(color == "R"):
        q1 = queue.Queue()  # Crea la primera cola de mensajes
        p1 = threading.Thread(
        target=colores.rojo, args=(q1, intensidad, archivo,self))
        p1.start()
        escritor_encabezado(encabezado, q1)
        image_data(o, q1)
    elif(color == "G"):
        q2 = queue.Queue()
        p2 = threading.Thread(
        target=colores.verde, args=(q2, intensidad, archivo,self))
        p2.start()
        escritor_encabezado(encabezado, q2)
        image_data(o, q2)
    elif(color == "B"):
        q3 = queue.Queue()
        p3 = threading.Thread(
        target=colores.azul, args=(q3, intensidad, archivo,self))
        p3.start()
        escritor_encabezado(encabezado, q3)
        image_data(o, q3)
    elif(color == "W"):
        q4 = queue.Queue()
        p4 = threading.Thread(
        target=colores.blanco_negro, args=(q4, intensidad, archivo,self))
        p4.start()
        escritor_encabezado(encabezado, q4)
        image_data(o, q4)

    leer = os.read(fd, cantidad_lectura)  # Lee nuevamente la imagen
    lectura = b''
    while (leer != b''):  # Lee sucesivamente lo que queda de la imagen
        o = []
        lectura = leer
        while lectura:
            o.append(lectura[:1])  # Crea la lista con lo leido anteriormente
            lectura = lectura[1:]
        if(color == "R"):
            image_data(o, q1)
        elif(color == "G"):
            image_data(o, q2)
        elif(color == "B"):
            image_data(o, q3)
        elif(color == "W"):
            image_data(o, q4)
        leer = os.read(fd, cantidad_lectura)
    os.close(fd)
    if(color == "R"):
        impri1 = terminar(q1)
        p1.join()
    elif(color =="G"):
        impri2 = terminar(q2)
        p2.join()
    elif(color == "B"):
        impri3 = terminar(q3)
        p3.join()
    elif(color == "W"):
        impri4 = terminar(q4)
        p4.join()
    
    
    if(impri1 == "DONE" or impri2 == "DONE" or impri3 == "DONE" or impri4 == "DONE"):
        print("Filtro generado")        

