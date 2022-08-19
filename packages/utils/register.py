from packages.common.input import inp
import json


def register():
    # Update and add to database
    print('-=-=-=- We appritiate you joining us :) -=-=-=-')
    t = inp('Which one are you (tourist - landlord - driver)? please: ', 'Pick correctly: ',
        key = lambda x: x in ['tourist', 'landlord', 'driver'])
    u = inp('Please enter your username: ', 'Must has atleast 3 characters: ', key = lambda el: len(el) >= 3)
    p = inp('Please enter your password: ', 'Must has atleast 8 characters: ', key = lambda el: len(el) >= 8)
    inp('Please enter your password again: ', 'Passwords must match: ', key=lambda x: x == p)

    # Make a new user (tourist or landlord or driver)
    if t == 'tourist':
        tel = inp('Please enter your telephone number: ', 'Must has atleast 11 characters and be a number: ', key = lambda el: len(el) >= 11 and el.isnumeric())
        nid = inp('Please enter your national id number: ', 'Must be 10 characters and be a number: ', key = lambda el: len(el) == 10 and el.isnumeric())
        account_id = 'kimyvuj45d'
        new_user = {'username': u,'password': p, 'national_id': nid, 'tel': tel, 'account': {'account_id': account_id}, "active_services": [], 'travels': []}
    elif t == 'landlord':
        pass
    else:
        pass


    __update_data(new_user, t)


    return {
        'username': u,
        'type': t,
        'password': p
    }


def __update_data(new_user, t):
        with open(f"./data/{t}s.json", "r") as jsonFile:
            data = json.load(jsonFile)
        data.append(new_user)
        with open(f"./data/{t}s.json", "w") as jsonFile:
            json.dump(data, jsonFile)

