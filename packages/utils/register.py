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
    # Make a new user (tourist or landlord or driver)
    if t == 'tourist':
        first_name = inp('Please enter your first name: ', 'Must has atleast 3 characters: ', key = lambda el: len(el) >= 3)
        last_name = inp('Please enter your last name: ', 'Must has atleast 3 characters: ', key = lambda el: len(el) >= 3)
        address = inp('Please enter your home city: ', 'Do not leave it empty: ')
        nid = inp('Please enter your national id number: ', 'Must be 10 characters and be a number: ', key = lambda el: len(el) == 10 and el.isnumeric())
        tel = inp('Please enter your telephone number: ', 'Must has atleast 3 characters and be a number: ', key = lambda el: len(el) >= 3 and el.isnumeric())
        new_user = pd.DataFrame([[
            u,p,first_name,last_name,address,nid,tel]],
            columns=['username','password','first_name','last_name','address','national_id','tel']
            )
    elif t == 'landlord':
        first_name = inp('Please enter your first name: ', 'Must has atleast 3 characters: ', key = lambda el: len(el) >= 3)
        last_name = inp('Please enter your last name: ', 'Must has atleast 3 characters: ', key = lambda el: len(el) >= 3)
        nid = inp('Please enter your national id number: ', 'Must be 10 characters and be a number: ', key = lambda el: len(el) == 10 and el.isnumeric())
        tel = inp('Please enter your telephone number: ', 'Must has atleast 3 characters and be a number: ', key = lambda el: len(el) >= 3 and el.isnumeric())
        new_user = pd.DataFrame([[
            u,p,first_name,last_name,nid,tel]],
            columns=['username','password','first_name','last_name','national_id','tel']
            )
    elif t == 'driver':
        pass

    
    update_user(new_user, t)
    update_accounts(new_user.national_id)
    return {
        'username': u,
        'type': t,
        'password': p
    }

