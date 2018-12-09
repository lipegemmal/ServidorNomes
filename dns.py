#Servidor intermediario para acesso indireto de Felipe Gemmal, Carlos Henrique Rorato Souza
# -*- coding: utf-8 -*-
import socket
import sys
import threading
#dados guardados em maps
#names = {"1":("localhost","1234")}
#keys = {"1":(listaS1)}

names = {}
keys ={}

#Para cada serviço, uma lista com suas palavras-chave
#listaS1 = ["video","engraçado","youtube","comedia"]
#listaS2 = ["audio","musica"]
#listaS3 = ["imagem","foto"]



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#ip e porta do servidor de nomes
ip = 'localhost'
porta = 12351 # Porta padrão que será enviada

#ip e porta do middleware
midIp = 'localhost'
midPorta = 12388


def cliente(connection,porta):

	print("Thread criada em busca por nome")
	
	connection.send("OK".encode('utf-8'))
	
	nomeServico= str(connection.recv(1024).decode('utf-8')).split(" ")
	
	if nomeServico[0] == "":
		print("Sem dados")
		connection.send(("N").encode('utf-8'))
		connection.close()
		return

	print(nomeServico)
	endereco = names.get(nomeServico[0],-1) #aqui ele deve procurar pelo nome do serviço
	

	#Não encontrou o serviço
	if(endereco == -1):
		connection.send(("N").encode('utf-8'))
	#Encontrou o nome do serviço
	else:
		returnip, returnporta = endereco
		connection.send((str(returnip)+" "+ returnporta).encode('utf-8'))
		
	connection.close()	
	return


def clienteKey(connection, porta):

	print("Thread criada em busca por chave")

	connection.send("OK".encode('utf-8'))

	nomeServico = str(connection.recv(1024).decode('utf-8')).split(" ")

	if nomeServico[0] == "":
		print("Sem dados")
		connection.send(("N").encode('utf-8'))
		connection.close()
		return

	print("Procurando por:"+nomeServico[0])
	# aqui ele deve procurar pelo nome do serviço
	encontrou = 0

	for x in keys.keys():   #para cada serviço
		y = keys.get(x)		#pegar as descrições
		for z in range (len(y)):  #e comparar ela com o que o cliente mandou
			if(y[z] == nomeServico[0]):
				encontrou = 1
				servico = x
				break
		if(encontrou == 1):
			break

	#Não encontrou o serviço
	if(encontrou == 0): 
		print("Nome nao existe")
		connection.send(("N").encode('utf-8'))
	#Encontrou o serviço
	else:
		endereco = names.get(servico, -1)
		returnip, returnporta = endereco
		connection.send((returnip+" "+ returnporta).encode('utf-8'))


	connection.close()
	return



def addService(connection,cliente):
	print("Thread criada")

	connection.send("OK".encode('utf-8'))

	#recebe nome , ip e porta do serviço
	novoServico= str(connection.recv(1024).decode('utf-8')).split(" ")
	
	connection.send("OK".encode('utf-8'))

	#recebe as chaves de busca do novo servico
	chavesServico = str(connection.recv(1024).decode('utf-8')).split(" ")

	print(chavesServico)
	

	#print("Colocando a chave: "+novoServico[0]+" e valor : "+novoServico[1]+" no dicionario")

	#print("Tamanho da lista de strings "+ str(len(novoServico)) )
	#print("Service String:"+novoServico[0])

	#for x in range (3,len(novoServico)):
	#	listaAux.append(novoServico[x])

	names.update({novoServico[0] : (novoServico[1], novoServico[2])})
	keys.update({novoServico[0]: chavesServico})

	print("Novo servico adicionado: "+str(novoServico[0]) +" "+str(names.get(novoServico[0])))

	connection.send("Novo servico adicionado".encode('utf-8'))
	
	connection.close()
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
	if(tipo == "request"):
		linha = threading.Thread(target=cliente,args=(co,porta))
		linha.start()

	elif(tipo == "addService"):
		linha = threading.Thread(target=addService,args=(co,endCliente))
		linha.start()

	elif(tipo == "keyRequest"):
		linha = threading.Thread(target=clienteKey,args=(co,porta))
		linha.start()

server.close()


