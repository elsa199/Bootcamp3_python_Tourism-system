import numpy as np
import pandas as pd
from time import mktime, localtime, sleep
from packages.common.clear import clear_console
from packages.tourist.functions import  gimmedates
from packages.common.input import inp
from packages.Bank.transaction import withdraw, deposit
from packages.common.calculation import calc_arrive_date

def request_transition(tourist_nid: str, start_city: str, destination_city: str, no_passengers: int, start_dates: np.ndarray, destination_dates: np.ndarray, new_services: pd.DataFrame,  total_price: float) -> list:
    """request_transition requests a transition based on start and destination city and number of passengers.

    Args:
        tourist_nid (str): The tourist id
        start_city (str): The starting city of transition
        destination_city (str): The destination city of transition
        no_passengers (int): The number of passengers
        start_dates (np.ndarray): An array of start times in seconds format to add the new start date
        destination_dates (np.ndarray): An array of destination times in seconds format to add the new destination date
        new_services (pd.DataFrame): A dataframe of new services that tourist picked till now
        total_price (float): The total charged price

    Returns:
        list: In case the tourist completes the request, the function returns a list containing 200 status, updated start times, updated destination times, updated new services, and total_price.
        In case the tourist cancels the request it returns status 400 and the rest of the list.
    """
    while True:
        print(f"\n*** Search for transition services for you from {start_city} to {destination_city}.***\n")
        start_date = gimmedates(start_city, destination_dates) # date of Leaving start_city
        status, service_id, service_type, destination_date, price = vehicle_search(tourist_nid, start_city, destination_city, no_passengers, start_date)
        if status == 300:
            clear_console()
            continue
        elif status == 400:
            clear_console()
            return [400, start_date, destination_date, new_service, total_price]
        elif status == 200:
            start_dates = np.append(start_dates, start_date)
            destination_dates = np.append(destination_dates, destination_date)
            # Write services to active service file
            new_service = pd.DataFrame(
                [['id',tourist_nid,service_id,service_type,'ride',start_city, destination_city,start_date,destination_date,price]],
                columns=['id','tourist_nid','service_id','type','service','starting_city','destination_city','start','end','price']
                )
            new_services = pd.concat([new_services, new_service], axis = 0, ignore_index=True)
            total_price += price
            clear_console()
            return [200, start_dates, destination_dates, new_services, total_price]
            


