from time import sleep
import pandas as pd
from packages.common.clear import clear_console
from packages.common.calculation import calc_duration
from packages.common.input import inp
from packages.Bank.transaction import withdraw, deposit
import numpy as np

def request_residence(tourist_nid, city, start_date, end_date, no_passengers, total_price, new_services):
    """request_residence requests a residence based on enter and exit time, city and number of passengers.

    Args:
        tourist_nid (str): The tourist id
        city (str): The city of residence
        start_date (float): Room enter time in seconds format
        destination_date (float): Room leave time in seconds format
        no_passengers (int): The number of passengers
        total_price (float): The total charged price
        new_services (pd.DataFrame): A dataframe of new services that tourist picked till now

    Returns:
        list: In case the tourist completes the request, the function returns a list containing 200 status, updated new services, and total_price.
        In case the tourist cancels the request it returns status 400 and the rest of the list.
        In case the tourist decides to changes the dates, it returns status 400 and the rest of the list.
    """
    while True:
        print(f"\n*** Search for residence services for you in {city}***\n")
        residence_start_date, residence_end_date, duration = calc_duration(start_date, end_date, '12:00', '14:00')
        status, service_id, service_type, price = residence_search(tourist_nid, city, duration, no_passengers)
        if status == 300:
            clear_console()
            return [300, new_services, total_price]
        elif status == 400:
            clear_console()
            return [400, new_services, total_price]
        elif status == 500:
            clear_console()
            return [200, new_services, total_price]
        elif status == 200:
            new_service = pd.DataFrame(
                [['id',tourist_nid,service_id,'residence',service_type,city,city,residence_start_date,residence_end_date,price]],
                columns=['id','tourist_nid','service_id','type','service','starting_city','destination_city','start','end','price']
                )
            new_services = pd.concat([new_services, new_service], axis = 0, ignore_index=True)
            total_price += price
            clear_console()
            return [200, new_services, total_price]


def residence_search(tourist_nid:str, city:str, duration:int, no_passengers:int):
    """residence_search searchs for a residence service with specified conditions and reserve the fitted service which tourist picks.

    This function also requests the responssible Landlord for reservation and it does the bank transaction related to tourist.

    Args:
        tourist_nid (str): The tourist id
        city (str): The city of residence
        s_datatime (float | int): Staying duration
        number (int): The number of passengers

    Returns:
        list: In case the tourist completes the request, the function returns a list containing 200 status, updated new services, and total_price.
        In case the tourist cancels the request it returns status 400 and the rest of the list.
        In case the tourist decides to changes the dates, it returns status 400 and the rest of the list.
    """

    residences = pd.read_csv('./data/residences.csv', dtype=str)


    # fit_residences = residences[
    #     ([int(el) >= no_passengers  for el in residences.capacity]) &
    #     ([el == city for el in residences.address]) &
    #     ([el  == '0' for el in residences.reserved])
    # ]
    
    # fit_residences = residences.loc[(residences['address']== city) & (residences['reserved']== 0) & (residences['capacity'] >= no_passengers)]
    fit_residences = residences.loc[(residences['address']== city) & (residences['reserved']== '0') & (pd.to_numeric(residences.capacity, errors='coerce').fillna(0).astype(np.int64) > no_passengers)]

    if fit_residences.size:
        ids = []
        for _, row in fit_residences.iterrows():
            ids.append(row.id)
            print(f'{row.type} with {row.capacity} people capacity, {row.rent} Tomans rent per night, {row.no_scores} scored this residence and its score is {row.score}.')
            print(f'\n*** code: {row.id} ***\n')
        id = inp(
            "- To reserve a residence type its code\n- To change the dates you entered type 'change'\n- To cancel the travel type 'cancel'\n(code/cancel/change): ",
            "Invalid input. Enter again: ",
            key = lambda el: el in ids or el.lower() == 'cancel' or el.lower() == 'change'
        )
        if id.lower() == 'change': return [300, 0, 0, 0]
        elif id.lower() == 'cancel': return [400, 0, 0, 0]
        else:
            confirm = inp(
                f"Are you sure you want this resident for a total {float(row.rent) * duration} Tomans? \n(y/cancel/change): ",
                "Invalid input. Enter again: ",
                convert = lambda el: el.lower(),
                key = lambda el: el in ['y', 'cancel', 'change']
            )
            if confirm == 'change': return [300, 0, 0, 0]
            elif confirm == 'cancel': return [400, 0, 0, 0]
            price = float(fit_residences[fit_residences.id == id].rent.to_string(index=False)) * duration
            fit_landlord_id = fit_residences[fit_residences.id == id].landlord_id.to_string(index=False)
        
        landlords = pd.read_csv('./data/landlords.csv', dtype=str)
        fit_landlord_data = landlords[landlords.national_id == fit_landlord_id]

        from packages.landlord.Landlord import Landlord
        fit_landlord = Landlord(fit_landlord_data.username.to_string(index=False),
                                fit_landlord_data.password.to_string(index=False),
                                fit_landlord_data.first_name.to_string(index=False),
                                fit_landlord_data.last_name.to_string(index=False),
                                fit_landlord_data.national_id.to_string(index=False),
                                fit_landlord_data.tel.to_string(index=False))
        while True:
            try:
                withdraw(tourist_nid, price)
                fit_landlord.reservation(id, duration)
                break
            except:
                print('\n# # You dont have enough money. # #\n')
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
                if what_to_do == 'change': return [300, 0, 0, 0]
                elif what_to_do == 'cancel': return [400, 0, 0, 0]
        
        return [200, id, fit_residences[fit_residences.id == id].type.to_string(index=False), price]
    else:
        id = inp(
            "\n***There wasn't any fit service for you***\n- To change the dates you entered type 'change'\n- To cancel the travel type 'cancel'\n- To skip this step enter 'skip'\n",
            "Invalid input. Enter again: ",
            key = lambda el: el.lower() in ['cancel', 'change', 'skip']
        )
        if id.lower() == 'change': return [300, 0, 0, 0]
        elif id.lower() == 'cancel': return [400, 0, 0, 0]
        elif id.lower() == 'skip': return [500, 0, 0, 0]




def score(residence_id, new_score):
    # Alter the residence file and add or average score
    residences = pd.read_csv('./data/residences.csv', dtype=str)
    # i = residences[residences.id == residence_id].index
    i = residences[residences.landlord_id == residence_id].index

    if (i.size)!= 0:
        no_scores = int(residences.iloc[i[0], residences.columns.get_loc('no_scores')])
        score = residences.iloc[i[0], residences.columns.get_loc('score')]
        if score == 'None': score = 0
        else: score = int(score)

        residences.iloc[i[0], residences.columns.get_loc('no_scores')] = no_scores + 1
        residences.iloc[i[0], residences.columns.get_loc('score')] = score + (new_score/(no_scores+1))


        residences.to_csv('./data/residences.csv', index=False)
    return
