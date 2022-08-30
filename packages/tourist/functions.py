from packages.common.input import inp, key_try_except
import numpy as np
from time import localtime, mktime
from datetime import date

def start_finder(address: str, cities: list) -> str:
    """start_finder prompts the tourist to find out the start city of a travel.

    Args:
        address (str): The home address entered by tourist when registered
        cities (list): A list of database cities

    Returns:
        str: The start city
    """
    if inp(f'Are you in your home town, {address} (y/n)?', '(y/n)? ', key=lambda el: el.upper() in ['Y', 'N']).upper()  == 'N':
            start = inp(
                "Please enter city code in which you are: ",
                f"Please enter a valid number between 1 and {len(cities)}: ",
                convert=int,
                key=lambda el: el > 0 and el <= len(cities)
        )
    else:
        start = cities.index(address) + 1
    return start


def gimmedates(trip:list, check_dates:list = [], state: str = 'leaving', check = True)-> list:
    """gimmedates prompts a tourist for a set of dates in 'YYYY MM DD hh:mm' format.

    Args:
        trip (list | str): A list of cities or just one city in string format
        check_dates (list, optional): The list of pre dates that the new dates are checked with them. Defaults to [].
        state (str, optional): state of tourist in respect of mentioned cities. Defaults to 'leaving'.
        check (bool, optional): Do you wnat to check entered date and time at all? Defaults to True.

    Returns:
        list | int: A list of givven dates or just one entered date, both in seconds format.
    """
    if not isinstance(trip, list): trip = [trip]
    if isinstance(check_dates, list): check_dates = np.array(check_dates)
    if check:
        dates = np.array([mktime(localtime())])
        if bool(check_dates.size):
            dates = np.append(dates, check_dates)
            l = len(check_dates)
        else: l = 0
    else:
        dates = np.array([])
        l = -1
    for city in trip:
        user_date = mktime(inp(
            f"Please enter when you're {state} {city} (YYYY MM DD hh:mm)? ", 'VALID and in format like "YYYY MM DD hh:mm" and not in the past: ',
            convert=lambda s: tuple([*[int(el) for el in s.split()[:-1]] + [int(el)
                                    for el in s.split()[-1].split(':')], 0, 0, 0, 0 if localtime()[1] < 7 else 1]),
            key=[
                    lambda el: np.all(mktime(el) > dates) and el[3] < 24 and el[4] < 60,
                    lambda el: key_try_except(el, lambda el2: date(el2[0], el2[1], el2[2]))
                ]
        ))
        dates = np.append(dates, user_date)
    if len(trip) == 1: return dates[-1]
    return dates[l + 1:]