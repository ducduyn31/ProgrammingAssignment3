from collections import defaultdict

from utilities import Singleton


class SimpleMemCache(metaclass=Singleton):
    def __init__(self):
        self.room_users = defaultdict(list)
        self.users_list = []

    def get_user_by_id(self, user_id):
        for user in self.users_list:
            if user.user_id == user_id:
                return user
        return None

    def add_user(self, user) -> bool:
        if user in self.users_list:
            return False
        self.users_list.append(user)
        return True

    def user_exists(self, user_id) -> bool:
        for user in self.users_list:
            if user.user_id == user_id:
                return True
        return False
