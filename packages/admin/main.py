from packages.common.input import inp
from loguru import logger


def main(commands: list, admin):
    """main function is the route of Admin APIs.

    This main funciton controls and guids the commands which an Admin can use. It takes the an instance of targeted Admin.

    Args:
        commands (list): A nested list containing: list[0] is a list of commands themselves and list[1] is a list of callback functions.
        If commands are a single list, main function considers the defaulted callback functions.
        admin (Admin): targeted Admin returned from logging in.
    """
    if not isinstance(commands[0], list): commands = [commands, [lambda:None for _ in range(len(commands))]]
    relogin = False
    while not relogin:
        logger.success("Wellcome...")
        logger.info("What's your command? :)")
        command = inp('***\n' + '\n'.join(['You can write these commands: '] + commands[0]) + '\n***\n', '\t\t***Wrong Command***\n', key = [lambda el: el in commands[0]])
        if command == 'add city':
            admin.add_city()
            continue
        elif command == 'relogin':
            relogin = True
            continue
        else:
            output = commands[1][commands[0].index(command)]()
            continue
