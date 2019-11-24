from utilities import Singleton


class CommandManager(metaclass=Singleton):

    def __init__(self):
        self.command_map = dict()

    def on_command_event(self):
        def wrapper(event):
            sender = event.get_user()
            room = event.get_room()

            command_label = event.get_command().get_label()
            command_args = event.get_command().get_arguments()

            if command_label in self.command_map:
                self.command_map[command_label][0](command_label, command_args, sender, room)
            else:
                sender.send_message('SERVER', 'Command not found!')

        return wrapper

    def register_command(self, label, handler, alias=None, description=''):
        if label not in self.command_map:
            self.command_map[label] = (handler, description, None)

        if alias is not None:
            for ali in alias:
                if ali not in self.command_map:
                    self.command_map[ali] = (handler, description, label)
