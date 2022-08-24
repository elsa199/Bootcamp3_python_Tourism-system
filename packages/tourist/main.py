from packages.common.clear import clear_console
from packages.common.input import inp



def main(commands: list, tourist):
    tourist.score(False)


    if not isinstance(commands[0], list): commands = [commands, [lambda:None for _ in range(len(commands))]]
    relogin = False
    while not relogin:
        clear_console()
        print("Wellcome... What's your command? :)")
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

