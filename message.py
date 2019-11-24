import struct


class Message:
    def __init__(self, usrname='', msg='', is_command=False, raw=None):
        if raw is None:
            self.u_name_l = len(usrname)
            self.message_l = len(msg)
            self.username = usrname
            self.message = msg
            self._is_command = is_command
        else:
            a, b, c, d, e = self._extract_raw(raw)
            self.u_name_l = a
            self.message_l = b
            self._is_command = c
            self.username = d
            self.message = e

    def set_username(self, new_username):
        self.u_name_l = len(new_username)
        self.username = new_username

    def get_username(self):
        return self.username

    def is_command(self):
        return self._is_command

    def set_message(self, new_message):
        self.message_l = len(new_message)
        self.message = new_message

    def get_message(self):
        return self.message

    @staticmethod
    def _extract_raw(raw_message):
        if len(raw_message) < 7:
            return 0, 0, False, None, None

        unl = raw_message[:2]
        ml = raw_message[2:6]
        command_flag = raw_message[6:7]

        len_username = int.from_bytes(unl, 'big')
        len_message = int.from_bytes(ml, 'big')

        uname = raw_message[7:(7 + len_username)]
        mess = raw_message[(7 + len_username):]

        return len_username, len_message, bool(command_flag[0]), uname.decode('utf-8'), mess.decode('utf-8')

    def serialize(self):
        u_name_l_byte = struct.pack('>H', self.u_name_l)
        message_l_byte = struct.pack('>I', self.message_l)
        is_command = struct.pack('>?', self._is_command)
        username_byte = str.encode(self.username)
        message_byte = str.encode(self.message)
        return u_name_l_byte + message_l_byte + is_command + username_byte + message_byte
