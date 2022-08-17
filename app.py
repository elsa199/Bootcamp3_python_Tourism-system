from data.points import cities, distances
from tools.common import inp
from tools.ga import ga
print('---------------------------------------------------------------------')
print('                     Wellcome to our program                         ')
print('         When ever you wanted to cancel use-> Ctrl + c + Enter       ')
print('---------------------------------------------------------------------\n')


print(*[f'{el}: {index + 1}' for index, el in enumerate(cities)], sep=" -=- ")

start = inp(
    "First please enter city code in which you are living or leaving: ",
    f"Please enter a valid number between 1 and {len(cities)}: ",
    convert=int,
    key=lambda el: el > 0 and el <= len(cities)
)

indexes = inp(
    'Please enter your visiting cities as a sequence (e.g. 1 2 3): ',
    f'Please enter a valid sequence of numbers between 1 and {len(cities)}, also dont enter your start city as first destination: ',
    convert=lambda Ls: [int(el) for el in Ls.split()],
    key=lambda L: L[0] != start
)

[indexes, best_distance] = ga(cities, distances, indexes, start)
