#Servidor para cliente de acesso indireto de Felipe Gemmal, Carlos Henrique Rorato Souza
# -*- coding: utf-8 -*-
import socket
import sys
import threading

#informações do serviço
ip = 'localhost'
porta = 12393

#informaçoes do middleware
ipMiddleware = 'localhost'
portaMiddleware = 12388

name = '1'
data = "teste1 batata"

def cliente(connection,client):
	string = ("Servico de multiplicacao, envie um numero")
	connection.send(("1 "+string).encode('utf-8'))
	
	pedido= str(connection.recv(1024).decode('utf-8'))

	#if len(pedido) != 1:
	#	resposta = "Numero_errado_de_dados"
	#elif not (type(pedido[0]) is str):
	#	resposta = "Entrada_nao_numerica"
	#else:
	resposta = int(pedido) * 10
	

	connection.send( str(resposta).encode('utf-8'))

	connection.close()	


def connectMiddleware(ip,porta,data,meuIP,minhaPorta):
	
	middle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	middle.connect((ip,porta))

	middle.send("addService".encode('utf-8'))

	resposta =str(middle.recv(1024).decode('utf-8'))

	print(resposta)	

	middle.send(('1 ' + str(meuIP) + " " + str(minhaPorta)).encode('utf-8'))

	resposta = str(middle.recv(1024).decode('utf-8'))

	print(resposta)

	middle.send((data).encode('utf-8'))

	resposta = str(middle.recv(1024).decode('utf-8'))

	print(resposta)	

	middle.close()
	return

connectMiddleware(ipMiddleware, portaMiddleware,data ,ip, porta)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((ip,porta))
server.listen(10)

print("Servico 1 ativo")
while True:
	co,pedido = server.accept()
	linha = threading.Thread(target=cliente,args=(co,pedido))
	linha.start()

server.close()
