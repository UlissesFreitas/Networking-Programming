# Importando a biblioteca socket
import socket
import os

# Definindo o IP do servidor# Definindo a porta
HOST = '10.88.0.4' 

# Definindo a porta
PORT = 5000

# Tamanho maximo de um arquivo
MAX_SIZE = 4294967296
# Comando de saida



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

# Criando o socket UDP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.connect((HOST, PORT)) # Ligando o socket a porta


while True:
    cmd = input('Digite um comando\n'+
        '0 - EXIT\n1 - LS \n2- GET\n-> ').upper()
    

    # caso seja enviado um comando como 23
    # sera lido somente o numero 2
    # e o numero 3 influenciara na proxima leitura
    if len(cmd) != 1:
        print( '\033[1;31m' + 'Comando invalido' + '\033[0;0m')
        continue


    # Convertendo a mensagem digitada de string para bytes
    cmd = cmd.encode('utf-8')

    # Enviando o comando ao servidor
    tcp_socket.sendall(cmd)


    # Espera o codigo de status enviado pelo servidor
    status = tcp_socket.recv(1)

    # ---------------------------------------------------------
    #print(status.decode('utf-8'))
    
    if status == STATUS_END:
        break

    # O comando estava errado
    elif status == STATUS_BAD:
        print( '\033[1;31m' + 'Comando invalido' + '\033[0;0m')     

    # pediu a lista de arquivos
    elif status == STATUS_LS:
        print('\033[1;32m' + '--Lista de Arquivos--'+ '\033[0;0m')
        lista = tcp_socket.recv(4096)
        lista = lista.decode('utf-8')
        lista = lista.split(' ')
        
        for l in lista:
            if l:
                print('\033[1;32m' + ' - ' + l + '\033[0;0m')

    
    # pede um arquivo
    elif status == STATUS_RCV:

        nome = input('Qual o nome do arquivo: ')

        while len(nome) < 1:
            nome = input('Qual o nome do arquivo: ')
        

        # Pede o arquivo ao servidor
        tcp_socket.send(nome.encode('utf-8'))

        # recebe o novo STATUS, se o arquivo existe ou nao
        status = tcp_socket.recv(1)
        print(status)

        if status == STATUS_NOT_FOUND:
            print('\033[1;31m' + 'Arquivo nao existe' + '\033[0;0m')
            continue

        elif status == STATUS_FOUND:
            
            # recebe o tamanho do arquivo
            size = tcp_socket.recv(MAX_SIZE)
            size = int(size.decode('utf-8'))
            
            try:
                posi = int(input(f'Local de inicio MAX({size}): '))
                if posi > size or posi < 0: raise ValueError
            
            except:
                print('\033[1;31m' + 'local invalido' + '\033[0;0m')
                print('\033[1;31m' + 'iniciando do valor zero(0)' + '\033[0;0m')
                posi = 0


            # informa ao servidor o local de inicio do download
            tcp_socket.send(str(posi).encode('utf-8'))


            # cria o arquivo
            
            strDiretorio = os.path.abspath(__file__)
            strDiretorio = os.path.dirname(strDiretorio)
            strDiretorio = strDiretorio 
            os.makedirs('cliente/downloads', exist_ok=True)
            strDiretorio = strDiretorio +'/downloads/'+ nome

            nome = os.path.relpath(strDiretorio)
            
            arquivo = open(nome, 'wb')
            
            # começa a leitura
            while posi < size:
                bytes = tcp_socket.recv(1024)
                arquivo.write(bytes)
                posi += 1024
            
            
            arquivo.close()
            print(nome, '\033[1;32m' + 'Download completo' +'\033[0;0m')
        else:
            print('\033[1;31m' + '1 - ERRO INTERNO NO SERVIDOR' + '\033[0;0m')
    
    else:
        print('\033[1;31m' + '2 - ERRO INTERNO NO SERVIDOR' + '\033[0;0m')
        

# Fechando o socket
tcp_socket.close()