import socket
import os
from helpers import get_valid_ip, get_valid_port
from time import sleep


def main():
    HOST = get_valid_ip()   # inserção do IP (localhost = 127.0.0.1)
    PORT = get_valid_port() # inserção da Porta (server rodando porta 50000)
    client((HOST, PORT))


def client(ADDR):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_client:
        socket_client.connect(ADDR)
        print(f'Conectado ao servidor em {ADDR[0]} {ADDR[1]}')

        chances = 5
        if chances == 5:
                print('Um número aleatório de 0 a 100 foi gerado.')
        
        while True:
            mensage = input('Digite um número entre 0 e 100: ')
            socket_client.sendall(mensage.encode()) # envia ao server o numero escolhido
            chances-=1  # diminui as vidas do cliente
            data = socket_client.recv(4096)
            data = data.decode()    # recebe a resposta do server
            print('Servidor: ', data)

            if data == f"Parabéns! Você acertou o número ({mensage})!":
                print("Encerrando a conexão com o servidor...")
                break
            
            if data == 'Suas chances acabaram.':
                print("Encerrando a conexão com o servidor...")
                break
    sleep(3)  # foi só para não apagar tudo sem ver a mensagem.
    menu()


def menu():
    if os.name == 'nt':
        clear_cmd = 'cls'
    else:
        clear_cmd = 'clear'

    os.system(clear_cmd)
    print('\tTela inicial do programa')
    print('-' * 40)
    print('Selecione uma das opções abaixo:\n')
    print('\t0 - Logar no servidor\n\t1 - Sair do programa\n')
    print('-' * 40)

    while True:
        op = input('-> ').strip()
        if op == '0':
            break
        elif op == '1':
            return
        else:
            print('Opção invalida!')

    os.system(clear_cmd)
    main()
menu()      
