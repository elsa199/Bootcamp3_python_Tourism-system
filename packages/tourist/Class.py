import numpy as np
import pandas as pd
from packages.common.clear import clear_console
from packages.tourist.ga import ga
from packages.common.input import inp, key_try_except
from packages.tourist.functions import start_finder, gimmedates
from time import sleep, time, gmtime, localtime, mktime, strftime
from calendar import timegm
from datetime import date
from packages.driver.Driver import search


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
    def score(self, flag = True):
        show = True
        if not flag:
            show = False
            flag =  inp("Do you want to score your previous services (y/n)? ", "y/n: ", key = lambda el: el.upper() in ['Y', 'N']).upper() == 'Y'
        if flag:
            df = pd.read_csv('./data/travels.csv', dtype=str)
            if df.isna().sum().sum():
                print("\n  **  Type cancel to terminate scoring, type none to don't give score to a service.\n")
                for i, row in df.iterrows():
                    if bool(df.loc[[i]].isna().sum().sum()) and row.tourist_nid == self['national_id']:
                        price = '{:,.2f}'.format(int(row.price))
                        start = strftime('%Y-%m-%d %H:%M', localtime(int(row.start)))
                        end = strftime('%Y-%m-%d %H:%M', localtime(int(row.end)))
                        print(f'Your {row.type} service from {row.starting_city} to {row.destination_city} in {start} to {end} costed you {price} Tomans.\n')
                        new_score = inp('From 1 to 5, score this service: ', 'Enter a valid amount: ', key = lambda el: el.upper() in ['1', '2', '3', '4', '5', 'NONE', 'CANCEL']).upper()
                        if new_score == 'CANCEL':
                            break
                        elif new_score == 'NONE':
                            df.iloc[i, df.columns.get_loc('score')] = 'None'
                        else:
                            df.iloc[i, df.columns.get_loc('score')] = int(new_score)
                            # call score function based on type and pass service id and new score to it
            else:
                if show:
                    print('\n\nThere is not any un-scored services in your profile. :)\n\n')
                    sleep(2)
            df.to_csv('./data/travels.csv', index = False)
            print('\n\n\t\tDone!!\n\n')
            sleep(2)
        clear_console()

    def travel(self):
        from packages.utils.points import load_cities_data
        cities, distances = load_cities_data()
        print('\n')
        print(*[f'{el}: {index + 1}' for index, el in enumerate(cities)], sep=" -=- ", end='\n\n')
        start, cities, distances = start_finder(self['address'], cities, distances)
        trip = inp(
            'Please enter your visiting cities as a sequence (e.g. 1 2 3): ',
            f'Please enter a valid sequence of numbers between 1 and {len(cities)}, also dont enter your start city: ',
            convert=lambda Ls: [int(el) for el in Ls.split()],
            key=lambda L: True if sum([1 if el != start and el > 0 and el <= len(cities) else 0 for el in L]) == len(L) else False
        )
        trip, best_distance = ga(cities, distances, trip, start)
        clear_console()

        while True:
            no_passengers = inp(
                'How many passenger are you (or you can type "cancel")? ', 'Enter a positive number: ',
                key=lambda el: el.isnumeric() and int(el) > 0 or el == 'cancel'
            )
            if no_passengers == 'cancel': return
            else: no_passengers = int(no_passengers)
            dates = gimmedates(trip)
            status, dates = search(trip, dates, no_passengers)
            if status: break
            
        clear_console()
        


        return trip, best_distance
