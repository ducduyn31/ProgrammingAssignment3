import json
from random import randint

import requests


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def random_name():
    try:
        with open('assets/names.json') as names_file:
            data = json.load(names_file)
            return data[randint(0, 500)]['name']

    except FileNotFoundError:
        amount, region = 500, 'United States'
        r = requests.get('https://uinames.com/api/?amount={}&region={}'.format(amount, region))
        print('requesting random names')

        if r.status_code == 200:
            f = open('assets/names.json', 'w')
            f.write(r.text)
            f.close()

            return random_name()
