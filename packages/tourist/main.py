from packages.common.input import inp


def main(commands: list, tourist):
    if not isinstance(commands[0], list): commands = [commands, [lambda:None for _ in range(len(commands))]]
    relogin = False
    while not relogin:
        command = inp('', '\t\t***Wrong Command***\n', key = [lambda el: el in commands[0]])
        if command == 'travel':
            tourist.travel()
            # print(f'Your route is -> {trip}')
            # print(f'Your total route length would be -> {best_distance}', end='\nDone!\n\n')
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

