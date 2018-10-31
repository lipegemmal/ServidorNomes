#Servidor para cliente de acesso indireto de Felipe Gemmal
import socket
import sys
import threading


def cliente(connection,client):
	pedido= str(connection.recv(1024).decode('utf-8')).split()
	
	if pedido[1] == "F":
		resposta = (62.1 * float(pedido[0]) ) - 44.7
	else:
		resposta = (72.7 * float(pedido[0]) ) - 58
	
	connection.send(str(resposta))
		
	connection.close()	


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = 'localhost'
porta = 12343 + 3

server.bind((ip,porta))
server.listen(10)

print("Servidor 3 ativo")
print("Esperando pedidos do DNS")
while True:
	co,pedido = server.accept()
	linha = threading.Thread(target=cliente,args=(co,pedido))
	linha.start()

server.close()
