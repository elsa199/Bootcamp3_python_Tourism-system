from packages.common.clear import clear_console
from packages.common.input import inp
import pandas as pd
from packages.utils.updates import update_user, update_accounts

def register(): # Update and add to database
    
    print('\n-=-=-=- We appritiate you joining us :) -=-=-=-\n')
    t = inp('Which one are you (tourist - landlord - driver)? please: ', 'Pick correctly: ',
        key = lambda x: x in ['tourist', 'landlord', 'driver'])
    users = pd.read_csv(f'./data/{t}s.csv', dtype=str)
    usernames = users.username.tolist()
    u = inp('Please enter your username: ', 'This username is used, enter another one: ', key = lambda el: el not in usernames)
    p = inp('Please enter your password: ', 'Must has atleast 8 characters: ', key = lambda el: len(el) >= 8)
    inp('Please enter your password again: ', 'Passwords must match: ', key=lambda x: x == p)


    if t == 'tourist':
        first_name = inp('Please enter your first name: ', 'Must has atleast 3 characters: ', key = lambda el: len(el) >= 3)
        last_name = inp('Please enter your last name: ', 'Must has atleast 3 characters: ', key = lambda el: len(el) >= 3)
        clear_console()
        addresses = [el[0] for el in pd.read_csv('./data/cities.csv', header=None).values]
        print('\n !! Please pick your city only from this list of cities that we provide service in !!:')
        print(' - '.join(addresses))
        address = inp('Please enter your home city: ', 'Pick correctly: ', convert = lambda el: el.title(), key = lambda el: el in addresses)
        clear_console()
        nid = inp('Please enter your national id number: ', 'Must be 10 characters and be a number: ', key = lambda el: len(el) == 10 and el.isnumeric())
        tel = inp('Please enter your telephone number: ', 'Must has atleast 10 characters and be a number: ', key = lambda el: len(el) >= 10 and el.isnumeric())
        new_user = pd.DataFrame([[
            u,p,first_name,last_name,address,nid,tel]],
            columns=['username','password','first_name','last_name','address','national_id','tel']
            )
    elif t == 'landlord':
        first_name = inp('Please enter your first name: ', 'Must has atleast 3 characters: ', key = lambda el: len(el) >= 3)
        last_name = inp('Please enter your last name: ', 'Must has atleast 3 characters: ', key = lambda el: len(el) >= 3)
        nid = inp('Please enter your national id number: ', 'Must be 10 characters and be a number: ', key = lambda el: len(el) == 10 and el.isnumeric())
        tel = inp('Please enter your telephone number: ', 'Must has atleast 10 characters and be a number: ', key = lambda el: len(el) >= 10 and el.isnumeric())
        new_user = pd.DataFrame([[
            u,p,first_name,last_name,nid,tel]],
            columns=['username','password','first_name','last_name','national_id','tel']
            )
    elif t == 'driver':
        first_name = inp('Please enter your first name: ', 'Must has atleast 3 characters: ', key = lambda el: len(el) >= 3)
        last_name = inp('Please enter your last name: ', 'Must has atleast 3 characters: ', key = lambda el: len(el) >= 3)
        nid = inp('Please enter your national id number: ', 'Must be 10 characters and be a number: ', key = lambda el: len(el) == 10 and el.isnumeric())
        tel = inp('Please enter your telephone number: ', 'Must has atleast 10 characters and be a number: ', key = lambda el: len(el) >= 10 and el.isnumeric())
        new_user = pd.DataFrame([[
            u,p,first_name,last_name,nid,tel]],
            columns=['username','password','first_name','last_name','national_id','tel']
            )

    
    update_user(new_user, t)
    update_accounts(str(new_user.national_id[0]))
    return {
        'username': u,
        'type': t,
        'password': p
    }

