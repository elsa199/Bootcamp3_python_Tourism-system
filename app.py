from packages.common.clear import clear_console
from packages.tourist.Class import Tourist
from packages.utils.env import main as initialize
from packages.utils.login import login
clear_console()

print('---------------------------------------------------------------------')
print('                     Wellcome to our program                         ')
print('         When ever you wanted to cancel use-> Ctrl + c + Enter       ')
print('---------------------------------------------------------------------\n')

while True:
    inputs = initialize()
    user = login(inputs)

    if isinstance(user, Tourist):
        from packages.tourist.main import main as tourist_route
        tourist_route(['travel', 'relogin'], user)

