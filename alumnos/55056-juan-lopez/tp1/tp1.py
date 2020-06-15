#!/usr/bin/env python3
import os
import multiprocessing
import time
import sys
import getopt

#start = time.perf_counter()


def rojo(q1, inten, archivo):
    archivo_rojo = "r_"+archivo
    fd1 = os.open(archivo_rojo, os.O_RDWR | os.O_CREAT)
    red = []
    j = 1
    r = 0
    nada = b'\x00'
    while True:
        msg = q1.get()
        if(msg[0] == b'P6'):
            for enc in msg:  # Escribe el encabezado
                os.write(fd1, enc)
        elif(msg == "enviando"):
            recibido = q1.get()
            for p in recibido:
                if(j-(3*r) == 1):
                    # Modifica la intensidad del byte
                    a_bytes = intensidad(p, inten)
                    os.write(fd1, a_bytes)  # Escribe en el archivo
                    os.write(fd1, nada)
                    os.write(fd1, nada)
                    r = r+1
                j = j+1

        if(msg == 'DONE'):
            os.close(fd1)
            print(msg)
            break


def verde(q2, inten, archivo):
    archivo_green = "g_"+archivo
    fd1 = os.open(archivo_green, os.O_RDWR | os.O_CREAT)
    red = []
    j = 1
    g = 0
    nada = b'\x00'
    while True:
        msg = q2.get()
        if(msg[0] == b'P6'):
            for enc in msg:  # Escribe el encabezado
                os.write(fd1, enc)
        elif(msg == "enviando"):
            recibido = q2.get()
            for p in recibido:
                if(j-(3*g) == 2):
                    a_bytes = intensidad(p, inten)
                    os.write(fd1, nada)
                    os.write(fd1, a_bytes)
                    os.write(fd1, nada)
                    g = g+1
                j = j+1

        if(msg == 'DONE'):
            os.close(fd1)
            print(msg)
            break


def azul(q3, inten, archivo):
    archivo_blue = "b_"+archivo
    fd1 = os.open(archivo_blue, os.O_RDWR | os.O_CREAT)
    red = []
    j = 1
    b = 0
    nada = b'\x00'
    while True:
        msg = q3.get()
        if(msg[0] == b'P6'):
            for enc in msg:  # Escribe el encabezado
                os.write(fd1, enc)
        elif(msg == "enviando"):
            recibido = q3.get()
            for p in recibido:
                if(j-(3*b) == 3):
                    a_bytes = intensidad(p, inten)
                    os.write(fd1, nada)
                    os.write(fd1, nada)
                    os.write(fd1, a_bytes)
                    b = b+1
                j = j+1

        if(msg == 'DONE'):
            os.close(fd1)
            print(msg)
            break


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


def intensidad(p, intensidad):  # Funcion que varia la intensidad
    a = int.from_bytes(p, byteorder='big')  # convierte los bytes en int    
    # Multiplica la intensidad por el byte pasado a int
    a_intensidad = a*intensidad 
    # Convierte a int en caso que la division quedara en float
    a_convertible = int(a_intensidad) 
    # Verifica si se excede el maximo color entonces se ajusta como 255 el cual es la maxima intesidad
    if(a_convertible > 255):  
        a_convertible = 255
    a_bytes = a_convertible.to_bytes((a_convertible.bit_length(
    ) + 7) // 8, 'big') or b'\0'  # Vuelve a convertir a bytes
    return a_bytes


def terminar(q1):  # Termina todo al completar la escritura
    q1.put('DONE')
    return "DONE"


def usage():  # Muestra el mensaje de ayuda para ver las opciones
    fdh = os.open("help", os.O_RDONLY)
    help = os.read(fdh, 1024)
    os.write(1, help)
    os.close(fdh)


if __name__ == "__main__":
    intensidad_red = 1
    intensidad_green = 1
    intensidad_blue = 1
    #archivo = "dog.ppm"
    #cantidad_lectura=1024
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:f:r:g:b:", [
                                   "help", "size", "file", "red", "green", "blue"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-s", "--size"):
            cantidad_lectura = int(arg)
        elif opt in ("-f", "--file"):
            archivo = arg
        elif opt in ("-r", "--red"):
            intensidad_red = float(arg)
        elif opt in ("-g", "--green"):
            intensidad_green = float(arg)
        elif opt in ("-b", "--azul"):
            intensidad_blue = float(arg)
        else:
            assert False, "unhandled option"
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
    q1 = multiprocessing.Queue()  # Crea la primera cola de mensajes
    q2 = multiprocessing.Queue()
    q3 = multiprocessing.Queue()
    p1 = multiprocessing.Process(
        target=rojo, args=(q1, intensidad_red, archivo))
    p2 = multiprocessing.Process(
        target=verde, args=(q2, intensidad_green, archivo))
    p3 = multiprocessing.Process(
        target=azul, args=(q3, intensidad_blue, archivo))
    p1.start()
    p2.start()
    p3.start()
    # escribe el encabezado en los 3 archivos
    escritor_encabezado(encabezado, q1)
    escritor_encabezado(encabezado, q2)
    escritor_encabezado(encabezado, q3)
    # Escribe la primera parte de los datos de la imagen(lo que esta a continuacion del encabezado)
    image_data(o, q1)
    image_data(o, q2)
    image_data(o, q3)
    leer = os.read(fd, cantidad_lectura)  # Lee nuevamente la imagen
    lectura = b''
    while (leer != b''):  # Lee sucesivamente lo que queda de la imagen
        o = []
        lectura = leer
        while lectura:
            o.append(lectura[:1])  # Crea la lista con lo leido anteriormente
            lectura = lectura[1:]
        image_data(o, q1)
        image_data(o, q2)
        image_data(o, q3)
        leer = os.read(fd, cantidad_lectura)
    os.close(fd)
    impri1 = terminar(q1)
    impri2 = terminar(q2)
    impri3 = terminar(q3)
    p1.join()
    p2.join()
    p3.join()

    if(impri1 == "DONE" and impri2 == "DONE" and impri3 == "DONE"):
        print("Se generaron los 3 filtros")
        os.system("ls *ppm")
    #finish = time.perf_counter()
    #tt = round(finish-start,3)
    #print ("tiempo total = ",tt)
