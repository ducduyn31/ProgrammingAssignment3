from events.room_event import RoomEvent, UserEvent


class UserMessageEvent(RoomEvent, UserEvent):

    def __init__(self, room, user, message):
        RoomEvent.__init__(self, room)
        UserEvent.__init__(self, user)
        self._message = message

    def get_raw_message(self):
        return self._message

    def get_message(self):
        return self._message.get_message()

    def get_sender(self):
        return self.get_user()

    def cancel(self):
        pass
