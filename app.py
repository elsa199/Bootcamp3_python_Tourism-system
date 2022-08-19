from data.points import cities, distances
from packages.tools.common import inp
from packages.utils.env import main as initialize
import json
import pandas as pd
print('---------------------------------------------------------------------')
print('                     Wellcome to our program                         ')
print('         When ever you wanted to cancel use-> Ctrl + c + Enter       ')
print('---------------------------------------------------------------------\n')


inputs = initialize()




if inputs['type'] == 'customer':
    fObj = open("./data/customers.json")
    jdict = json.load(fObj)
    customers = pd.json_normalize(jdict)
    while True:
        # Check username and password initialize(True)
        if (inputs['username'] in customers.username.tolist() and inputs['password'] in customers.password.tolist()):
            break
        else:
            print("***************\nWrong username and password. Please try again.\n***************\n")
            inputs = initialize(True)
    from packages.routes.customer import main as customer_route
    [trip, best_distance] = customer_route(cities, distances)
    print(trip, best_distance)