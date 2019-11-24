from command_manager import CommandManager
from command import Command


def help_command(label, args, sender, room):
    command_list = {}
    for command in CommandManager().command_map:
        _, description, alias = CommandManager().command_map[command]
        if alias is None:
            if command in command_list:
                command_list[command][0] = description
            else:
                command_list[command] = [description, []]
        else:
            if alias not in command_list:
                command_list[alias] = ['', []]
            command_list[alias][1].append(command)

    msg = 'Commands Table\n'
    i = 1
    for command in command_list:
        ames = '{}. /{} : \n\t{} \n\t(alias: {})\n\n'.format(i, command, command_list[command][0],
                                                             ', '.join(command_list[command][1]))
        msg += ames
        i += 1

    sender.send_message('SERVER', msg)


def list_command(label, args, sender, room):
    user_name_list = [u.name for u in room.connecting_users]
    message = '{} users: {}'.format(len(user_name_list), ', '.join(user_name_list))

    sender.send_message('SERVER', message)


def nick_command(label, args, sender, room):
    new_name = args[0]

    if not len(new_name) > 3:
        sender.send_message('SERVER', 'New name must be at least 3 characters long')
    else:
        room.broadcast('{} changes its name to {}'.format(sender.name, new_name))
        sender.set_name(new_name)


def private_message_command(label, args, sender, room):
    receiver = None
    msg = ' '.join(args[1:])
    users = room.connecting_users
    for user in users:
        if user.name == args[0]:
            receiver = user
            break

    if receiver is None:
        sender.send_message('SERVER', 'User does not exists')
    else:
        receiver.send_command(Command(sender.name, 'private {}'.format(msg)))
