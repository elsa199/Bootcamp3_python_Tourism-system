from packages.common.input import inp
from packages.common.input import clear_console
from loguru import logger

def main(commands: list, landlord):
    if not isinstance(commands[0], list): commands = [commands, [lambda:None for _ in range(len(commands))]]
    relogin = False
    while not relogin:
        clear_console()
        logger.success("Wellcome...")
        logger.info("What's your command? :)")
        command = inp('***\n' + '\n'.join(['You can write these commands: '] + commands[0]) + '\n***\n', '\t\t***Wrong Command***\n', key = [lambda el: el in commands[0]])
        if command == 'register residence':
            landlord.registeration()
            continue
        elif command == 'relogin':
            relogin = True
            continue
        else:
            output = commands[1][commands[0].index(command)]()
            continue