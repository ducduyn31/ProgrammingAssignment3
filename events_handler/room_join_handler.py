def on_room_join(event):
    event.get_user().add_room(event.get_room())
    event.get_room().broadcast('{} has joined!'.format(event.get_user().name))
