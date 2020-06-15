import os
import globales as glo
import modificador as mod
import threading
#global buffer
def red(interleave ,offset,donde_termino,r):
    valor_modificado = b''
    for valor in glo.guia_rojo:
        if (donde_termino <= valor < donde_termino + len(glo.buffer)):
            glo.candado.acquire()
            para_modificar = glo.buffer[valor-donde_termino]          
            glo.candado.release()
            if(r == len(glo.global_palabra)-2):
                
                glo.candado.acquire()
                para_ocultar = glo.global_palabra[r]
                
                glo.candado.release()
                
                valor_modificado = mod.modificador(para_modificar,int(para_ocultar),"red")
                print("ULTIMO ROJO",valor_modificado , valor , para_ocultar , r)

                glo.candado.acquire()
                glo.buffer[valor-donde_termino] = valor_modificado
                glo.candado.release()
                try:
                    ident = glo.barrera.wait()
                except threading.BrokenBarrierError:
                    print(nom_hilo, 'Cancelando')
                return -40,-40
            if (r < len(glo.global_palabra)):
                para_ocultar = glo.global_palabra[r]
                valor_modificado = mod.modificador(para_modificar,int(para_ocultar),"red")
                glo.candado.acquire()
                glo.buffer[valor-donde_termino] = valor_modificado
                glo.candado.release()
            if(r > len(glo.global_palabra)):
                try:
                    ident = glo.barrera.wait()
                    return -40,-40
                except threading.BrokenBarrierError:
                    print(nom_hilo, 'Cancelando')
                else:
                    print('Ejecutando después de la espera', ident)
                            
            r = r+3
    donde_termino = donde_termino + len(glo.buffer)
    try:
        ident = glo.barrera.wait()
    except threading.BrokenBarrierError:
        print(nom_hilo, 'Cancelando')
    return donde_termino,r
def green(interleave ,offset,donde_termino,g):
    valor_modificado = b''
    
    for valor in glo.guia_verde:
        if (donde_termino <= valor < donde_termino + len(glo.buffer)):
            glo.candado.acquire()
            para_modificar = glo.buffer[valor-donde_termino]
            glo.candado.release()                        
            if(g > len(glo.global_palabra)):
                try:
                    ident = glo.barrera.wait()
                    return -40,-40
                except threading.BrokenBarrierError:
                    print(nom_hilo, 'Cancelando')
                else:
                    print('Ejecutando después de la espera', ident)
            if(g == len(glo.global_palabra)-1):
                glo.candado.acquire()
                para_ocultar = glo.global_palabra[g]
                glo.candado.release()
                valor_modificado = mod.modificador(para_modificar,int(para_ocultar),"green")
                glo.candado.acquire()
                glo.buffer[valor-donde_termino] = valor_modificado
                glo.candado.release()
                try:
                    ident = glo.barrera.wait()
                except threading.BrokenBarrierError:
                    print(nom_hilo, 'Cancelando')
                return -40,-40  
            if (g < len(glo.global_palabra)): 
                para_ocultar = glo.global_palabra[g]                   
                valor_modificado = mod.modificador(para_modificar,int(para_ocultar),"green") 
                glo.candado.acquire()  
                glo.buffer[valor-donde_termino] = valor_modificado
                glo.candado.release()
            g = g+3

    donde_termino = donde_termino + len(glo.buffer)

    try:
        ident = glo.barrera.wait()
    except threading.BrokenBarrierError:
        print(nom_hilo, 'Cancelando')
    return donde_termino,g

def blue(interleave ,offset,donde_termino,b):
    valor_modificado = b''
    for valor in glo.guia_azul:
        if (donde_termino <= valor < donde_termino + len(glo.buffer)):
            glo.candado.acquire()
            para_modificar = glo.buffer[valor-donde_termino]
            glo.candado.release()

            if(b < len(glo.global_palabra)):     
                para_ocultar = glo.global_palabra[b]              
                valor_modificado = mod.modificador(para_modificar,int(para_ocultar),"blue")
                glo.candado.acquire()
                glo.buffer[valor-donde_termino] = valor_modificado
                glo.candado.release()

            if(b > len(glo.global_palabra)-1):
                try:
                    ident = glo.barrera.wait()
                    return -40,-40
                except threading.BrokenBarrierError:
                    print(nom_hilo, 'Cancelando')
                else:
                    print('Ejecutando después de la espera', ident)             
            b = b + 3
    donde_termino = donde_termino + len(glo.buffer)

    try:
        ident = glo.barrera.wait()
    except threading.BrokenBarrierError:
        print(nom_hilo, 'Cancelando')
    return donde_termino,b




