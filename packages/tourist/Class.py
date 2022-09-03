import numpy as np
import pandas as pd
from packages.common.clear import clear_console
from packages.tourist.ga import ga
from packages.common.input import inp, key_try_except
from packages.tourist.functions import start_finder, gimmedates
from time import sleep, time, gmtime, localtime, mktime, strftime
from calendar import timegm
from datetime import date
from packages.driver.functions import request_transition
from packages.landlord.functions import request_residence
from packages.utils.updates import update_services
from packages.Bank.transaction import deposit

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
        return None

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)
        # --------------------------------------------------------------------------------------

    def deposit(self)->bool:
        """deposit is used to deposit money in tourist account.

        Returns:
            bool: True or False for completion of transaction.
        """
        amount = inp("How much do you want to deposit? ", "Enter a valid number: ", convert = int, key = lambda el: el>0)
        try:
            deposit(self['national_id'], amount)
            print("\t\t! Done !\n\n")
            sleep(2)
            return True
        except:
            print("\t\t! Faild !\n\n")
            sleep(2)
            return False

    def show_services(self):
        services = pd.read_csv('./data/services.csv', dtype=str)
        active_services = pd.read_csv('./data/active_services.csv')
        all_services = pd.concat([services, active_services], axis = 0, ignore_index=True)
        fit_all_service = all_services.loc[(all_services["tourist_nid"] == self['national_id'])]
        print("All the services you have used so far:")

        for _, row in fit_all_service.iterrows():
                print(f'{row.type}:({row.service}) in date: {strftime("%Y-%m-%d %H:%M", localtime(int(row.start)))} till {strftime("%Y-%m-%d %H:%M", localtime(int(row.end)))}.')
                print("........................................................................")
        inp('Enter "ok" to continue.', 'Enter "ok": ', convert = lambda el: el.lower(), key = lambda el: el == 'ok')


        # --------------------------------------------------------------------------------------
    def score(self, show = True)-> None:
        """score function starts the scoring system for done travels of a tourist.

        Args:
            show (bool, optional): The boolean value to ask a confirming question first. Defaults to True.
        """
        df = pd.read_csv('./data/services.csv', dtype=str)
        df_chek = df[df['tourist_nid'] == self['national_id']]
        if df_chek.isna().sum().sum():
            if not show:
                flag = inp("Do you want to score your previous services (y/n)? ", "(y/n): ", key = lambda el: el.upper() in ['Y', 'N']).upper() == 'Y'
            else: flag = True
            if flag:
                    print("\n  **  Type cancel to terminate scoring, type none to don't give score to a service.\n")
                    for i, row in df.iterrows():
                        if bool(df.loc[[i]].isna().sum().sum()) and row.tourist_nid == self['national_id']:
                            price = '{:,.2f}'.format(int(row.price))
                            start = strftime('%Y-%m-%d %H:%M', localtime(int(row.start)))
                            end = strftime('%Y-%m-%d %H:%M', localtime(int(row.end)))
                            if row.type == 'ride':
                                print(f'\nYou used transition service with {row.service} from {row.starting_city} to {row.destination_city} in {start} and it costed you {price} Tomans.\n')
                            else:
                                print(f'\nYou stayed in {row.service} in {row.starting_city} from {start} to {end} and it costed you {price} Tomans.\n')
                            new_score = inp('From 1 to 5, score this service: ', 'Enter a valid amount: ', key = lambda el: el.upper() in ['1', '2', '3', '4', '5', 'NONE', 'CANCEL']).upper()
                            if new_score == 'CANCEL':
                                break
                            elif new_score == 'NONE':
                                df.iloc[i, df.columns.get_loc('score')] = 'None'
                            else:
                                df.iloc[i, df.columns.get_loc('score')] = int(new_score)
                                if row.type == 'ride':
                                    from packages.driver.functions import score
                                else:
                                    from packages.landlord.functions import score
                                score(row.service_id, int(new_score))
                                # call score function based on type and pass service id and new score to it
                    df.to_csv('./data/services.csv', index = False)
                    print('\n\n\t\tDone!!\n\n')
        else:
            if show:
                print('\n\nThere is not any un-scored services in your profile. :)\n\n')
        sleep(2)
        clear_console()

        # --------------------------------------------------------------------------------------
    def travel(self):
        """travel method is used to make a travel service for a tourist.

        The travel function uses Genetic Algorithm to specify the route of the travel. Then it automatically finds services and reserve them for a tourist.

        Returns:
            None
        """
        from packages.utils.points import load_cities_data
        cities, distances = load_cities_data()
        print()
        print(*[f'{el}: {index + 1}' for index, el in enumerate(cities)], sep=" -=- ", end='\n\n')
        start = start_finder(self['address'], cities)
        trip = inp(
            'Please enter your visiting cities as a sequence (e.g. 1 2 3): ',
            f'Please enter a valid sequence of numbers between 1 and {len(cities)}, also dont enter your start city: ',
            convert=lambda Ls: [int(el) for el in Ls.split()],
            key=lambda L: True if sum([1 if el != start and el > 0 and el <= len(cities) else 0 for el in L]) == len(L) else False
        )
        trip, best_distance = ga(cities, distances, trip, start)
        clear_console(False)
        print("\t\t-=-=-= The best route to your travel is as below =-=-=-\n\n")
        print('\t\t', *trip, '', sep=' - ')
        sleep(7)
        clear_console()
        no_passengers = inp(
            'How many passenger are you (or you can type "cancel")? ', 'Enter a positive number: ',
            key=lambda el: el.isnumeric() and int(el) > 0 or el == 'cancel'
        )
        if no_passengers == 'cancel': return False
        else: no_passengers = int(no_passengers)

        new_services = pd.DataFrame(
                columns=['id','tourist_nid','service_id','type','service','starting_city','destination_city','start','end','price']
                )
        start_dates = np.array([])
        destination_dates = np.array([])
        total_price = 0



        if inp("Do you have your own car (y/n)? ", "y/n: ", convert = lambda el: el.upper(), key = lambda el: el in ['Y', 'N']) == "N":
            i = 0
            while i < len(trip):
                if i < len(trip) - 1:
                    status, start_dates, destination_dates, new_services, total_price = request_transition(
                        self['national_id'], trip[i], trip[i+1], no_passengers, start_dates, destination_dates, new_services,  total_price
                    )
                    if status == 400: return False
                if i > 0:
                    if i ==  len(trip) - 1:
                        start_date = gimmedates(trip[i], destination_dates) # date of Leaving start_city
                        start_dates = np.append(start_dates, start_date)

                    status, new_services, total_price = request_residence(
                        self['national_id'], trip[i], destination_dates[i-1], start_dates[i], no_passengers, total_price, new_services
                    )
                    if status == 400 : return False
                    if status == 300: continue
                i += 1
        else:
            start_dates = np.append(start_dates, mktime(localtime())) # Consider travels from start just now
            i = 1
            while i < len(trip):
                destination_date = gimmedates(trip[i], destination_dates, 'arriving to')
                start_date = gimmedates(trip[i], destination_dates)
                status, new_services, total_price = request_residence(
                    self['national_id'], trip[i], destination_date, start_date, no_passengers, total_price, new_services
                )
                if status == 400 : return False
                if status == 300 : continue
                start_dates = np.append(start_dates, start_date)
                destination_dates = np.append(destination_dates, destination_date)
                i += 1

                
        update_services(new_services)
        clear_console()
        print('!!! You registerd for a travel !!!')
        print(f'\n\t\t Total cost was:  {total_price} \n')
        print(f'\t You will travel from:')
        print(f'\t\t\t{trip[0]} to {trip[-1]}')
        print(f'\nTotal Distance would be:')
        print(f'\t\t\t** {best_distance} **')




