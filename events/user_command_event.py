from events.room_event import RoomEvent, UserEvent


class UserCommandEvent(RoomEvent, UserEvent):

    def __init__(self, room, user, command):
        RoomEvent.__init__(self, room)
        UserEvent.__init__(self, user)
        self._command = command

    def get_command(self):
        return self._command

    def cancel(self):
        pass
