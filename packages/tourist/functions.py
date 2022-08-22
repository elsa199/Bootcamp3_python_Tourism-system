from packages.common.input import inp, key_try_except
from packages.utils.points import update_cities_data
import numpy as np
from time import time, gmtime, localtime, mktime, strftime
from calendar import timegm
from datetime import date

def start_finder(address, cities, distances):
    flag = True
    try:
        if inp(f'Are you in your home town, {address} (y/n)?', '(y/n)? ', key=lambda el: el.upper() in ['Y', 'N']).upper()  == 'N':
            if inp('Do we have your current city in the list (y/n)?', '(y/n)? ', key=lambda el: el.upper() in ['Y', 'N']).upper() == 'Y':
                start = inp(
                    "First please enter city code in which you are: ",
                    f"Please enter a valid number between 1 and {len(cities)}: ",
                    convert=int,
                    key=lambda el: el > 0 and el <= len(cities)
            )
            else:
                flag = False
                raise Exception()
        else: raise Exception()
    except Exception:
        try:
            if flag:
                search = address
                start = cities.index(search) + 1
            else:
                raise Exception()
        except Exception:
            print("\n       ----> Not recognized home city <----\n")
            cities, distances = update_cities_data(cities, distances, address)
    return [start, cities, distances]


def gimmedates(trip):
    dates = np.array([mktime(localtime())])
    for city in trip:
        user_date = mktime(inp(
            f"Please enter when you're leaving {city} (YYYY MM DD hh:mm)? ", 'VALID and in format like "YYYY MM DD hh:mm" and not in the past: ',
            convert=lambda s: tuple([*[int(el) for el in s.split()[:-1]] + [int(el)
                                    for el in s.split()[-1].split(':')], 0, 0, 0, 1]),
            key=[
                    lambda el: np.all(mktime(el) > dates) and el[3] < 24 and el[4] < 60,
                    lambda el: key_try_except(el, lambda el2: date(el2[0], el2[1], el2[2]))
                ]
        ))
        dates = np.append(dates, user_date)
    return dates[1:]