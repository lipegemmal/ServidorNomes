#Cliente basico acesso indireto de Felipe Gemmal
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

	middleServer.send("getAddress")

	ipService, portaService = str(middleServer.recv(1024).decode('utf-8')).split(" ")

	middleServer.close()
	return ipService, portaService


def requestService(ip,porta,serviceName):
	nameServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	nameServer.connect((ip, int(porta) ))

	nameServer.send("request")

	print("Informe o serviço desejado: ")

	opcao = raw_input()

	nameServer.send(opcao)

	ipService, portaService = str(nameServer.recv(1024).decode('utf-8')).split(" ")

	nameServer.close()
	return ipService, portaService




print("Requisitando endereco do servidor de nomes:")

ipName,portaName = requestNameServer(ip,porta)

print("Recebi "+ str(ipName)+" "+str(portaName))

sys.stdout.flush()

print("Requisitando endereco do servico:")

ipService,portaService = requestService(ipName,portaName,1)

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