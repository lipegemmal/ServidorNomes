#Servidor intermediario para acesso indireto de Felipe Gemmal
# -*- coding: utf-8 -*-
import socket
import sys
import threading


names = {"1":('localhost',"12391"), "2":('localhost',"12392"), "3":('localhost',"12393")}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = 'localhost'
porta = 12345

midIp = 'localhost'
midPorta = 12388


def cliente(connection,porta):

	print("Thread criada")
	nomeServico= str(connection.recv(1024).decode('utf-8'))
		
	if nomeServico == "":
		print("Sem dados")
		return

	print(nomeServico)
	endereco = names.get(nomeServico,-1)
	
	if(endereco == -1):
		print("Nome nao existe")
	
	else:
		connection.send("localhost"+" "+ endereco)
		
	#conexao.close()
	connection.close()	
	return


def addService(connection,cliente):
	print("Thread criada")
	novoServico= str(connection.recv(1024).decode('utf-8')).split(" ")
	

	#print("Colocando a chave: "+novoServico[0]+" e valor : "+novoServico[1]+" no dicionario")

	#print("Tamanho da lista de strings "+ str(len(novoServico)) )
	#print("Service String:"+novoServico[0])


	names.update({novoServico[0] : novoServico[1]})

	print("Novo servico adicionado: "+novoServico[0]+" "+names.get(novoServico[0]) )
	
	return

def connectMiddleware(ip,porta,minhaPorta):
	
	middle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	middle.connect((ip,porta))

	middle.send("addAddress")

	resposta =str(middle.recv(1024).decode('utf-8'))

	print(resposta)	

	middle.send(str(minhaPorta) )

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


