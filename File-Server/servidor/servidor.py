# Importando a biblioteca socket
import socket

HOST = '' #Definindo o IP do servidor
PORT = 50000 #Definindo a porta
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



# Criando o socket TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind((HOST, PORT)) # Ligando o socket a porta
tcp_socket.listen(1) # Máximo de conexões enfileiradas
print('Recebendo Mensagens...\n\n')

while True:
    con, cliente = tcp_socket.accept() # Aceita a conexão com o cliente
    print('Conectado por: ', cliente)
    while True:
        msg = con.recv(1024) #buffer de 1024 bytes
        if not msg: break
        # Imprimindo a mensagem recebida convertendo de bytes para string
        print(cliente, msg.decode('utf-8'))
        print('Finalizando Conexão do Cliente ', cliente)

    con.close()