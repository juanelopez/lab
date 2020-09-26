import os
import threading
from concurrent import futures
import time
import argparse
import time
import sys
import filtro
import socketserver
def tipo_archivo(extension):
    #print("EXTENSION",extension)
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
    else:
        content_type = "No soportado"
        return content_type
class servidor(socketserver.ForkingTCPServer):
    def __init__(self,server_address,RequestHandlerClass,cantidad_lectura,directorio):
        socketserver.ForkingTCPServer.__init__(self,server_address,RequestHandlerClass)
        socketserver.allow_reuse_address = True
        self.cantidad_lectura = cantidad_lectura
        self.directorio = directorio
class Manejador(socketserver.BaseRequestHandler):
    def handle(self):
        directorio = self.server.directorio
        cantidad_lectura = self.server.cantidad_lectura
        lista=[]
        enviado = self.request.recv(1024)
        enviado = enviado.decode("utf-8")
        lista = enviado.split('\n') #spplitlines es mucho mas facil lo divide completamente al enviado
        n=0
        http_version = "HTTP/1.1"
        metodo_lista = []
        metodo = lista[0]
        codigos = ["200","404","403","500"]
        mensaje = ["OK","Not Found","Forbidden","Internal Error"]
        metodo_lista=metodo.split()
        print(metodo_lista)
        metodo = metodo_lista[0]
        archivo_pedido = metodo_lista[1]
        pedido_llegando = directorio[1:] + archivo_pedido
        version_http = metodo_lista[2]
        archivo_nombre = []
        archivo_nombre = pedido_llegando.split('.',1)
        extension = archivo_nombre[-1]
        ppm_split = extension.split('?')
        extension = ppm_split[0]
        archivo_requerido = archivo_nombre[0] + "."+extension
        if(metodo == "GET"):
            if(archivo_pedido == "/"):
                archivo_requerido = directorio[1:]+"/index.html"
                extension = "html"
            try:
                fd1 = os.open(archivo_requerido,os.O_RDONLY)
                ppm_archivo = archivo_requerido
                request = http_version +" "+codigos[0] +" "+ mensaje[0]+ "\n"
                content_type = tipo_archivo(extension)
                if(content_type == "No soportado" or len(ppm_split) > 2):
                    request = http_version + " " + codigos[3] + " " + mensaje[3] + "\n"
                    os.close(fd1)
                    self.request.sendall(bytes(request, 'utf-8'))
                else:
                    self.request.sendall(bytes(request, 'utf-8'))
                    self.request.sendall(bytes(content_type, 'utf-8'))
                    size = "Content-Lenght: "+str(os.path.getsize(archivo_requerido))+"\n\n" #segundo enter separa el header del body
                    self.request.sendall(bytes(size, 'utf-8'))
                    if(extension == "ppm" and len(ppm_split) == 2):
                        os.close(fd1)
                        division_request = ppm_split[1].split("&")
                        color = division_request[0].split("=")
                        intensidad = division_request[1].split("=")
                        filtro.filtrado(color[1],intensidad[1],cantidad_lectura,ppm_archivo,self) #hago el sendall desde la funcion
                    else:
                        lectura = os.read(fd1,cantidad_lectura)
                        while(lectura != b''):
                            self.request.sendall(lectura)
                            lectura = os.read(fd1,cantidad_lectura)
                        os.close(fd1)
                        
            except:
                
                print("El archivo no existe")				
                request = http_version +" "+ codigos[1] +" "+ mensaje[1] +"\n"
                self.request.sendall(bytes(request, 'utf-8'))


            
if __name__ == "__main__":
    #---------------Argumentos------
    parser = argparse.ArgumentParser(description='Tp3- servidor')
    parser.add_argument('-s', '--size',action="store", type= int, default=1024, help="Bloque de lectura máxima para los documentos")
    parser.add_argument('-d', '--documentroot',action="store", dest="file_dir", required=True, type=str, help="Directorio donde estan los documentos web")
    parser.add_argument('-p', '--port',action="store", dest="port", required=True, type=int, help="Puerto en donde espera conexiones nuevas")
    args = parser.parse_args()
    PORT = args.port
    cantidad_lectura = args.size
    directorio = args.file_dir
    #--------Fin argumentos --------
    HOST= "0.0.0.0" #con 0.0.0.0 toma todas las ip de la maquina
    with servidor((HOST,PORT),Manejador,cantidad_lectura,directorio) as srv:        
        srv.serve_forever()
