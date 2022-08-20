import numpy as np
from packages.common.clear import clear_console
from packages.tourist.ga import ga
from packages.common.input import inp
from packages.tourist.functions import start_finder

class Tourist():
    def __init__(
        self, username: str, password: str, national_id: str, tel: str, address: str, first_name: str, last_name: str, 
        account: dict = {}, active_services: list = [], travels: list = [], **kwargs
        ):
        self['username'] = username
        self['password'] = password
        self['national_id'] = national_id
        self['address'] = address
        self['first_name'] = first_name
        self['last_name'] = last_name
        self['tel'] = tel
        self['account'] = account
        self['active_services'] = active_services
        self['travels'] = travels
        return None
    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)
        # --------------------------------------------------------------------------------------
    def travel(self):
        from data.points import cities, distances
        print('\n')
        print(*[f'{el}: {index + 1}' for index, el in enumerate(cities)], sep=" -=- ", end='\n\n')
        start, cities, distances = start_finder(self['address'], cities, distances)
        trip = inp(
            'Please enter your visiting cities as a sequence (e.g. 1 2 3): ',
            f'Please enter a valid sequence of numbers between 1 and {len(cities)}, also dont enter your start city: ',
            convert=lambda Ls: [int(el) for el in Ls.split()],
            key=lambda L: True if sum([1 if el != start else 0 for el in L]) == len(L) else False
        )
        trip, best_distance = ga(cities, distances, trip, start)
        trip = [cities[el - 1] for el in trip]

        clear_console()
        return trip, best_distance

