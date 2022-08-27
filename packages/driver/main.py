from packages.common.input import inp
from packages.common.clear import clear_console

def main(commands: list, moving_service):
    """main function is the route of Intercity_services APIs.

    This main funciton controls and guids the commands which an Intercity_services can use. It takes the an instance of targeted Intercity_services.

    Args:
        commands (list): A nested list containing: list[0] is a list of commands themselves and list[1] is a list of callback functions.
        If commands are a single list, main function considers the defaulted callback functions.
        admin (Intercity_services): targeted Intercity_services returned from logging in.
    """
    if not isinstance(commands[0], list): commands = [commands, [lambda:None for _ in range(len(commands))]]
    relogin = False
    while not relogin:
        clear_console()
        print("Wellcome... What's your command? :)")
        command = inp('***\n' + '\n'.join(['You can write these commands: '] + commands[0]) + '\n***\n', '\t\t***Wrong Command***\n', key = [lambda el: el in commands[0]])
        if command == 'register vehicle':
            moving_service.registeration()
            continue
        elif command == 'relogin':
            relogin = True
            continue
        else:
            output = commands[1][commands[0].index(command)]()
            continue