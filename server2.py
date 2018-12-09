#Servidor para cliente de acesso indireto de Felipe Gemmal, Carlos Henrique Rorato Souza
# -*- coding: utf-8 -*-
import socket
import sys
import threading

#serviço ip /porta
ip = 'localhost'
porta = 12346 

#informaçoes do middleware
ipMiddleware = 'localhost'
portaMiddleware = 12388

myName = '2'
keys = "sexo maioridade"


def cliente(connection,client):
	string = ("Servico de teste de maioridade, envie sexo(F/M) e idade em uma linha")
	connection.send(("1 "+string).encode('utf-8'))

	pedido= str(connection.recv(1024).decode('utf-8')).split(" ")

	print(pedido)
	print(len(pedido))

	#verificando erros		
	if len(pedido) != 2 :
		resposta = "Dados_de_entrada_invalidos"

	#executando função do serviço
	elif pedido[0] == "F":
		if int(pedido[1]) >= 21:
			print("Entrei 1")
			resposta = "Sim"
		else:
			print("Entrei 2")
			resposta = "Nao"

	elif pedido[0] == "M":
		if int(pedido[1]) >= 18:
			print("Entrei 3")
			resposta = "Sim"
		else:
			print("Entrei 4")
			resposta = "Nao"
	else:
		print("Entrei 5")
		resposta = "Entrada_1_errada"
	
	connection.send(resposta)
		
	connection.close()	


def connectMiddleware(ip, porta, meuNome,keys, meuIP, minhaPorta):

	middle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	middle.connect((ip, porta))

	middle.send("addService".encode('utf-8'))

	resposta = str(middle.recv(1024).decode('utf-8'))

	print(resposta)

	middle.send((meuNome+" "+ str(meuIP) + " " + str(minhaPorta)).encode('utf-8'))

	resposta = str(middle.recv(1024).decode('utf-8'))

	print(resposta)

	middle.send((keys).encode('utf-8'))

	resposta = str(middle.recv(1024).decode('utf-8'))

	print(resposta)

	middle.close()
	return

connectMiddleware(ipMiddleware,portaMiddleware,myName,keys,ip,porta)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((ip,porta))
server.listen(10)

print("Servidor 2 ativo")
print("Esperando pedidos do DNS")
while True:
	co,pedido = server.accept()
	linha = threading.Thread(target=cliente,args=(co,pedido))
	linha.start()

server.close()
