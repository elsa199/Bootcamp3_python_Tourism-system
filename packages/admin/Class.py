from packages.common.clear import clear_console
from packages.common.input import inp
class Admin():
    def __init__(
        self, username: str, password: str, **kwargs
    ):
        self['username'] = username
        self['password'] = password
        return None

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)
        # --------------------------------------------------------------------------------------
    def add_city(self):
        from packages.utils.points import update_cities_data, load_cities_data
        cities, distances = load_cities_data()
        new_city = inp('Enter your new city: ', "Don't leave it empty: ", convert = lambda el: el.title())
        cities, distances = update_cities_data(cities, distances, new_city)
        return clear_console