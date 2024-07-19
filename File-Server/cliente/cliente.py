import socket

HOST = '127.0.0.1' #Definindo o IP do servidor
PORT = 50000 #Definindo a porta

# Criando o socket UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


while True:

    # Recebe a mensagem a ser enviada
    msg = input('Digite a mensagem: ')

    # Convertendo a mensagem digitada de string para bytes
    msg = msg.encode('utf-8')

    # Enviando a mensagem ao servidor
    udp_socket.sendto(msg, (HOST, PORT))
    
    # Recebendo a mensagem do servidor
    msg, cliente = udp_socket.recvfrom(512)

    # Exibe a mensagem recebida
    print(cliente, msg.decode('utf-8'))


# Fechando o socket
udp_socket.close()