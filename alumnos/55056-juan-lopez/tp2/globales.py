import threading

global buffer
buffer = []
global global_palabra
global_palabra = []

global guia_rojo
guia_rojo = []
global guia_verde
guia_verde = []
global guia_azul
guia_azul = []


#variables para controlar los problemas de concurrencia
global candado
candado = threading.Lock()
global barrera
barrera = threading.Barrier(3)
