from packages.common.clear import clear_console
from packages.tourist.Class import Tourist
from packages.admin.Class import Admin
from packages.utils.env import main as initialize
from packages.utils.login import login
from loguru import logger
import sys

clear_console(0)

logger.remove()
logger.add(sys.stderr, format = "{time:HH:mm:ss} | <red>[{level}]</red> Message : <green>{message}</green>", colorize=True)
logger.info("The program was started successfully")
print('---------------------------------------------------------------------')
print('                     Wellcome to our program                         ')
print('         When ever you wanted to cancel use-> Ctrl + C + Enter      ')
print('---------------------------------------------------------------------\n')


rerun = False
while True:
    inputs = initialize(rerun)
    user = login(inputs) # {'username': 'hamed', "password": '1', "type": 'tourist'}
    if not bool(user):
        rerun = True
        continue

    if isinstance(user, Tourist):
        from packages.tourist.main import main as tourist_route
        tourist_route(['travel', 'relogin'], user)
    elif isinstance(user, Admin):
        from packages.admin.main import main as admin_route
        admin_route(['add city', 'relogin'], user)
    clear_console(0)
    rerun = False

