import asyncio 
import os
import socket
import argparse
import complementarias
async def handle(reader, writer,directorio,cantidad_lectura):
    data = await reader.read(100)
    request_recibida = []
    request_recibida = data.split(b'\r\n')
    message = data.decode()
    addr = writer.get_extra_info('peername')
    logger = asyncio.create_task(complementarias.mostrar_direccion(addr,directorio))
    peticion = asyncio.create_task(devolver_peticion(request_recibida,writer,directorio,cantidad_lectura))
    await logger
    await peticion
    writer.close()

async def devolver_peticion(request_recibida,writer,directorio,cantidad_lectura):
    dividir_request = request_recibida[0].decode().split(" ")
    metodo = dividir_request[0]
    archivo = dividir_request[1]
    if(directorio == "/"):
    	directorio = ""
    if(archivo != "/"):
        archivo_dividido = []
        archivo_dividido = archivo[1:].split(".")
        dividir_500_extension = []
        dividir_500_extension = archivo_dividido[1].split('?')
        if(len(archivo_dividido) == 2):
            extension = archivo_dividido[1]
        else:
            extension = " "
    if (archivo == "/"):
        archivo = "/index.html"
        extension = "html"
        dividir_500_extension = ["html"]    
    version = str.encode(dividir_request[2])    
    if(len(dividir_500_extension) > 1):
        enviar_500 = version + b' 500 Internal Server Error\n'
        writer.write(enviar_500)
    else:
        if(metodo == "POST"):
            enviar_500 = version + b' 500 Internal Server Error\n'
            writer.write(enviar_500)
        elif(metodo == "GET"):
            try:
                fd1 = os.open(directorio+archivo[1:],os.O_RDONLY)
                request = version+b' 200 OK\n'
                content_type = complementarias.tipo_archivo(extension)
                request_lenght = b'Content-Lenght:20000\n\n'
                writer.write(request)
                writer.write(bytes(content_type,'utf-8'))
                writer.write(request_lenght)             
                lectura = os.read(fd1,cantidad_lectura)
                while(lectura != b''):
                    writer.write(lectura)
                    lectura = os.read(fd1,cantidad_lectura)
                os.close(fd1)
            except:
                print("El archivo no existe")				
                request = version +b' 404 Not Found\n'
                writer.write(request)
    await writer.drain()


async def main():
    parser = argparse.ArgumentParser(description='Tp4- servidor asyncio')
    parser.add_argument('-s', '--size',action="store", type= int, default=1024, help="Bloque de lectura máxima para los documentos")
    parser.add_argument('-d', '--documentroot',action="store", dest="file_dir", required=True, type=str, help="Directorio donde estan los documentos web")
    parser.add_argument('-p', '--port',action="store", dest="port", required=True, type=int, help="Puerto en donde espera conexiones nuevas")
    args = parser.parse_args()
    PORT = args.port
    cantidad_lectura = args.size
    directorio = args.file_dir
    if(directorio[-1] != "/"):
        directorio = directorio+"/"
    server = await asyncio.start_server(lambda r,w: handle(r,w,directorio,cantidad_lectura), ('::','0.0.0.0'),PORT)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')  
    async with server:
        await server.serve_forever()
 #mostrar numero de proceso
asyncio.run(main())
