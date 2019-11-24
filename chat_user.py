from socket import SHUT_RDWR

from command import Command
from message import Message


class ConnectionUser:
    def __init__(self, user_socket, user_id, user_name):
        self.sock = user_socket
        self._sock_shutdown = False
        self.name = user_name
        self.user_id = user_id
        self.rooms = []

    def add_room(self, room):
        if self not in room.connecting_users:
            room.connecting_users.append(self)
        if room not in self.rooms:
            self.rooms.append(room)

    def quit_room(self, room):
        if self in room.connecting_users:
            room.connecting_users.remove(self)
        if room in self.rooms:
            self.rooms.remove(room)

    def quit_room_by_id(self, room_id):
        for room in self.rooms:
            if room.room_id == room_id:
                self.quit_room(room)

    def send_message(self, sender, message):
        self.sock.send(Message(usrname=sender, msg=message).serialize())

    def send_command(self, command):
        self.sock.send(command.serialize())

    def get_socket(self):
        return self.sock

    def set_name(self, new_name):
        self.name = new_name
        self.send_command(Command(usrname='SERVER', msg='name {}'.format(new_name)))

    def terminate_session(self):
        if not self._sock_shutdown:
            self.sock.shutdown(SHUT_RDWR)
            self.sock.close()
            self._sock_shutdown = True