def vehicle_search(tourist_nid:str, start_city:str, end_city:int,  number: int, s_datatime: float) -> list:
    """vehicle_search searchs for a transition service with specified conditions and reserve the fitted service which tourist picks.

    This function also requests the responssible Intercity_services for reservation and it does the bank transaction related to tourist.

    Args:
        tourist_nid (str): The tourist id
        start_city (str): The starting city of transition
        end_city (int): The destination city of transition
        number (int): The number of passengers
        s_datatime (float): Travel start time in seconds format

    Returns:
        list: In case the tourist completes the request, the function returns a list containing 200 status, id of picked service, type of the service, the time which tourist arrives to the destination, and price of service.
        In case the tourist cancels the request it returns status 400 and the rest of the list.
    """

    vehicles = pd.read_csv('./data/vehicles.csv', dtype=str)
    vehicles.drop(vehicles[vehicles['capacity'] == '0'].index, inplace=True)
    vehicles.drop(vehicles[[float(el) <= mktime(localtime()) for el in vehicles.start_datatime]].index, inplace=True)
    vehicles.to_csv('./data/vehicles.csv', index=False)
    print(vehicles.starting_city)
    
    local_s_datatime = localtime(s_datatime)
    
    fit_vehicles = vehicles[
        ([int(el) >= number  for el in vehicles['capacity']]) &
        (vehicles['starting_city'] == start_city) &
        (vehicles['destination_city'] == end_city) &
        ([localtime(float(el)).tm_year == local_s_datatime.tm_year and localtime(float(el)).tm_mon == local_s_datatime.tm_mon and localtime(float(el)).tm_mday == local_s_datatime.tm_mday for el in vehicles.start_datatime])
        ]
    
    if fit_vehicles.size:
        ids = []
        for _, row in fit_vehicles.iterrows():
            ids.append(row.id)
            print(f'{row.type} with {row.capacity} people capacity, {row.rent} Tomans rent per person, {row.num_score} scored this vegicle and its score is {row.score}.')
            print(f'\n*** code: {row.id} ***\n')
        id = inp(
            "- To reserve a vehivle type its code\n- To change the dates you entered type 'change'\n- To cancel the vehicle type 'cancel'\n(code/cancel/change): ",
            "Invalid input. Enter again: ",
            key = lambda el: el in ids or el.lower() == 'cancel' or el.lower() == 'change'
        )
        if id.lower() == 'change': return [300, 0, 0, 0, 0]
        elif id.lower() == 'cancel': return [400, 0, 0, 0, 0]
        else:
            confirm = inp(
                f"Are you sure you want this vehicle for a total {float(row.rent) * number} Tomans? \n(y/cancel/change): ",
                "Invalid input. Enter again: ",
                convert = lambda el: el.lower(),
                key = lambda el: el in ['y', 'cancel', 'change']
            )
            if confirm == 'change': return [300, 0, 0, 0, 0]
            elif confirm == 'cancel': return [400, 0, 0, 0, 0]
            price = float(fit_vehicles[fit_vehicles.id == id].rent[0]) * number
            fit_moving_service_id = fit_vehicles[fit_vehicles.id == id].moving_service_id[0]
        
        moving_services = pd.read_csv('./data/drivers.csv', dtype=str)
        fit_moving_service_data = moving_services[moving_services.national_id == fit_moving_service_id]

        from packages.driver.moving_service import Intercity_services
        fit_moving_service = Intercity_services(fit_moving_service_data.username[0], fit_moving_service_data.password[0], fit_moving_service_data.first_name[0],
                                           fit_moving_service_data.last_name[0], fit_moving_service_data.national_id[0], fit_moving_service_data.tel[0])
        while True:
            try:
                print(id)
                print('num', number, type(number))
                withdraw(tourist_nid, price)
                fit_moving_service.reservation(id, number)
                break
            except:
                print('\n# # You dont have enough money. # #')
                what_to_do = inp(
                    "- To deposit more money and try again: deposit\n- To change the dates you entered: change\n- To cancel the travel: cancel\n(deposit/cancel/change): ",
                    "Invalid input. Enter again: ",
                    convert = lambda el: el.lower(),
                    key = lambda el: el in ['deposit', 'cancel', 'change']
                )
                if what_to_do == 'deposit':
                    amount = inp("How much do you want to deposit? ", "Enter a valid number: ", convert = int, key = lambda el: el>0)
                    try:
                        deposit(tourist_nid, amount)
                    except:
                        print("FAILD!!! Automatice canceling process.")
                        sleep(3)
                        return [400, 0, 0, 0]
                if what_to_do == 'change': return [300, 0, 0, 0, 0]
                elif what_to_do == 'cancel': return [400, 0, 0, 0, 0]

        destination_date = calc_arrive_date(
            fit_vehicles[fit_vehicles.id == id].starting_city[0],
            fit_vehicles[fit_vehicles.id == id].destination_city[0],
            fit_vehicles[fit_vehicles.id == id].start_datatime[0],
            fit_vehicles[fit_vehicles.id == id].avg_speed[0]
        )
        return [200, id, fit_vehicles[fit_vehicles.id == id].type[0], destination_date, price]
    else:
        id = inp(
            "\n***There wasn't any fit service for you***\n- To change the dates you entered type 'change'\n- To cancel the travel type 'cancel'\n- To skip this step enter 'skip'",
            "Invalid input. Enter again: ",
            key = lambda el: el.lower() in ['cancel', 'change', 'skip']
        )
        if id.lower() == 'change': return [300, 0, 0, 0, 0]
        elif id.lower() == 'cancel': return [400, 0, 0, 0, 0]
        elif id.lower() == 'skip': return [500, 0, 0, 0, 0]

def score(vehicle_id, new_score):
    # Alter the vehicles file and add or average score
    vehicles = pd.read_csv('./data/vehicles.csv', dtype=str)
    # i = residences[residences.id == residence_id].index
    i = vehicles[vehicles.moving_service_id == vehicle_id].index

    if (i.size)!= 0:
        no_scores = int(vehicles.iloc[i[0], vehicles.columns.get_loc('no_scores')])
        score = vehicles.iloc[i[0], vehicles.columns.get_loc('score')]
        if score == 'None': score = 0
        else: score = int(score)

        vehicles.iloc[i[0], vehicles.columns.get_loc('no_scores')] = no_scores + 1
        vehicles.iloc[i[0], vehicles.columns.get_loc('score')] = score + (new_score/(no_scores+1))


        vehicles.to_csv('./data/vehicles.csv', index=False)
    return