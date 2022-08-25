from time import mktime, localtime
import pandas as pd
from pandas import DataFrame

def update_services(new_service: DataFrame = pd.DataFrame()):
    active_services = pd.read_csv('data/active_services.csv', dtype=str)
    done_services = pd.read_csv('data/services.csv', dtype=str)

    last_id = max([int(el) for el in active_services.id] + [int(el) for el in done_services.id])

    done_services = pd.concat([done_services, active_services[[int(el) < mktime(localtime()) for el in active_services.end]]], axis = 0, ignore_index=True)    
    done_services.to_csv('data/services.csv', index= False)
    active_services = active_services.drop(active_services[[int(el) < mktime(localtime()) for el in active_services.end]].index)
    if bool(new_service.size):
        for i in new_service.index:
            last_id += 1
            new_service.loc[i,'id'] = str(last_id)
        active_services = pd.concat([active_services, new_service], axis = 0, ignore_index=True)
    active_services.to_csv('data/active_services.csv', index= False)




def update_user(new_user, type):
    users = pd.read_csv(f'./data/{type}s.csv', dtype=str)
    users = pd.concat([users, new_user], axis = 0, ignore_index=True)
    users.to_csv(f'./data/{type}s.csv', index= False)



def update_accounts(national_id):
    accounts = pd.read_csv(f'data/accounts.csv', dtype=str)
    if national_id not in [el for el in accounts.owner_id] or not accounts.size:
        try: last_id = max([int(el) for el in accounts.id])
        except: last_id = 0
        new_account = pd.DataFrame([[str(last_id + 1), national_id, '0']], columns=['id','owner_id','deposit'])

        accounts = pd.concat([accounts, new_account], axis = 0, ignore_index=True)
        accounts.to_csv(f'data/accounts.csv', index= False)
