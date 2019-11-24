from socket import SHUT_RDWR

from events.room_event import RoomEvent


class HandshakingEvent(RoomEvent):

    def __init__(self, room_instance, client_socket):
        super().__init__(room_instance)
        self.initiator = client_socket

    def get_initiator(self):
        return self.initiator

    def cancel(self):
        self.initiator.shutdown(SHUT_RDWR)
        self.initiator.close()
