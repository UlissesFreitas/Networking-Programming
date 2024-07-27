# Importando a biblioteca socket
import socket
import os 

HOST = '' #Definindo o IP do servidor
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

# Retorna uma lista com os arquivos disponiveis na pasta de 
# Funcao 100% pronta
def listar_arquivos():
    # Obtendo o diretório corrente
    strDiretorio = os.path.abspath(__file__)
    strDiretorio = os.path.dirname(strDiretorio)
    strDiretorio = strDiretorio + '/arquivos/'

    #   print('\033[32m' +  i + '\033[0;0m' )

    return os.listdir(strDiretorio)


# Verifica se o arquivo existe no diretório local   
# Funcao 80% pronta, falta retirar os caracteres especiais
# Vitoria

def retirando_caracteres(arquivo):
    permitidos="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-."
    filename=''.join(letra for letra in arquivo if letra in permitidos)
    return filename

def VerificaNomeArquivo(filename):
    strDiretorio = os.path.abspath(__file__)
    strDiretorio = os.path.dirname(strDiretorio)
    strDiretorio = strDiretorio + '/arquivos/'

    if not filename: return False
    if not os.path.exists(strDiretorio + filename):
        return False
    
    return True

def VerificaComando(comando):
    # verifica se o comando começa com GET/
    # vitoria
    pass

# Criando o socket TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind((HOST, PORT)) # Ligando o socket a porta
tcp_socket.listen(1) # Máximo de conexões enfileiradas
print('Recebendo Mensagens...\n\n')

while True:
    print('Esperando uma nova conexao')
    con, cliente = tcp_socket.accept() # Aceita a conexão com o cliente
    print('Conectado por: ', cliente)
    
    
    while True:
        # Espera a primeira mensagem
        # deve ser um comando para listar, enviar ou sair
        cmd = con.recv(10)

        if not cmd: continue



        print('.')
        msg = con.recv(1024) #buffer de 10 bytes
        if not msg: continue
        # a msg que deve ser um comando no formato
        # GET/arquivo.txt
        # GET/boneco.jpeg
        # analisar para saber se o comando e valido
        # se nao contiver 'GET/' em msg o comando sera consideraddo invalido
        # caso o comando seja invalido deve enviar um codigo de erro ao cliente
        # e depois voltar ao inicio do while
        # vitoria

        # --------------------------
        # Analisa se o nome do arquivo e valido, se o arquivo existe
        # caso o arquivo nao exista retorna um codigo de erro ao cliente


        # Imprimindo a mensagem recebida convertendo de bytes para string
        print(cliente, msg)
        



# THE END
con.close()