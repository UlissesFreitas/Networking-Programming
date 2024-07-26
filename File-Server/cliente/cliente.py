# Importando a biblioteca socket
import socket

HOST = '10.88.0.4' #Definindo o IP do servidor
PORT = 50000 #Definindo a porta

# Criando o socket UDP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.connect((HOST, PORT)) # Ligando o socket a porta

msg = input('Digite a mensagem: ')

# Convertendo a mensagem digitada de string para bytes
msg = msg.encode('utf-8')

# Enviando a mensagem ao servidor
tcp_socket.send(msg)

# Fechando o socket
tcp_socket.close()