import socket
import threading
import time
import os

# Definindo o IP do servidor
HOST = ''

# Definindo a porta
PORT = 5000

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


class servidor:
    
    def __init__(self, host, porta):
        self.host = host
        self.porta = porta
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.bind((self.host, self.porta))
        # isso fica aqui ? eis a questao
        self.tcp_socket.listen(1)
   
    def listar_arquivos(self):
        # Obtendo o diretório corrente
        strDiretorio = os.path.abspath(__file__)
        strDiretorio = os.path.dirname(strDiretorio)
        strDiretorio = strDiretorio + '/arquivos/'

        result = ' '
        for arq in os.listdir(strDiretorio):
            result += arq + ' '

        return result

    def run(self):
        
        while True:
            # antes o codigo estava aqui
            # self.tcp_socket.listen(1)
            print('Esperando uma nova conexao')

            self.con, self.cliente = self.tcp_socket.accept()
            print('Conectado por: ', self.cliente)
        
            while True:
                cmd = self.con.recv(1)

                if cmd == CMD_EXIT:
                    print('Encerrando conexao')
                    self.con.sendall(STATUS_END)
                    break

                elif cmd == CMD_LS:

                    # Cria uma string com o nome dos arquivos
                    lista = self.listar_arquivos()

                    # envia um LS ok para o cliente
                    self.con.sendall(STATUS_LS)

                    # Envia a lista de arquivos existentes
                    self.con.sendall(lista.encode('utf-8'))


                elif cmd == CMD_GET:
                    # envia um RCV
                    self.con.sendall(STATUS_RCV)

                    # recebe o nome do arquivo a ser enviado
                    nomeArq = self.con.recv(1024)
                    nomeArq = nomeArq.decode('utf-8')
                    print(nomeArq)

                    try:
                        strDiretorio = os.path.abspath(__file__)
                        strDiretorio = os.path.dirname(strDiretorio)
                        strDiretorio = strDiretorio + '/arquivos/' + nomeArq

                        nomeArq = os.path.relpath(strDiretorio)

                        # gera um erro caso o arquivo seja muito grande
                        size = os.path.getsize(nomeArq)  

                        # verifica o tamanho do arquivo
                        if size > MAX_SIZE:
                            raise ValueError

                        # cria arquivo
                        fd = open(nomeArq, 'rb')

                        # 
                        self.con.sendall(STATUS_FOUND)
                        # envia o tamando do arquivo
                        self.con.sendall(str(size).encode('utf-8'))

                        # recebe o local de inicio do download
                        leitura = self.con.recv(size)
                        leitura = int(leitura.decode('utf-8'))
                        fd.seek(leitura)

                        while leitura < size:
                            # le o conteudo do arquivo
                            leitura += 1024
                            data = fd.read(leitura)
                            self.con.sendall(data)


                        print(nomeArq, '->', self.cliente)
                        fd.close()

                    except FileExistsError:
                        print('pedido de arquivo inexistente')
                        self.con.sendall(STATUS_NOT_FOUND)

                    except ValueError:
                        self.con.sendall(STATUS_BAD)

                else:
                    print('1-BAD REQUEST', self.cliente)
                    self.con.sendall(STATUS_BAD)
            

            # THE END
            self.con.close()



if __name__ == '__main__':
    servidor = servidor(HOST, PORT)
    srv = threading.Thread(target=servidor.run)

    srv.start()

