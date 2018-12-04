#Middleware para organizar os servidores de nomes replicados
# -*- coding: utf-8 -*-
import os
import socket, string
import sys
import threading
import heapq
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = 'localhost'
porta = 12388

server.bind((ip,porta))
server.listen(10)

#a heap é minima
heap = []

def addNameServer(connection,endClient):

    connection.send("Envie porta a ser utilizada".encode('utf-8'))

    porta = str(connection.recv(1024).decode('utf-8'))

    ip,portaConexao = endClient

    heapq.heappush(heap,(1,( str(ip) ,str(porta) )))   
    for x,y in heap:
        print(str(x) +" "+ str(y) +" ")

    connection.send("Agora esta connectado".encode('utf-8'))
    connection.close()
    return

def sendHeap(mensagem,chaves,parIpPorta):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip,porta = parIpPorta

    server.connect((str(ip),int(porta)))

    server.send("addService".encode('utf-8'))

	#print("Requisicao de criacao de servico sendo realizada ...")
	#time.sleep(1)
    
    resposta = str(server.recv(1024).decode('utf-8'))

    #envia ip e porta do servico
    server.send(mensagem.encode('utf-8'))

    
    resposta = str(server.recv(1024).decode('utf-8'))

    server.send(chaves.encode('utf-8'))

    resposta = str(server.recv(1024).decode('utf-8'))

    server.close()
    return

def addService(connection,endClient):
    connection.send("Envie porta a ser utilizada".encode('utf-8'))
    mensagem_service = str(connection.recv(1024).decode('utf-8'))

    connection.send("Ip e porta recebidos".encode('utf-8'))
	
    chaves = str(connection.recv(1024).decode('utf-8'))

    for x,y in heap:
    	sendHeap(mensagem_service,chaves,y)

    connection.send("Agora esta connectado".encode('utf-8'))
    connection.close()
    return

def getNameAddress(connection, endClient):

    element = heapq.heappop(heap)
    
    priority , address = element
    ip, porta = address
    
    heapq.heappush(heap,(priority+1 , address)) # para não começar de zero e ter um limite para a prioridade

    
    print("Enviando "+ str(priority)+ " e " + str(address))

    connection.send((str(ip)+" "+str(porta)).encode('utf-8'))
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

    if(tipo == 'addService'):
    	linha = threading.Thread(target = addService, args = (connection, endClient))
    	linha.start()
    
server.close()


