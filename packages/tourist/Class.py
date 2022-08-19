from packages.tourist.ga import ga
from packages.common.input import inp


class Tourist():
    def __init__(
        self, username: str, password: str, national_id: str, tel: str,
        account: dict = {}, active_services: list = [], travels: list = [], **kwargs
        ):
        self['username'] = username
        self['password'] = password
        self['national_id'] = national_id
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
    def travel(self, cities, distances):
        print(*[f'{el}: {index + 1}' for index, el in enumerate(cities)], sep=" -=- ")
        start = inp(
            "First please enter city code in which you are living or leaving: ",
            f"Please enter a valid number between 1 and {len(cities)}: ",
            convert=int,
            key=lambda el: el > 0 and el <= len(cities)
        )
        trip = inp(
            'Please enter your visiting cities as a sequence (e.g. 1 2 3): ',
            f'Please enter a valid sequence of numbers between 1 and {len(cities)}, also dont enter your start city as first destination: ',
            convert=lambda Ls: [int(el) for el in Ls.split()],
            key=lambda L: L[0] != start
        )
        return ga(cities, distances, trip, start)
