#Middleware para organizar os servidores de nomes replicados
# -*- coding: utf-8 -*-
import os
import socket, string
import sys
import threading
import heapq

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = 'localhost'
porta = 12388

server.bind((ip,porta))
server.listen(10)

#a heap é minima
heap = []

def addNameServer(connection,endClient):

    connection.send("Envie porta a ser utilizada")

    porta = str(connection.recv(1024).decode('utf-8'))

    ip,portaConexao = endClient

    heapq.heappush(heap,(1,( str(ip) ,str(porta) )))   
    for x,y in heap:
        print(str(x) +" "+ str(y) +" ")

    connection.send("Agora esta connectado")
    connection.close()
    return

def getNameAddress(connection, endClient):

    element = heapq.heappop(heap)
    
    priority , address = element
    ip, porta = address
    
    heapq.heappush(heap,(priority + 1 , address))

    
    print("Enviando "+ str(priority)+ " e " + str(address))

    connection.send(str(ip)+" "+str(porta))
    connection.close()
    return 



while True:
    connection,endClient = server.accept()

    print("Conexao estabelecida")

    tipo = str(connection.recv(1024).decode('utf-8'))

    if(tipo == 'addAddress'):
        linha = threading.Thread(target= addNameServer, args= (connection,endClient))
        linha.start()

    if(tipo == 'getAddress'):
        linha = threading.Thread(target= getNameAddress, args= (connection,endClient))
        linha.start()
    
server.close()


