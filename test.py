from packages.landlord.Landlord import Landlord
from packages.common.clear import clear_console
from packages.tourist.Class import Tourist
from packages.admin.Class import Admin
from packages.utils.env import main as initialize
from packages.utils.login import login
from packages.utils.updates import update_accounts
from packages.Bank.transaction import deposit, withdraw
from packages.common.input import inp
clear_console(0)

print('---------------------------------------------------------------------')
print('                     Wellcome to our program                         ')
print('         When ever you wanted to cancel use-> Ctrl + c + Enter       ')
print('---------------------------------------------------------------------\n')
rerun = False


# while True:
#     inputs = initialize(rerun)
#     user = login({'username': 'hamed', "password": '1', "type": 'tourist'}) # 
#     if not bool(user):
#         rerun = True
#         continue

#     if isinstance(user, Tourist):
#         from packages.tourist.main import main as tourist_route
#         tourist_route(['travel', 'deposit', 'score', 'relogin'], user)
#     elif isinstance(user, Admin):
#         from packages.admin.main import main as admin_route
#         admin_route(['add city', 'relogin'], user)
#     elif isinstance(user, Landlord):
#         from packages.landlord.main import main as landlord_route
#         landlord_route(['register residence', 'relogin'], user)
#     clear_console(0)
#     rerun = False

