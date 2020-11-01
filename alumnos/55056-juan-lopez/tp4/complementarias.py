import time 
import asyncio 
import os
async def mostrar_direccion(addr,directorio):
    print(addr,time.strftime('%x %X'))
    escribir = "Direccion: " + addr[0] + " Puerto: "+str(addr[1]) + " Fecha: "+time.strftime('%x %X')+"\n"
    fd2 = os.open(directorio+"log.txt",os.O_CREAT|os.O_WRONLY|os.O_APPEND)
    os.write(fd2,bytes(escribir,"utf-8"))
    os.close(fd2)
def tipo_archivo(extension):
    if (extension == "jpg"):
        content_type= "Content-Type: image/"+extension+"\n"
        return content_type
    elif(extension == "html" or extension == "htm"):
        content_type= "Content-Type: text/"+extension+"\n"
        return content_type
    elif(extension == "pdf"):
        content_type= "Content-Type: application/"+extension+"\n"
        return content_type
    elif(extension == "ppm"):
        content_type= "Content-Type: image/x-portable-pixmap\n"
        return content_type
    elif(extension == "ico"):
        content_type = "Content-Type: image/x-icon\n"
        return content_type
    else:
        content_type = "No soportado"
        return content_type