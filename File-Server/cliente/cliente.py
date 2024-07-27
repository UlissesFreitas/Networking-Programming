# Importando a biblioteca socket
import socket

HOST = '10.88.0.4' #Definindo o IP do servidor
PORT = 50004 #Definindo a porta
MAX_SIZE = 4294967296

# status de erro interno do servidor
STATUS_ISE = '500'

# status 404 arquivo nao encontrado
STATUS_NOT_FOUND = '404'

# status 400 requisicao invalida
STATUS_BAD = '400'

# status 302 arquivo encontrado
STATUS_FOUND  = '302'

# status 200 ok arquivo enviado
STATUS_OK = '200'



# Criando o socket UDP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.connect((HOST, PORT)) # Ligando o socket a porta


while True:
    cmd = input('Digite a mensagem: ')

# Convertendo a mensagem digitada de string para bytes
    cmd = cmd.encode('utf-8')

# analisa se o comando e valido


# Enviando o comando ao servidor
    tcp_socket.send(cmd)

# Espera o codigo de status enviado pelo servidor


    print(status.decode('utf-8'))

# Fechando o socket
tcp_socket.close()