import encabezado
import os
import globales as glo
import escritor
import modificador
import threading
from concurrent import futures
import time
import argparse
import time
import sys
start = time.perf_counter()

if __name__ == "__main__":
    
    hilos = futures.ThreadPoolExecutor(max_workers=3)

    #-----------Manejo de argumentos-------------------
    parser = argparse.ArgumentParser(description='Tp2 - procesa ppm')
    parser.add_argument('-s', '--size',action="store", type= int, default=1024, help="Bloque de lectura")
    parser.add_argument('-f', '--file',action="store", dest="file_portador", required=True, type=str, help="Archivo portador")
    parser.add_argument('-m', '--message',action="store", dest="file_mensaje", required=True, type=str, help="Mensaje estenografico")
    parser.add_argument('-e', '--offset',action="store", type= int, default = 0 ,help="Offset en pixeles del inicio del raster")
    parser.add_argument('-i', '--interleave',action="store", type= int, default = 1 ,help="Interleave de modificacion de pixel")
    parser.add_argument('-o', '--output',action="store", dest="file_salida", required=True, type=str, help="Estego-mensaje(archivo de salida)")
    args = parser.parse_args()
    
    cantidad_lectura = args.size
    interleave = args.interleave
    offset = args.offset
    try:
        fd_mensaje = os.open(args.file_mensaje,os.O_RDONLY)
    except:
        print("El archivo no existe")
        sys.exit(1)
    tamano_para_leer = os.stat(args.file_mensaje).st_size
    palabra_bytes = os.read(fd_mensaje,tamano_para_leer) 
    os.close(fd_mensaje)
    palabra = str(palabra_bytes,'utf-8')
    tamano_mensaje = len(palabra)
    total_texto = tamano_mensaje *8 + interleave*3 + 3*offset
    #----------Fin manejo argumentos------------------
    #----------------Manejo encabezado----------------
    try:   
        fd = os.open(args.file_portador, os.O_RDONLY)
    except:
        print("El archivo no existe")
        sys.exit(2)
    extension = os.path.splitext(args.file_portador)
    if(extension[1] != ".ppm"):
        print("Formato del archivo incorrecto")
        print("Se esperaba una archivo del formato archivo.ppm (portable pixmap) pero se recibio el archivo: ", archivo)
        sys.exit(3)
    leido = os.read(fd, cantidad_lectura)
    lista = leido.split(b'\n')# Pasa a una lista el encabezado y parte de la image data
    encabezado,imagen_tamano = encabezado.lector_encabezado(lista,offset,interleave,tamano_mensaje) # NO OLVIDAR DE CAMBIAR
    print("tamano imagen",imagen_tamano)
    print("TOTAL TEXTO",total_texto , "imagen",imagen_tamano)
    if(imagen_tamano < total_texto):
        print("El interleave",interleave,"combinado con una tamano de texto ",total_texto,"y un offset de ",offset,"no se pueden escribir en el archivo")
        sys.exit(4)
    fd1 = os.open(args.file_salida, os.O_RDWR | os.O_CREAT)
    salida_encabezado = b''
    if(encabezado[0] == b'P6'):
        for enc in encabezado:  # Escribe el encabezado
            salida_encabezado = salida_encabezado + enc
    os.write(fd1,salida_encabezado)
    instruccion = "#UMCOMPU2"+" "+str(offset)+" "+str(interleave)+" "+str(tamano_mensaje)
    #----------------Fin manejo encabezado-------------
    temp = b''
    for enc in encabezado:
        temp = temp+enc
    long_enc = len(temp)-len(instruccion)-1
    print("LONGITUD ENCABEZADO",long_enc+len(instruccion)+1)
    temp = leido[long_enc:] #retira el encabezado de lo leido dejando solo la image data
    o = []
    while temp:
        o.append(temp[:1])
        temp = temp[1:]
    glo.buffer = o#guardo el archivo en variable global
    #-----tratamiento de frase-----------
    palabra_lista=[]
    palabra_lista = modificador.desarmador(palabra)
    glo.global_palabra= palabra_lista
    longitud_palabra= len(palabra_lista)
    print("longitud palabra",longitud_palabra/8)
    #----fin tratamiento de frase--------
    modificador.guiador(offset,interleave,longitud_palabra) #guia las escrituras
    donde_termino_rojo = 0
    donde_termino_verde = 0
    donde_termino_azul = 0
    r=0
    g=1
    b=2
    hilo_futuro_r = hilos.submit(escritor.red,interleave , offset,donde_termino_rojo,r)
    hilo_futuro_g = hilos.submit(escritor.green,interleave , offset,donde_termino_verde,g)
    hilo_futuro_b = hilos.submit(escritor.blue,interleave , offset,donde_termino_verde,b)
    
    donde_termino_rojo,r = hilo_futuro_r.result()
    donde_termino_verde,g = hilo_futuro_g.result()
    donde_termino_azul,b = hilo_futuro_b.result()
    salida_archivo = b''
    glo.candado.acquire()
    o = glo.buffer    
    glo.candado.release()
    for escribir_archivo in o:  # Escribe el encabezado
        salida_archivo = salida_archivo + escribir_archivo
    escritor_para_test=os.write(fd1,salida_archivo)

    leer = os.read(fd, cantidad_lectura) 
    lectura = b''
    
    while (leer != b''):  # Lee sucesivamente lo que queda de la imagen
        o = []
        salida_archivo = b''
        lectura = leer
        while lectura:
            o.append(lectura[:1])  # Crea la lista con lo leido anteriormente
            lectura = lectura[1:]
        glo.candado.acquire()
        glo.buffer = o    
        glo.candado.release()
        
        if( (g > 0 and  g < len(glo.global_palabra )-1) or (r > 0 and  r < len(glo.global_palabra )-1)):
            if (donde_termino_verde < glo.guia_verde[-1]):
                hilo_futuro_r = hilos.submit(escritor.red,interleave , offset,donde_termino_rojo,r)
                hilo_futuro_g = hilos.submit(escritor.green,interleave , offset,donde_termino_verde,g)
                hilo_futuro_b = hilos.submit(escritor.blue,interleave , offset,donde_termino_verde,b)
            donde_termino_rojo,r = hilo_futuro_r.result()
            donde_termino_verde,g = hilo_futuro_g.result()
            donde_termino_azul,b = hilo_futuro_b.result()
        glo.candado.acquire()
        o = glo.buffer    
        glo.candado.release()
        for escribir_archivo in o:  # Escribe el encabezado
            salida_archivo = salida_archivo + escribir_archivo
        escritor_para_test=os.write(fd1,salida_archivo) 
        leer = os.read(fd, cantidad_lectura)
    os.close(fd)
    os.close(fd1)
finish = time.perf_counter()
tt = round(finish-start,3)
print ("tiempo total = ",tt)