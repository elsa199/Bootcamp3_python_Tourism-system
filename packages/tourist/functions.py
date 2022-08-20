from packages.common.input import inp
from data.points import update_pds

def start_finder(address, cities, distances):
    try:
        if inp('Are you in home (y/n)?', '(y/n)? ', key=lambda el: el.upper() in ['Y', 'N']).upper()  == 'N':
            if inp('Do we have your current city in the list (y/n)?', '(y/n)? ', key=lambda el: el.upper() in ['Y', 'N']).upper() == 'Y':
                start = inp(
                    "First please enter city code in which you are living or leaving: ",
                    f"Please enter a valid number between 1 and {len(cities)}: ",
                    convert=int,
                    key=lambda el: el > 0 and el <= len(cities)
            )
            else: raise Exception(False)
        else: raise Exception(True)
    except Exception as e:
        try:
            search = address if e else 'Some non-sensce'
            print(search)
            start = cities.index(search) + 1
        except:
            print("\n       ----> Not recognized home city <----\n")
            cities, distances = update_pds(cities, distances, address)
    return [start, cities, distances]
