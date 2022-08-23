import numpy as np
import pandas as pd
from packages.common.clear import clear_console
from packages.tourist.functions import  gimmedates
from packages.driver.Driver import search as ride_search

def request_transition(tourist_nid, start_city, destination_city, no_passengers, start_dates, destination_dates, new_services,  total_price):
    while True:
        print(f"\n*** Search for transition services for you from {start_city} to {destination_city}.***\n")
        start_date = gimmedates(start_city, destination_dates) # date of Leaving start_city
        status, service_id, service_type, destination_date, price = ride_search(start_city, destination_city, no_passengers, start_date)
        if status == 300:
            clear_console()
            break
        elif status == 400:
            clear_console()
            return [400, None, None, None, None]
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
            return [400, start_date, destination_date, new_service, total_price]
            