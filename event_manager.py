from collections import defaultdict

from command_manager import CommandManager
from events.user_command_event import UserCommandEvent
from utilities import Singleton


class EventManager(metaclass=Singleton):

    def __init__(self):
        self.event_map_handler = defaultdict(list)
        self.event_map_handler[UserCommandEvent] = [CommandManager().on_command_event()]

    def emit(self, event):
        for generic_event in self.event_map_handler.copy():
            if isinstance(event, generic_event):
                for handler in self.event_map_handler[generic_event]:
                    handler(event)

    def register_handler(self, event, handler):
        self.event_map_handler[event].append(handler)
