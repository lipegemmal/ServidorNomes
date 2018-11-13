#Servidor intermediario para acesso indireto de Felipe Gemmal, Carlos Henrique Rorato Souza
# -*- coding: utf-8 -*-
import socket
import sys
import threading

#dados dos serviços
names = {"1":('localhost',"12391"), "2":('localhost',"12392"), "3":('localhost',"12393")}

#Para cada serviço, uma lista com suas palavras-chave
listaS1 = ["video","engraçado","youtube","comedia"]
listaS2 = ["audio","musica"]
listaS3 = ["imagem","foto"]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = 'localhost'
porta = 12345 # Porta padrão que será enviada

midIp = 'localhost'
midPorta = 12388


def cliente(connection,porta):

	print("Thread criada")
	nomeServico= str(connection.recv(1024).decode('utf-8'))
	
	encontrou = 0

	if nomeServico == "":
		print("Sem dados")
		return

	print(nomeServico)
	endereco = names.get(nomeServico,-1) #aqui ele deve procurar pelo número
	
	if(endereco == -1): #para cada serviço, caso não ache o número do serviço, vai procurar pelas palavras chave:
		
		for(x in listaS1): #Serviço 1
			if(x == nomeServico): 
				connection.send(("localhost"+" "+ names.get("1",-1)).encode('utf-8'))
				encontrou = 1
		for(y in listaS2): #Serviço 2
			if(y == nomeServico):
				connection.send(("localhost"+" "+ names.get("1",-1)).encode('utf-8'))
				encontrou = 1
		for(k in listaS3): #Serviço 3
			if(k == nomeServico):
				connection.send(("localhost"+" "+ names.get("1",-1)).encode('utf-8'))
				encontrou = 1

		if(encontrou == 0) print("Nome nao existe")

	else:
		connection.send(("localhost"+" "+ str(endereco)).encode('utf-8'))
		
	#conexao.close()
	connection.close()	
	return


def addService(connection,cliente):
	print("Thread criada")
	novoServico= str(connection.recv(1024).decode('utf-8')).split(" ")
	

	#print("Colocando a chave: "+novoServico[0]+" e valor : "+novoServico[1]+" no dicionario")

	#print("Tamanho da lista de strings "+ str(len(novoServico)) )
	#print("Service String:"+novoServico[0])

	print(novoServico)

	names.update({novoServico[0] : (novoServico[1], novoServico[2])})

	print("Novo servico adicionado: "+str(novoServico[0]) +" "+str(names.get(novoServico[0])))
	
	return

def connectMiddleware(ip,porta,minhaPorta):
	
	middle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	middle.connect((ip,porta))

	middle.send("addAddress".encode('utf-8'))

	resposta =str(middle.recv(1024).decode('utf-8'))

	print(resposta)	

	middle.send(str(minhaPorta).encode('utf-8'))

	resposta = str(middle.recv(1024).decode('utf-8'))

	print(resposta)

	middle.close()
	return




connectMiddleware(midIp,midPorta,porta)

server.bind((ip,porta))
server.listen(10)

print("Esperando conexao")
while True:
	
	co,endCliente = server.accept()
	print("Conexao aceita")
	
	tipo= str(co.recv(1024).decode('utf-8'))

	print(tipo +' Criando thread')
	if(tipo == 'request'):
		linha = threading.Thread(target=cliente,args=(co,porta))
		linha.start()

	elif(tipo == 'addService'):
		linha = threading.Thread(target=addService,args=(co,endCliente))
		linha.start()
	

server.close()


