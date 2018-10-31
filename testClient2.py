#Cliente basico acesso indireto de Felipe Gemmal
# -*- coding: utf-8 -*-
import os
import socket, string
import sys

nameServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = 'localhost'
porta = 12388

print("Conectando")

nameServer.connect((ip,porta))

print("Enviando requisicao")

#tipo de servico requisitado, colocado aqui por conta do tempo de recv do dns
nameServer.send("getAddress")

print("Recebendo resposta")

resposta = str(nameServer.recv(1024).decode('utf-8'))

print(resposta)

nameServer.close()