import pandas as pd
from packages.common.clear import clear_console
from packages.landlord.Landlord import search as residence_search


def request_residence(tourist_nid, city, start_date, end_date, no_passengers, total_price, new_services):
    while True:
        print(f"\n*** Search for residence services for you in {city}***\n")
        status, service_id, service_type, price = residence_search(city, start_date, end_date, no_passengers)
        if status == 300:
            clear_console()
            break
        elif status == 400:
            clear_console()
            return [400, None, None, None]
        elif status == 200:
            new_service = pd.DataFrame(
                [['id',tourist_nid,service_id,'residence',service_type,city,city,start_date,end_date,price]],
                columns=['id','tourist_nid','service_id','type','service','starting_city','destination_city','start','end','price']
                )
            new_services = pd.concat([new_services, new_service], axis = 0, ignore_index=True)
            total_price += price
            clear_console()
            return [400, status, new_services, total_price]