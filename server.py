import socket
import threading
from time import sleep
import random

HOST = 'localhost'  # 127.0.0.1
PORT = 50000

def handle_client(socket_client, client_address, numero):
        print(f'Conectado em {client_address}')  # cliente conectado
        chances = 5

        while chances >= 0:  # loop para receber as mensagens
                data = socket_client.recv(4096)
                data = data.decode()  # recebendo a mensagem e decodificando em string
                
                if data.isdigit():  # verifica se a string contém apenas dígitos
                        data = int(data)  # converte a string em um número inteiro
                        print(f'O cliente em {client_address} escolheu: {data}')

                        mensagem = None
                        if data == numero:
                                print("Cliente acertou o número!")
                                mensagem = f'Parabéns! Você acertou o número ({data})!'
                                mensagem = mensagem.encode()
                                socket_client.sendall(mensagem)
                                socket_client.close()
                                break                        
                        elif data > numero and data <= 100:
                                mensagem = 'O numero aleatório é menor!'
                                chances-=1
                        elif data < numero and data >= 0:
                                mensagem = 'O número aleatório é maior!'
                                chances-=1
                        else: 
                                mensagem = 'Número inválido. Informe um valor de 0 a 100'
                        print(mensagem)
                        mensagem = mensagem.encode()   # transformando em bytes para enviar
               
                        if chances > 0:
                                socket_client.sendall(mensagem)
                        elif chances == 0:
                                mensagem = 'Suas chances acabaram.'
                                print(mensagem)
                                socket_client.sendall(mensagem.encode())
                                print('\nEncerrando conexões com o cliente.')
                                break
                
                else:
                        print(f'O cliente em {client_address} enviou um valor inválido: {data}')
                        socket_client.sendall('Você escolheu um valor inválido. Selecione outro.'.encode())
               

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:  # criando um socket do tipo TCP
    socket_server.bind((HOST, PORT))  # associa um socket a um endereço e uma porta especifica
    socket_server.listen()      # começa a "escutar" as conexões
    print('Aguardando conexão de um cliente...')

    while True:  # loop que fica sempre procurando conexões
        socket_client, client_address = socket_server.accept()  # aceitando a conexão do client
        print('\nNovo cliente conectado. Inicializando jogo...')
        numero = random.randint(0, 100)                         # gerando um numero aleatorio
        print(f'O número escolhido é: {numero}')                
        
        client_thread = threading.Thread(target=handle_client, args=(socket_client, client_address, numero)) # cria uma thread para cada cliente conectado
        client_thread.start()   # iniciando a thread do client
