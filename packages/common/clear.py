import os
import sys
print(sys.platform)

def clear_console():
    if sys.platform in ['win32', 'cygwin']:
        os.system('cls')
    elif sys.platform in ['linux', 'darwin']:
        os.system('clear')
