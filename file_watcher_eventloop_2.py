# Для тестирования запускаем программу,
# в новой вкладке терминала делаем запрос к серверу
# nc localhost 5001
# повторяем эту процедуру из другого терминала
# убеждаемся, что код умеет принимать соединения и общаться
# с несколькими клиентами одновременно


import socket
from select import select


def run_server(port=5001, backlog=5):
    """
    :param port: порт сервера
    :param backlog: максимальное кол-во клиентов,
    которые могут подключаться одновременно
    :return:
    """
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', port))
    server_socket.listen(backlog)
    print('Server socket created...')


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print(f'Connection established with {addr}...')
    read_queue.append(client_socket)
    print('\n\n', len(read_queue), read_queue, '\n\n')


def process_message(client_socket):
    request = client_socket.recv(4096)
    print(f'\nFrom client: {client_socket}\nMessage received: {request.decode()}')

    if request:
        response = f'SASAT LEZHAT\n\n'.encode()
        client_socket.send(response)
    else:
        print(f'Closing the connection with client {client_socket}...')
        read_queue.remove(client_socket)
        client_socket.close()
        print('\n\n', len(read_queue), read_queue, '\n\n')


def event_loop():
    while True:
        # В UNIX все процессы, девайсы и вообще всё является файлами
        # Сокет -- файл с точки зрения ОС
        # Это позволяет использовать системную библиотеку select,
        # которая poll'ит изменения файлов.
        # Функция select() принимает на вход минимум 3 списка
        # rlist -- файлы, которые ждут чтения
        # wlist -- файлы, которые ждут записи
        # xlist -- файлы, которые ждут ошибок
        ready_for_read, _, _ = select(read_queue, [], [])
        print('\n', len(read_queue), read_queue)
        print(len(ready_for_read), ready_for_read, '\n')
        for sock in ready_for_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                process_message(sock)


def main():
    global read_queue
    read_queue = list()
    run_server()
    read_queue.append(server_socket)
    event_loop()


if __name__ == '__main__':
    main()
