from packages.common.clear import clear_console
from packages.common.input import inp
from loguru import logger



def main(commands: list, tourist):
    """main function is the route of Tourist APIs.

    This main funciton controls and guids the commands which an Tourist can use. It takes the an instance of targeted Tourist.

    Args:
        commands (list): A nested list containing: list[0] is a list of commands themselves and list[1] is a list of callback functions.
        If commands are a single list, main function considers the defaulted callback functions.
        admin (Tourist): targeted Tourist returned from logging in.
    """
    tourist.score(False)


    if not isinstance(commands[0], list): commands = [commands, [lambda:None for _ in range(len(commands))]]
    relogin = False
    while not relogin:
        clear_console()
        logger.success("Wellcome...")
        logger.info("What's your command? :)")
        command = inp('***\n' + '\n'.join(['You can write these commands: '] + commands[0]) + '\n***\n', '\t\t***Wrong Command***\n', key = [lambda el: el in commands[0]])
        if command == 'travel':
            tourist.travel()
            continue
        if command == 'show services':
            tourist.show_services()
            continue
        if command == 'deposit':
            tourist.deposit()
            continue
        elif command == 'score':
            tourist.score()
            continue
        elif command == 'profile':
            # Show tourist data
            continue
        elif command == 'relogin':
            relogin = True
            continue
        else:
            output = commands[1][commands[0].index(command)]()
            continue

