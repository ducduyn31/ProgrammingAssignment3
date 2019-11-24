def on_messaging(event):
    room_users = event.get_room().connecting_users
    for user in room_users:
        user.send_message(event.get_sender().name, event.get_message())