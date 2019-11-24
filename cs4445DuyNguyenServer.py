import uuid
from socket import *
from threading import Thread

from command import Command
from command_manager import CommandManager
from event_manager import EventManager
from events import HandshakingEvent, RoomJoinEvent, UserMessageEvent, RoomExitEvent, UserCommandEvent
from events_handler import on_handshake, on_room_join, on_messaging, on_exit
from events_handler.commands_handler import list_command, help_command, nick_command, private_message_command
from message import Message


class ChatRoom:

    def __init__(self, max_users, host='', port=3000, room_id=uuid.UUID(int=0)):
        self.serve_sock = socket(AF_INET, SOCK_STREAM)
        self._host = host
        self._port = port
        self.serving_address = (host, port)

        self.connecting_users = []
        self.max_users = max_users

        self.connection_threads = []

        self.room_id = room_id

    def __del__(self):
        for user in self.connecting_users:
            user.terminate_session()
            user.quit_room(self)
        for thrd in self.connection_threads:
            thrd.join()

    def serve_one(self, sock):
        EventManager().emit(HandshakingEvent(self, sock))

        user = None

        for u in self.connecting_users:
            if u.get_socket() == sock:
                user = u

        while True:
            message = sock.recv(1024)
            if len(message) == 0:
                EventManager().emit(RoomExitEvent(self, user))
                break
            else:
                m = Message(raw=message)
                if m.is_command():
                    EventManager().emit(UserCommandEvent(self, user, Command(raw=message)))
                else:
                    EventManager().emit(UserMessageEvent(self, user, m))

    def serving(self):
        try:
            print('[SYSTEM] Serving on {}:{}'.format(self._host, self._port))
            self.serve_sock.bind(self.serving_address)
            self.serve_sock.listen(self.max_users)
            while True:
                client_sock, client_addr = self.serve_sock.accept()
                connection_thread = Thread(target=self.serve_one, args=[client_sock])
                connection_thread.start()
                self.connection_threads.append(connection_thread)
        except KeyboardInterrupt:
            print('Server stopping...')
            self.__del__()

    def broadcast(self, message):
        for user in self.connecting_users:
            user.send_message('SERVER', message)


def register_commands():
    CommandManager().register_command('help', help_command, ['h', '?'], 'Show commands table. \nUsage: /help')
    CommandManager().register_command('list', list_command, ['l'], 'List all players in room. \nUsage: /list')
    CommandManager().register_command('nick', nick_command, ['n'], 'Change your username. \nUsage: /nick <new_name>')
    CommandManager().register_command('msg', private_message_command, ['m'],
                                      'Message to an user privately. \nUsage: /msg <username> <message>')


def register_events():
    EventManager().register_handler(HandshakingEvent, on_handshake)
    EventManager().register_handler(RoomJoinEvent, on_room_join)
    EventManager().register_handler(UserMessageEvent, on_messaging)
    EventManager().register_handler(RoomExitEvent, on_exit)


if __name__ == '__main__':
    register_events()
    register_commands()
    room = ChatRoom(10, port=3000)
    room.serving()
