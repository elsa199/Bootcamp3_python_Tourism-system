import os
import sys
from packages.tools.common import inp
import json

def main(rerun = False):
    if rerun: sys.argv = ['']
    def __set_out(key, value):
        out[key] = value
    login__checker = True
    while True:
        __ok, out = __checker()
        if  __ok and login__checker:
            args = [[sys.argv[i], sys.argv[i+1]] for i in range(1, len(sys.argv), 2)]
            setCB = lambda key, value: __set_out(key, value)
            __do_on_args(args, [['u', 'username'], ['p', 'password'], ['t', 'type']], setCB)
            if 'username' in out.keys() or 'type' in out.keys() or 'password' in out.keys():
                if 'username' not in out.keys() or 'type' not in out.keys() or 'password' not in out.keys():
                    print('when using enviromental variables, use three "type", "username" and "password" together.')
                    login__checker = False
                    continue
        return out

def __do_on_args(arg_list, exp_list, func_list):
    if callable(func_list): func_list = [func_list for _ in range(len(exp_list))]
    for arg in arg_list:
        find = arg[0][2] if arg[0].startswith('--') else arg[0][1]
        index = __find_index(exp_list, find)
        if index != -1: func_list[index](exp_list[index][1], arg[1])



def __find_index(list, el):
    for i, el_list in enumerate(list):
        if el in el_list: return i
    return -1

def __checker():
    if len(sys.argv) > 1 and len(sys.argv) % 2 != 0 and sys.argv[1] != '-h' and sys.argv[1] != '--help' and sys.argv[1] != '-r' and sys.argv[1] != '--register':
        return [True, dict()]
    elif len(sys.argv) == 1:
        temp = __must()
        return [False, temp]
    elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
        sys.exit('msg')
    elif sys.argv[1] == '-r' or sys.argv[1] == '--register':
        temp = __register()
        return [False, temp]
    elif len(sys.argv) % 2 == 0:
        raise SyntaxError("You have an error in syntax, try: python app.py --help")


def __must():
    t = inp('Which one are you (customer - admin - landlord - driver) or type "register"? please: ', 'Pick correctly: ',
        key = lambda x: x in ['customer', 'admin', 'landlord', 'driver', 'register'])
    if t == 'register':
        temp = __register()
        return temp
    u = inp('Please enter your username: ', 'Dont leave it empty: ')
    p = inp('Please enter your password: ', 'Dont leave it empty: ')
    return {
        'username': u,
        'type': t,
        'password': p
    }
def __register():
    # Update and add to database
    print('-=-=-=- We appritiate you joining us :) -=-=-=-')
    t = inp('Which one are you (customer - admin - landlord - driver)? please: ', 'Pick correctly: ',
        key = lambda x: x in ['customer', 'admin', 'landlord', 'driver'])
    u = inp('Please enter your username: ', 'Must has atleast 3 characters: ', key = lambda el: len(el) >= 3)
    p = inp('Please enter your password: ', 'Must has atleast 8 characters: ', key = lambda el: len(el) >= 8)
    inp('Please enter your password again: ', 'Passwords must match: ', key=lambda x: x == p)
    __update_data({'username': u,'password': p}, t)
    return {
        'username': u,
        'type': t,
        'password': p
    }


def __update_data(new_user, t):
    if t == 'customer':
        with open("./data/customers.json", "r") as jsonFile:
            data = json.load(jsonFile)
        data.append(new_user)
        with open("./data/customers.json", "w") as jsonFile:
            json.dump(data, jsonFile)




if __name__ == "__main__":
    print(main())
