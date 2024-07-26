import os
import socket

HOST = ''
PORT = 12345
MAX_SIZE = 4294967296


# status de erro interno do servidor
STATUS_ISE = 500

# status 404 arquivo nao encontrado
STATUS_NOT_FOUND = 404

# status 400 requisicao invalida
STATUS_BAD = 400

# status 302 arquivo encontrado
STATUS_FOUND  = 302

# status 200 ok arquivo enviado
STATUS_OK = 200


# Retorna uma lista com os arquivos disponiveis na pasta de 
# Funcao 100% pronta
def listar_arquivos():
    # Obtendo o diretório corrente
    strDiretorio = os.path.abspath(__file__)
    strDiretorio = os.path.dirname(strDiretorio)
    strDiretorio = strDiretorio + '/arquivos/'


    #for i in os.listdir(strDiretorio):
    #   print('\033[32m' +  i + '\033[0;0m' )

    return os.listdir(strDiretorio)


# Verifica se o arquivo existe no diretório local   
# Funcao 80% pronta, falta retirar os caracteres especiais
# Vitoria

def VerificaArquivo(fileName):
    strDiretorio = os.path.abspath(__file__)
    strDiretorio = os.path.dirname(strDiretorio)
    strDiretorio = strDiretorio + '/arquivos/'

    if not os.path.exists(strDiretorio + fileName):
        return False
    
    return True


# Cria o socket 
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# liga o socket a porta
tcp_socket.bind((HOST, PORT))

tcp_socket.listen(1)

while True:
    print('oi')
    # Aceita a conexao do cliente
    con, cliente = tcp_socket.accept()

    print('Conectado por: ', cliente)

    # Recebe o primeiro comando do cliente
    data = con.recv(1024)
    if not data: break




    """
    # Verifica se o arquivo existe no diretório local
    if VerificaArquivo(fileName):
        # Envia o arquivo para o cliente
        with open(strDiretorio + fileName, 'rb') as file:
            data = file.read(1024)
            while data:
                socket.sendall(data)
                data = file.read(1024)

    else:
        # eviar mensagem dizendo que o arquivo nao existe
        socket.sendall('Arquivo nao existe'.encode('utf-8'))
    """

socket.close()
