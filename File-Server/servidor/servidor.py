import os
import socket

HOST = '127.0.0.1'
PORT = 12345

# Lista os arquivos disponíveis no diretório local
def listar_arquivos():
    # Obtendo o diretório corrente
    strDiretorio = os.path.abspath(__file__)
    strDiretorio = os.path.dirname(strDiretorio)
    strDiretorio = strDiretorio + '/arquivos/'

    print('Lista de arquivos disponiveis\n' )
    #print(os.listdir())
    for i in os.listdir(strDiretorio):
        print('\033[32m' +  i + '\033[0;0m' )

    print('\n')


# Verifica se o arquivo existe no diretório local   
def VerificaArquivo(fileName):
    strDiretorio = os.path.abspath(__file__)
    strDiretorio = os.path.dirname(strDiretorio)
    strDiretorio = strDiretorio + '/arquivos/'

    if not os.path.exists(strDiretorio + fileName):
        return False
    else:
        return True
    
# Cria o socket 
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))


while True:

    # Lista os arquivos disponíveis no diretório local    
    listar_arquivos()

    # Recebe o nome do arquivo que o cliente deseja baixar
    data, source = socket.recvfrom(1024)
    fileName =data.decode('utf-8')
    if not fileName:
        break


    
    # Verifica se o arquivo existe no diretório local
    if VerificaArquivo(fileName):
        # Envia o arquivo para o cliente
        with open(strDiretorio + fileName, 'rb') as file:
            data = file.read(1024)
            while data:
                socket.sendall(data)
                data = file.read(1024)
        print('Arquivo enviado com sucesso!')
    else:
        print('Arquivo não encontrado!')

socket.close()