#Servidor para cliente de acesso indireto de Felipe Gemmal, Carlos Henrique Rorato Souza
import socket
import sys
import threading

#serviço ip/porta
ip = 'localhost'
porta = 14279


#informaçoes do middleware
ipMiddleware = 'localhost'
portaMiddleware = 12388

myName = '3'
keys = "IMC gordura"



def cliente(connection,client):

	string = ("Servico de teste de calculo de IMC, envie sexo(F/M) e o peso em kg")
	connection.send(("1 "+string).encode('utf-8'))

	pedido= str(connection.recv(1024).decode('utf-8')).split()
	
	if pedido[1] == "F":
		resposta = (62.1 * float(pedido[0]) ) - 44.7
	else:
		resposta = (72.7 * float(pedido[0]) ) - 58
	
	connection.send(str(resposta))
		
	connection.close()	


def connectMiddleware(ip, porta, meuNome, keys, meuIP, minhaPorta):

	middle = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	middle.connect((ip, porta))

	middle.send("addService".encode('utf-8'))

	resposta = str(middle.recv(1024).decode('utf-8'))

	print(resposta)

	middle.send((meuNome+" " + str(meuIP) + " " +
              str(minhaPorta)).encode('utf-8'))

	resposta = str(middle.recv(1024).decode('utf-8'))

	print(resposta)

	middle.send((keys).encode('utf-8'))

	resposta = str(middle.recv(1024).decode('utf-8'))

	print(resposta)

	middle.close()
	return


connectMiddleware(ipMiddleware, portaMiddleware, myName, keys, ip, porta)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((ip,porta))
server.listen(10)

print("Servidor 3 ativo")
print("Esperando pedidos do DNS")
while True:
	co,pedido = server.accept()
	linha = threading.Thread(target=cliente,args=(co,pedido))
	linha.start()

server.close()
