import pandas as pd

def login(inputs):
    users = pd.read_csv(f'./data/{inputs["type"]}s.csv', dtype=str)
    while True:
        # Check username and password initialize(True)
        try:
            i = users.username.tolist().index(inputs['username'])
            if users.password.tolist()[i] == inputs['password']:
                user = users.iloc[i].to_dict()
                break
            else: raise Exception()
        except Exception as e:
            print("***************\nWrong username and password. Please try again.\n***************\n")
            return False
    if inputs['type'] == 'tourist':
        from packages.tourist.Class import Tourist
        return Tourist(**user)
    if inputs['type'] == 'admin':
        from packages.admin.Class import Admin
        return Admin(**user)
    if inputs['type'] == 'landlord':
        from packages.landlord.Landlord import Landlord
        return Landlord(**user)
    if inputs['type'] == 'driver':
        from packages.driver.moving_service import Intercity_services
        return Intercity_services(**user)
