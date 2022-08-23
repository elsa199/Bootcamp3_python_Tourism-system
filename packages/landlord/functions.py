import pandas as pd
from packages.common.clear import clear_console
from packages.common.calculation import calc_duration
from packages.common.input import inp


def request_residence(tourist_nid, city, start_date, end_date, no_passengers, total_price, new_services):
    while True:
        print(f"\n*** Search for residence services for you in {city}***\n")
        residence_start_date, residence_end_date, duration = calc_duration(start_date, end_date, '12:00', '14:00')
        status, service_id, service_type, price = residence_search(city, duration, no_passengers)
        if status == 300:
            clear_console()
            break
        elif status == 400:
            clear_console()
            return [400, None, None, None]
        elif status == 500:
            clear_console()
            return [200, None, None, None]
        elif status == 200:
            new_service = pd.DataFrame(
                [['id',tourist_nid,service_id,'residence',service_type,city,city,residence_start_date,residence_end_date,price]],
                columns=['id','tourist_nid','service_id','type','service','starting_city','destination_city','start','end','price']
                )
            new_services = pd.concat([new_services, new_service], axis = 0, ignore_index=True)
            total_price += price
            clear_console()
            return [400, status, new_services, total_price]


def residence_search(city:str, duration:int, no_passengers:int):
    residences = pd.read_csv('./data/residences.csv', dtype=str)
    fit_residences = residences[int(residences.capacity) >= no_passengers and residences.adress.upper() == city.upper()]

    if not fit_residences.size:
        ids = []
        for _, row in fit_residences.iterrows():
            ids.append(row.id)
            print(f'{row.type} with {row.capacity} people capacity, {row.rent} Tomans rent per day, {row.no_scores} scored this residence and its score is {row.score}.')
            print(f'\n*** code: {row.id} ***\n')
        id = inp(
            "- To reserve a residence type its code\n- To change the dates you entered type 'change'\n- To cancel the travel type 'cancel'\n",
            "Invalid input. Enter again: ",
            key = lambda el: el in ids or el.lower() == 'cancel' or el.lower() == 'change'
        )
        if id.lower() == 'change': return [300, None, None, None]
        elif id.lower() == 'cancel': return [400, None, None, None]
        else: fit_landlord_id = fit_residences[fit_residences.id == id].landlord_id

        landlords = pd.read_csv('./data/landlords.csv', dtype=str)
        fit_landlord_data = landlords[landlords.national_id == fit_landlord_id]

        from packages.landlord.Landlord import Landlord
        fit_landlord = Landlord(fit_landlord_data.username,fit_landlord_data.password, fit_landlord_data.first_name,fit_landlord_data.family_name,fit_landlord_data.national_code,fit_landlord_data.tel)
        price = fit_landlord.reservation(id, duration)
        return 200, id, fit_residences[fit_residences.id == id].type, price
    else:
        id = inp(
            "\n***There wasn't any fit service for you***\n- To change the dates you entered type 'change'\n- To cancel the travel type 'cancel'\n- To skip this step enter 'skip'",
            "Invalid input. Enter again: ",
            key = lambda el: el.lower() in ['cancel', 'change', 'skip']
        )
        if id.lower() == 'change': return [300, None, None, None]
        elif id.lower() == 'cancel': return [400, None, None, None]
        elif id.lower() == 'skip': return [500, None, None, None]




def score(residence_id, new_score):
    # Alter the residence file and add or average score
    residences = pd.read_csv('./data/residences.csv', dtype=str)
    i = residences[residences.id == residence_id].index

    no_scores = int(residences.iloc[i[0], residences.columns.get_loc('no_scores')])
    score = residences.iloc[i[0], residences.columns.get_loc('score')]
    if score == 'None': score = 0
    else: score = int(score)

    residences.iloc[i[0], residences.columns.get_loc('no_scores')] = no_scores + 1
    residences.iloc[i[0], residences.columns.get_loc('score')] = score + (new_score/(no_scores+1))


    residences.to_csv('./data/residences.csv', index=False)
    return
