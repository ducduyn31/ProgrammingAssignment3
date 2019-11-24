import uuid
from socket import SHUT_RDWR

from chat_user import ConnectionUser
from event_manager import EventManager
from events import RoomJoinEvent
from message import Message
from storage import SimpleMemCache
from utilities import random_name


def on_handshake(event):
    sock = event.get_initiator()
    message = sock.recv(16)
    connecting_session = uuid.UUID(bytes=message[:16])
    storage = SimpleMemCache()

    # Invalid Handshake
    if len(message) != 16:
        sock.send(Message('SERVER', 'Invalid handshake!').serialize())
        sock.shutdown(SHUT_RDWR)
        sock.close()
        return

    connecting_user = None

    if connecting_session == uuid.UUID(int=0):
        session_id = uuid.uuid4()
        connecting_user = ConnectionUser(sock, session_id, random_name())
        storage.add_user(connecting_user)
        sock.send(Message('SERVER', '{}.{}'.format(session_id.int, connecting_user.name)).serialize())

    elif storage.user_exists(connecting_session):
        connecting_user = storage.get_user_by_id(connecting_session)
        sock.send(Message('SERVER', '{}.{}'.format(connecting_session.int, connecting_user.name)).serialize())

    EventManager().emit(RoomJoinEvent(event.get_room(), connecting_user))
