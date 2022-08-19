from packages.tools.common import inp
import json
from packages.utils.env import main as initialize
import pandas as pd
from packages.tools.ga import ga


def main(cities, distances, commands: list):
    if not isinstance(commands[0], list): commands = [commands]
    while True:
        command = inp('', '\t\t***Wrong Command***\n', key = [lambda el: el in commands[0]])
        if command == 'travel':
            [trip, best_distance] = travel(cities, distances)
            trip = [cities[el - 1] for el in trip]
            print(f'Your route is -> {trip}')
            print(f'Your total route length would be -> {best_distance}', end='\nDone!\n\n')
            continue
        elif command == 'profile':
            # Show customer data
            continue
        else:
            output = commands[1][commands[0].index(command)]()
            print(output)
            continue




def travel(cities, distances):
        
    print(*[f'{el}: {index + 1}' for index, el in enumerate(cities)], sep=" -=- ")

    start = inp(
        "First please enter city code in which you are living or leaving: ",
        f"Please enter a valid number between 1 and {len(cities)}: ",
        convert=int,
        key=lambda el: el > 0 and el <= len(cities)
    )

    trip = inp(
        'Please enter your visiting cities as a sequence (e.g. 1 2 3): ',
        f'Please enter a valid sequence of numbers between 1 and {len(cities)}, also dont enter your start city as first destination: ',
        convert=lambda Ls: [int(el) for el in Ls.split()],
        key=lambda L: L[0] != start
    )

    return ga(cities, distances, trip, start)


def login(inputs):
    fObj = open("./data/customers.json")
    jdict = json.load(fObj)
    customers = pd.json_normalize(jdict)
    while True:
        # Check username and password initialize(True)
        try:
            if customers.password.tolist()[customers.username.tolist().index(inputs['username'])] == inputs['password']:
                print("Wellcome sir... What's your command? :)")
                break
            else: raise Exception()
        except Exception as e:
            print(e)
            print("***************\nWrong username and password. Please try again.\n***************\n")
            inputs = initialize(True)
            continue
    return inputs