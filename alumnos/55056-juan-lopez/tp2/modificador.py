import globales as glo

def modificador(bytes_entrada,ocultar,color):
    a = int.from_bytes(bytes_entrada, byteorder='big')
    a_binario=bin(a)
    longitud = len(a_binario)-1
    bitmenos=a_binario[longitud]
    if(bitmenos == '1'):
        if(ocultar == 0):
            a = a - 1
    elif(bitmenos == '0'):
        if (ocultar == 1):
            a= a + 1
    a_bytes = a.to_bytes((a.bit_length(
    ) + 7) // 8, 'big') or b'\0'
    return a_bytes

def desarmador(palabra):
    lista =[]
    lista_final =[]
    count=0
    for a in palabra:
        convertido=ord(a)
        binario_convertido=bin(convertido)
        longitud = len(binario_convertido) - 1
        lista=list(map(str, binario_convertido))
        lista.pop(0)
        lista.pop(0)
        while(len(lista)< 8 ):
            lista.insert(0,'0')
        for elemento in lista:
            lista_final.append(elemento)
    return lista_final

def guiador(offset , interleave,longitud_palabra):
    r=0
    g=0 
    b=0
    
    glo.guia_rojo=[]
    glo.guia_verde=[]
    glo.guia_azul=[]
    numero_r = offset
    numero_g = offset+interleave
    numero_b = offset+2*interleave
    glo.guia_rojo.append(numero_r*3)
    glo.guia_verde.append(numero_g*3+1)
    glo.guia_azul.append(numero_b*3+2)
    
    for i in range(0,longitud_palabra):
        if(i-(3*r) == 0):
            r=r+1
            numero_r = numero_r + interleave*3
            glo.guia_rojo.append(numero_r*3)
        elif(i-(3*g) == 1):
            g=g+1
            numero_g = numero_g + interleave*3
            glo.guia_verde.append(numero_g*3+1)
            
        elif(i-(3*b) == 2):
            b=b+1
            numero_b = numero_b + interleave*3
            glo.guia_azul.append(numero_b*3+2)

    
    

