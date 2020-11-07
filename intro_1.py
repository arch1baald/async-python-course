# Для тестирования запускаем программу,
# в новой вкладке терминала делаем запрос к серверу
# nc localhost 5001
# повторяем эту процедуру из другого терминала
# убеждаемся, что код умеет принимать соединения с несколькими
# клиентами, но отвечает на сообщения только одному из них
# до тех пор, пока другой не прервет соединение


import socket


def main():
    # Запускаем сервер на порту
    port = 5001
    # Максимальное кол-во одновременных соединений
    backlog = 2

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', port))
    server_socket.listen(backlog)

    # Принимаем запросы на соединение с клиентами.
    while True:
        # Без этого цикла while только 1 клиент сможет присоединиться
        # и пообщаться с сервером. Когда соединение будет разорвано,
        # программа остановится и сервер автоматически ляжет.
        print('Waiting for a new client...')
        client_socket, addr = server_socket.accept()
        print(f'Connection established with {addr}...')

        while True:
            # Без этого цикла while клиент сможет отправить только 1 сообщение,
            # потому что после цикла закрывается client_socket.
            print(f'Waiting for a new message from client {addr}...')
            request = client_socket.recv(4096)
            print(f'\nFrom client: {addr}\nMessage received: {request.decode()}\n')

            if not request:
                print(f'request: {request}')
                break
            else:
                response = f'From client: {addr}\nMessage received: {request.decode()}\n'.encode()
                client_socket.send(response)

        print(f'Closing connection with client {addr}...')
        client_socket.close()


if __name__ == '__main__':
    main()
