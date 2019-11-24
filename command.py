from message import Message


class Command(Message):

    def __init__(self, usrname='', msg='', is_command=True, raw=None, prefix='/'):
        super().__init__(usrname, msg, is_command, raw)
        if not self.is_command():
            raise Exception('Not Command')
        self.COMMAND_PREFIX = prefix

    def get_label(self):
        label = self.get_message().split()[0]
        if self.get_message().startswith(self.COMMAND_PREFIX):
            label = label[len(self.COMMAND_PREFIX):]
        return label

    def get_arguments(self):
        return self.get_message().split()[1:] if len(self.get_message().split()) > 1 else []