import sys
from packages.common.input import inp
from packages.utils.register import register as __register
from packages.common.clear import clear_console
from packages.utils.updates import update_services

def main(rerun = False):
    update_services()
    if rerun: sys.argv = ['app.py']
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
        clear_console(0)
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
    t = inp('Which one are you (tourist - admin - landlord - driver) or type "register"? please: ', ' : ',
        key = lambda x: x in ['tourist', 'admin', 'landlord', 'driver', 'register'])
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




if __name__ == "__main__":
    print(main())
