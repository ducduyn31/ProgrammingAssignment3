from events.room_event import RoomEvent, UserEvent


class RoomJoinEvent(RoomEvent, UserEvent):
    def __init__(self, room_instance, user):
        RoomEvent.__init__(self, room_instance)
        UserEvent.__init__(self, user)

    def cancel(self):
        pass
