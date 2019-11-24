def on_exit(event):
    user = event.get_user()
    room = event.get_room()

    # There is only 1 chat room now so exiting room also means terminating session
    user.terminate_session()
    user.quit_room(room)

    room.broadcast('{} quits!'.format(user.name))
