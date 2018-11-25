#Cliente basico acesso indireto de Felipe Gemmal, Carlos Henrique Rorato Souza
# -*- coding: utf-8 -*-
import os
import socket, string
import sys

#nameServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#servico = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = 'localhost'
porta = 12388

#nameServer.connect((ip,porta))



def requestNameServer(ip, porta):
	middleServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	middleServer.connect((ip,porta))

	middleServer.send("getAddress".encode('utf-8'))

	ipService, portaService = str(middleServer.recv(1024).decode('utf-8')).split(" ")

	middleServer.close()
	return ipService, portaService


def requestService(ip,porta,serviceName):
	nameServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	nameServer.connect((ip, int(porta) ))

	nameServer.send("request".encode('utf-8'))

	resposta = str(nameServer.recv(1024).decode('utf-8'))

	print("Informe o serviço desejado: ")

	opcao = input()
	#opcao = raw_input() - deu erro no meu windows - Carlos

	nameServer.send(opcao.encode('utf-8')) #aqui ele manda a característica para o dns

	data = str(nameServer.recv(1024).decode('utf-8')).split(" ")

	ipService, portaService = data

	nameServer.close()
	return ipService, portaService




print("Requisitando endereco do servidor de nomes:")

data = requestNameServer(ip,porta)

ipName,portaName = data

print("Recebi "+ str(ipName)+" "+str(portaName))

sys.stdout.flush()

print("Requisitando endereco do servico:")

data = requestService(ipName,portaName,1)

if( str(data) == "N"):
	print("Informação errada")

ipService,portaService = data

print("Recebi "+ str(ipService)+" "+str(portaService))

sys.stdout.flush()





#while True:
	#print("Se quiser salario- 1 + salario")
	#print("Se quiser maior idade - 2 + sexo(F/M) + idade (lista 2)")
	#print("Se quiser peso ideal - 3 + altura + sexo(F/M) ( lista 4)")

	#opcao = raw_input()

	#if int(opcao) == 1:
	#	dados = raw_input()

	#elif int(opcao) == 2:
	#	sexo = raw_input()
	#	idade = raw_input()
	#	dados = sexo +" "+idade
	#else:
	#	altura = raw_input()
	#	sexo = raw_input()
	#	dados = altura+" "+sexo

#nameServer.close()