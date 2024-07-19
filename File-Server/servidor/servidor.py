import os
import socket

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

