def lector_encabezado(lista,offset,interleave,tamano_mensaje):
    encabezado = []
    formato = lista[0]
    if(formato != b'P6'):
        print("Numero magico incorrecto")
        print("Se esperaba como numero magico P6 pero se recibio ", formato)
        sys.exit(4)
    encabezado.append(formato)
    encabezado.append(b'\n')
    lista.pop(0)
    instruccion = "#UMCOMPU2"+" "+str(offset)+" "+str(interleave)+" "+str(tamano_mensaje)
    encabezado.append(bytes(instruccion,'utf-8'))
    encabezado.append(b'\n')
    for i in range(0, len(lista)):
        if(lista[0][0] == 35):  # 35 es # en ascii
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
    imagen_tamano = int(size[0])*int(size[1])*3
    lista.pop(0)
    cant_colores = lista[0]
    encabezado.append(cant_colores)
    encabezado.append(b'\n')
    lista.pop(0)
    return encabezado ,imagen_tamano