from packages import Tourist, Admin, Landlord, Intercity_services
from packages.common import clear_console
from packages.utils.env import main as initialize
from packages.utils import login
from loguru import logger
import sys
clear_console(0)

logger.remove()
logger.add(sys.stderr, format = "{time:HH:mm:ss} | <red>[{level}]</red> Message : <green>{message}</green>", colorize=True)
logger.info("The program was started successfully")

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

