# Importando as bibliotecas
import socket
import os

# Definindo o IP do servidor
HOST = ''

# Definindo a porta
PORT = 50008

# Tamanho maximo de um arquivo
MAX_SIZE = 4294967296

# Comando de saida
CMD_EXIT = b'0'

# Comandos para listar os arquivos
CMD_LS = b'1'

# Comando para enviar
CMD_GET = b'2'

# status 200 ok
STATUS_OK = b'3'

# status 201 LS OK
STATUS_LS = b'4'

# status 302 arquivo encontrado
STATUS_FOUND = b'5'

# status 404 arquivo nao encontrado
STATUS_NOT_FOUND = b'6'

# status 400 requisicao invalida
STATUS_BAD = b'7'

# status 202, esperando o nome do arquivo
STATUS_RCV = b'8'

# status 000, Encerrando conexao
STATUS_END = b'9'


# Retorna uma lista com os arquivos disponiveis na pasta de
def listar_arquivos():
    # Obtendo o diretório corrente
    strDiretorio = os.path.abspath(__file__)
    strDiretorio = os.path.dirname(strDiretorio)
    strDiretorio = strDiretorio + '/arquivos/'

    result = ' '
    for arq in os.listdir(strDiretorio):
        result += arq + ' '

    return result


# Criando o socket TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ligando o socket a porta
tcp_socket.bind((HOST, PORT))

# Máximo de conexões enfileiradas
tcp_socket.listen(1)

print('Servidor iniciado...\n\n')

while True:

    print('Esperando uma nova conexao')

    # Aceita a conexão com o cliente
    con, cliente = tcp_socket.accept()
    print('Conectado por: ', cliente)

    while True:
        # Espera o primeiro comando
        cmd = con.recv(1)

        # testa se e o comando de saida
        if cmd == CMD_EXIT:
            con.sendall(STATUS_END)
            break

        elif cmd == CMD_LS:

            # Cria uma string com o nome dos arquivos
            lista = listar_arquivos()

            # envia um LS ok para o cliente
            con.sendall(STATUS_LS)

            # Envia a lista de arquivos existentes
            con.sendall(lista.encode('utf-8'))

        # Enviar arquivo
        elif cmd == CMD_GET:

            # envia um GET
            con.sendall(STATUS_RCV)

            # recebe o nome do arquivo a ser enviado
            nomeArq = con.recv(1024)
            nomeArq = nomeArq.decode('utf-8')
            print(nomeArq)

            try:
                strDiretorio = os.path.abspath(__file__)
                strDiretorio = os.path.dirname(strDiretorio)
                strDiretorio = strDiretorio + '/arquivos/' + nomeArq

                nomeArq = os.path.relpath(strDiretorio)

                # gera um erro caso o arquivo seja muito grande
                size = os.path.getsize(nomeArq)

                if size > MAX_SIZE:
                    raise ValueError

                fd = open(nomeArq, 'rb')

                #
                con.sendall(STATUS_FOUND)
                # envia o tamando do arquivo
                con.sendall(str(size).encode('utf-8'))

                # recebe o local de inicio do download
                leitura = con.recv(size)
                leitura = int(leitura.decode('utf-8'))
                fd.seek(leitura)

                while leitura < size:
                    # le o conteudo do arquivo
                    leitura += 1024
                    data = fd.read(leitura)
                    con.sendall(data)
        

                print(nomeArq, '->', cliente)
                fd.close()
            except FileNotFoundError:
                print('pedido de arquivo inexistente')
                con.sendall(STATUS_NOT_FOUND)

            except ValueError:
                con.sendall(STATUS_BAD)

        else:
            print('1-BAD REQUEST', cliente)
            con.sendall(STATUS_BAD)


    # THE END
    con.close()
    
tcp_socket.close()
