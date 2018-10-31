#Cliente basico acesso indireto de Felipe Gemmal
# -*- coding: utf-8 -*-
import os
import socket, string
import sys

nameServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = 'localhost'
porta = 12388


nameServer.connect((ip,porta))

print("Enviando meu nome")

nameServer.send("addAddress")

resposta = str(nameServer.recv(1024).decode('utf-8'))

print(resposta)

nameServer.close()
