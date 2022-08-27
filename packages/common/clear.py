import os
import sys

def clear_console(flag: bool = 1)->None:
    """clear_console clears the console with respect to the 'os' of running machine.

    Args:
        flag (bool, optional): rather to print exit hint or not. Defaults to True.
    """
    if sys.platform in ['win32', 'cygwin']:
        os.system('cls')
    elif sys.platform in ['linux', 'darwin']:
        os.system('clear')
    if flag:
        print('---------------------------------------------------------------------')
        print('         When ever you wanted to cancel use-> Ctrl + c + Enter       ')
        print('---------------------------------------------------------------------\n')
