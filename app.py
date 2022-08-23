from packages.common.clear import clear_console
from packages.tourist.Class import Tourist
from packages.admin.Class import Admin
from packages.utils.env import main as initialize
from packages.utils.login import login
clear_console(0)

print('---------------------------------------------------------------------')
print('                     Wellcome to our program                         ')
print('         When ever you wanted to cancel use-> Ctrl + c + Enter       ')
print('---------------------------------------------------------------------\n')
rerun = False


# from packages.utils.updates import update_travels
# update_travels()



while True:
    inputs = initialize(rerun)
    user = login(inputs) # {'username': 'hamed', "password": '1', "type": 'tourist'}
    if not bool(user):
        rerun = True
        continue

    if isinstance(user, Tourist):
        from packages.tourist.main import main as tourist_route
        tourist_route(['travel', 'score', 'relogin'], user)
    elif isinstance(user, Admin):
        from packages.admin.main import main as admin_route
        admin_route(['add city', 'relogin'], user)
    clear_console(0)
    rerun = False

