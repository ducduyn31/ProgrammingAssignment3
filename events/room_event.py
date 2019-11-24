from abc import abstractmethod


class RoomEvent:

    def __init__(self, room_instance):
        self._room = room_instance

    def get_room(self):
        return self._room

    @abstractmethod
    def cancel(self):
        pass


class UserEvent:

    def __init__(self, user):
        self._user = user

    def get_user(self):
        return self._user
