import sys
import uuid
from socket import *
from threading import Thread

from command import Command
from message import Message

username = ''
uid = uuid.UUID(int=0)


def handshake(server_sock, sess):
    global uid, username

    server_sock.send(sess.bytes)
    recv = server_sock.recv(1024)
    result = Message(raw=recv)
    msg = result.get_message().split('.')

    username = msg[1]
    uid = uuid.UUID(int=int(msg[0]))

    print('[{}] Welcome {}! Your id is {}'.format(result.get_username(), username, uid))


def listen_to_server(server_sock):
    global username
    while True:
        try:
            inc_msg_raw = server_sock.recv(1024)
            inc_msg = Message(raw=inc_msg_raw)
            if inc_msg.is_command():
                cmd = Command(raw=inc_msg_raw)
                label = cmd.get_label()

                if label == 'name':
                    username = cmd.get_arguments()[0]
                elif label == 'private':
                    print('[{}] messaged you: {}'.format(cmd.get_username(), ' '.join(cmd.get_arguments())))
            else:
                print('[{}] {}'.format(inc_msg.get_username(), inc_msg.get_message()))
        except error:
            print('Goodbye {}'.format(username))
            break


def handling_message(sending_socket):
    entered = input('>')

    if entered.startswith('/'):
        sending_socket.send(Message(usrname=username, msg=entered, is_command=True).serialize())
        return True
    else:
        sending_socket.send(Message(usrname=username, msg=entered, is_command=False).serialize())
        return True


if __name__ == '__main__':

    port = 3000
    session = uuid.UUID(int=0)
    if len(sys.argv) >= 2:
        port = int(sys.argv[1]) if sys.argv[1] is not None else 3000
    if len(sys.argv) >= 3:
        session = uuid.UUID(int=sys.argv[2]) if sys.argv[2] is not None else uuid.UUID(int=0)

    with socket(AF_INET, SOCK_STREAM) as serverSocket:
        try:
            serverSocket.connect(('127.0.0.1', port))
            handshake(serverSocket, session)

            listen_in_bg = Thread(target=listen_to_server, args=[serverSocket])
            listen_in_bg.start()

            while True:
                if not handling_message(serverSocket):
                    break
        except KeyboardInterrupt:
            serverSocket.shutdown(SHUT_RDWR)
            serverSocket.close()
