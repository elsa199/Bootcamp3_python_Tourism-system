from time import sleep
import pandas as pd
from packages.common.clear import clear_console
from packages.common.calculation import calc_duration
from packages.common.input import inp
from packages.Bank.transaction import withdraw, deposit
from time import mktime

def request_vehicle(tourist_nid, start_city:str, end_city:int,  number: int, s_datatime, total_price, new_services):
    while True:
        print(f"\n*** Search for vehicle services for your trip from {start_city} to {end_city}***\n")
        status, service_id, service_type, price = vehicle_search(tourist_nid, start_city, end_city,  number, s_datatime)
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
                [['id',tourist_nid,service_id,'vehicle',service_type,start_city,end_city,s_datatime,price]],
                columns=['id','tourist_nid','service_id','type','service','starting_city','destination_city','start','price']
                )
            new_services = pd.concat([new_services, new_service], axis = 0, ignore_index=True)
            total_price += price
            clear_console()
            return [200, new_services, total_price]


 
def check_time(service_id, distance, s_datatime): # az city2
    vehicle = pd.read_csv('./data/vehicle.csv', dtype=str)
    i = vehicle.loc[(vehicle['Id']== service_id)].index
    avg_speed = vehicle.iloc[i[0], vehicle.columns.get_loc('avg_speed')] 
    s_dt = vehicle.iloc[i[0], vehicle.columns.get_loc('Start_datatime')] 

    t_delta = distance/avg_speed
    time_est = s_dt + t_delta

    return time_est


def vehicle_search(tourist_nid:str, start_city:str, end_city:int,  number: int, s_datatime):
    vehicle = pd.read_csv('./data/vehicle.csv', dtype=str)
    output_file= []
    
    vehicle.drop(vehicle[(vehicle['capacity'] == 0)].index, inplace=True)
    vehicle2 = vehicle.drop('national_id',axis=1)

    for i in vehicle2['start_date&time']:
        if i < mktime(localtime()):
            d= vehicle2[vehicle2['start_date&time']== i].index.values
            vehicle2.drop(d,axis='index',inplace= True)

    
    fit_vehicle = vehicle2.loc[(vehicle2['starting_city']== start_city) & (vehicle2['destination_city']== end_city) & 
                    (vehicle2['start_date&time']== s_datatime) & (vehicle2['capacity']>= number)]

    if fit_vehicle.size:
        ids = []
        for _, row in fit_vehicle.iterrows():
            ids.append(row.id)
            print(f'{row.type} with {row.capacity} people capacity, {row.rent} Tomans rent per person, {row.num_score} scored this vegicle and its score is {row.avg_Score}.')
            print(f'\n*** code: {row.id} ***\n')
        id = inp(
            "- To reserve a vehivle type its code\n- To change the dates you entered type 'change'\n- To cancel the vehicle type 'cancel'\n(code/cancel/change): ",
            "Invalid input. Enter again: ",
            key = lambda el: el in ids or el.lower() == 'cancel' or el.lower() == 'change'
        )
        if id.lower() == 'change': return [300, 0, 0, 0]
        elif id.lower() == 'cancel': return [400, 0, 0, 0]
        else:
            confirm = inp(
                f"Are you sure you want this vehicle for a total {float(row.rent) * number} Tomans? \n(y/cancel/change): ",
                "Invalid input. Enter again: ",
                convert = lambda el: el.lower(),
                key = lambda el: el in ['y', 'cancel', 'change']
            )
            if confirm == 'change': return [300, 0, 0, 0]
            elif confirm == 'cancel': return [400, 0, 0, 0]
            price = float(fit_vehicle[fit_vehicle.Id == id].rent[0]) * number
            fit_vehicle_id = fit_vehicle[fit_vehicle.Id == id].fit_vehicle[0]
        
        vehicle_owner = pd.read_csv('./data/vehicle_owner.csv', dtype=str)
        fit_veh_owner_data = vehicle_owner[vehicle_owner.national_id == fit_vehicle_id]

        from packages.moving_services.moving_service import Intercity_services
        vehicle_owner = Intercity_services(fit_veh_owner_data.username, fit_veh_owner_data.password, fit_veh_owner_data.first_name,
                                           fit_veh_owner_data.last_name, fit_veh_owner_data.national_id, fit_veh_owner_data.tel)
        while True:
            try:
                withdraw(tourist_nid, price)
                fit_vehicle.reservation(id, number)
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
                if confirm == 'change': return [300, 0, 0, 0]
                elif confirm == 'cancel': return [400, 0, 0, 0]
        
        return [200, id, fit_vehicle[fit_vehicle.Id == id].type[0], price]
    else:
        id = inp(
            "\n***There wasn't any fit service for you***\n- To change the dates you entered type 'change'\n- To cancel the travel type 'cancel'\n- To skip this step enter 'skip'",
            "Invalid input. Enter again: ",
            key = lambda el: el.lower() in ['cancel', 'change', 'skip']
        )
        if id.lower() == 'change': return [300, 0, 0, 0]
        elif id.lower() == 'cancel': return [400, 0, 0, 0]
        elif id.lower() == 'skip': return [500, 0, 0, 0]


def score(vehicle_id, new_score):

    vehicle = pd.read_csv('./data/vehicle.csv', dtype=str)
    i = vehicle[vehicle.Id == vehicle_id].index

    avg_Score = vehicle.iloc[i[0], vehicle.columns.get_loc('avg_Score')]
    num_score = vehicle.iloc[i[0], vehicle.columns.get_loc('num_score')]
    vehicle.iloc[i[0], vehicle.columns.get_loc('num_score')] = num_score + 1
    vehicle.iloc[i[0], vehicle.columns.get_loc('avg_ Score')] = avg_Score + (new_score/(num_score+1))

    vehicle.to_csv('./data/vehicle.csv', index=False)
    return