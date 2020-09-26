import os
import multiprocessing
import time
import sys
import threading
import queue
import socketserver

def rojo(q1, inten, archivo,self):
    j = 1
    r = 0
    nada = b'\x00'
    para_escribir = b''
    while True:
        msg = q1.get()
        if(msg[0] == b'P6'):
            for enc in msg:  # Escribe el encabezado
                self.request.sendall(enc)
        elif(msg == "enviando"):
            recibido = q1.get()
            for p in recibido:
                if(j-(3*r) == 1):
                    # Modifica la intensidad del byte
                    a_bytes = intensidad(p, inten) #falla en intensidad
                    para_escribir = para_escribir+a_bytes+nada+nada 
                    r = r+1    
                j = j+1
            self.request.sendall(para_escribir)
            para_escribir = b''
            
        if(msg == 'DONE'):
            #os.close(fd1)
            print(msg)
            break


def verde(q2, inten, archivo,self):
    j = 1
    g = 0
    nada = b'\x00'
    para_escribir = b''
    while True:
        msg = q2.get()
        if(msg[0] == b'P6'):
            for enc in msg:  # Escribe el encabezado
                self.request.sendall(enc)
        elif(msg == "enviando"):
            recibido = q2.get()
            for p in recibido:
                if(j-(3*g) == 2):
                    a_bytes = intensidad(p, inten)
                    para_escribir = para_escribir+nada+a_bytes+nada 
                    g = g+1
                j = j+1
            self.request.sendall(para_escribir)
            para_escribir = b''
        if(msg == 'DONE'):
            print(msg)
            break


def azul(q3, inten, archivo,self):
    j = 1
    b = 0
    nada = b'\x00'
    para_escribir = b''
    while True:
        msg = q3.get()
        if(msg[0] == b'P6'):
            for enc in msg:  # Escribe el encabezado
                self.request.sendall(enc)
        elif(msg == "enviando"):
            recibido = q3.get()
            for p in recibido:
                if(j-(3*b) == 3):
                    a_bytes = intensidad(p, inten)
                    para_escribir = para_escribir+nada+nada+a_bytes
                    b = b+1
                j = j+1
            self.request.sendall(para_escribir)
            para_escribir = b''
            
        if(msg == 'DONE'):
            #os.close(fd1)
            print(msg)
            break

def blanco_negro(q4,inten,archivo,self):
    j = 0
    b = 0
    nada = b'\x00'
    para_escribir = b''
    lista_bw = []
    bw = 0
    while True:
        msg = q4.get()
        if(msg[0] == b'P6'):
            for enc in msg:  # Escribe el encabezado
                self.request.sendall(enc)
        elif(msg == "enviando"):
            recibido = q4.get()
            for p in recibido:
                lista_bw.append(p)
                bw = bw+1
                if (bw == 3):
                    devuelto = intensidad_bw(lista_bw,inten)
                    para_escribir = para_escribir + devuelto + devuelto + devuelto
                    lista_bw = []
                    bw = 0
                j = j+1
            self.request.sendall(para_escribir)
            para_escribir = b''
            
        if(msg == 'DONE'):
            #os.close(fd1)
            print(msg)
            break
def intensidad(p, intensidad):  # Funcion que varia la intensidad
    
    a = int.from_bytes(p, byteorder='big')  # convierte los bytes en int    
    # Multiplica la intensidad por el byte pasado a int
    a_intensidad = a*float(intensidad) 
    # Convierte a int en caso que la division quedara en float
    a_convertible = int(a_intensidad) 
    # Verifica si se excede el maximo color entonces se ajusta como 255 el cual es la maxima intesidad
    if(a_convertible > 255):  
        a_convertible = 255
    a_bytes = a_convertible.to_bytes((a_convertible.bit_length(
    ) + 7) // 8, 'big') or b'\0'  # Vuelve a convertir a bytes
    intensidad = 0
    return a_bytes
def intensidad_bw(p,intensidad):
    salida = 0
    for blanco_negro in p:
        a = int.from_bytes(blanco_negro, byteorder='big')
        a_intensidad = a*float(intensidad)
        # Convierte a int en caso que la division quedara en float
        a_convertible = int(a_intensidad) 
        # Verifica si se excede el maximo color entonces se ajusta como 255 el cual es la maxima intesidad
        if(a_convertible > 255):  
            a_convertible = 255
        salida = salida + a_convertible
    salida = salida/3
    salida = round(salida)
    a_bytes = salida.to_bytes((salida.bit_length(
    ) + 7) // 8, 'big') or b'\0'  # Vuelve a convertir a bytes
    return a_bytes