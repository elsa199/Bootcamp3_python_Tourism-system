from packages.common.clear import clear_console
from packages.tourist.Class import Tourist
from packages.admin.Class import Admin
from packages.landlord.Landlord import Landlord
from packages.driver.moving_service import Intercity_services
from packages.utils.env import main as initialize
from packages.utils.login import login
clear_console(0)

print('---------------------------------------------------------------------')
print('                     Wellcome to our program                         ')
print('         When ever you wanted to cancel use-> Ctrl + c + Enter       ')
print('---------------------------------------------------------------------\n')
rerun = False


while True:
    inputs = initialize(rerun)
    user = login(inputs)
    if not bool(user):
        rerun = True
        continue

    if isinstance(user, Tourist):
        from packages.tourist.main import main as tourist_route
        tourist_route(['travel', 'deposit', 'score', 'relogin', 'show services'], user)
    elif isinstance(user, Admin):
        from packages.admin.main import main as admin_route
        admin_route(['add city', 'relogin'], user)
    elif isinstance(user, Landlord):
        from packages.landlord.main import main as landlord_route
        landlord_route(['register residence', 'relogin'], user)
    elif isinstance(user, Intercity_services):
        from packages.driver.main import main as intercity_services_route
        intercity_services_route(['register vehicle', 'relogin'], user)
    clear_console(0)
    rerun = False

