import socket
import sys
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host =''
rota = ''
"""
sock.connect(("httpbin.org", 80))

sock.sendall(b'GET /image/jpeg HTTP/1.1\r\n'+
        b'Host: httpbin.org\r\n'+
        b'\r\n')

"""
sock.connect(("viacep.com.br", 80))
sock.send (b"GET   /ws/59124770/json/ HTTP/1.1\r\n"+
           b"Host: viacep.com.br\r\n"+
           b"\r\n")


data = sock.recv(1)

while b'\r\n\r\n' not in data:
    data += sock.recv(1)

metadados, dados = data.split(b'\r\n\r\n', 1)

http, headers = metadados.split(b'\r\n', 1)


if b'200' not in http:
    print('ERRO')
    sock.close()
    sys.exit()

print(headers)

tipo = ''
content = ''
leitura = 0
dicio = {}

for header in headers.split(b'\r\n'):
    key, value = header.split(b': ', 1)
    print(key, '->', value)
    dicio[key] = value


if b'Content-Type' in dicio.keys():
    tipo = dicio[b'Content-Type'].split(b'/', 1)

else:
    print('Tipo de conteudo nao encontrado')
    sock.close()
    sys.exit()


if b'Content-Length' in dicio.keys():
    leitura = int(dicio[b'Content-Length'])
    print('Length ->', leitura)
    fd = open("x.jpeg", "wb")
    print(dados)

    while len(dados) < leitura:
        dados += sock.recv(1024)
    
    fd.write(dados)
    fd.close()


elif b'Transfer-Encoding' in dicio.keys():
    print('chunked')
    tam += sock.recv(1)
    while b'\r\n' not in tam:
        tam += sock.recv(1)

    tam = tam.split(b'\r\n', 1)[0]
    print( int.from_bytes(tam))
    #sock.recv()

else:
    print('Tamanho nao encontrado')
    sock.close()
    sys.exit()

sock.close()