import os
import sys

def clear_console(flag: int = 1):
    if sys.platform in ['win32', 'cygwin']:
        os.system('cls')
    elif sys.platform in ['linux', 'darwin']:
        os.system('clear')
    if flag:
        print('---------------------------------------------------------------------')
        print('         When ever you wanted to cancel use-> Ctrl + c + Enter       ')
        print('---------------------------------------------------------------------\n')
