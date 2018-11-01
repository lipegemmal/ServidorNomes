#Servidor para cliente de acesso indireto de Felipe Gemmal
import socket
import sys
import threading

ip = 'localhost'
porta = 12391

ipMiddleware = 'localhost'
portaMiddleware = 12388

def cliente(connection,client):
	pedido= connection.recv(1024).decode('utf-8')

	if len(pedido) != 1:
		resposta = "Numero_errado_de_dados"

	elif not (type(pedido[0]) is str):
		resposta = "Entrada_nao_numerica"
		
	else:
		resposta = int(pedido) * 10
	

	connection.send( str(resposta).encode('utf-8'))

	connection.close()	


def connectMiddleware(ip,porta,meuIP,minhaPorta):
	
	middle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	middle.connect((ip,porta))

	middle.send("addService".encode('utf-8'))

	resposta =str(middle.recv(1024).decode('utf-8'))

	print(resposta)	

	middle.send(('1 ' + str(meuIP) + " " + str(minhaPorta)).encode('utf-8'))

	resposta = str(middle.recv(1024).decode('utf-8'))

	print(resposta)

	middle.close()
	return

connectMiddleware(ipMiddleware, portaMiddleware, ip, porta)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((ip,porta))
server.listen(10)

print("Servico 1 ativo")
print("Esperando pedidos do DNS")
while True:
	co,pedido = server.accept()
	linha = threading.Thread(target=cliente,args=(co,pedido))
	linha.start()

server.close()
