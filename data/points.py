import numpy as np
import pandas as pd
from packages.common.input import inp

cities = [el[0] for el in pd.read_csv('./data/cities.csv', header=None).values.tolist()]
# cities = [
#     'Tehran',  # 1
#     'Mashhad', # 2
#     'Isfahan', # 3
#     'Chaloos', # 4
#     'Zahedan', # 5
#     'Brojerd', # 6
#     'Hamedan', # 7
#     'Tabriz'   # 8
# ]
distances = pd.read_csv('./data/distances.csv', header=None)
# distances = np.array([
#     #1      2       3       4       5       6       7       8
#     [0,     911,    442,    141,    1516,   393,    317,    618], # 1
#     [911,   0,      1162,   910,    916,    1206,   1194,   1550], # 2
#     [442,   1162,   0,      580,    1212,   353,    474,    900], # 3
#     [141,   910,    580,    0,      1598,   522,    447,    746], # 4
#     [1516,  916,    1212,   1598,   0,      1612,   1636,   2022], # 5
#     [393,   1206,   353,    522,    1612,   0,      145,    698], # 6
#     [317,   1194,   474,    447,    1636,   145,    0,      558], # 7
#     [618,   1550,   900,    746,    2022,   698,    558,    0], # 8
# ])

def update_pds(cities: list, distances, address):

    temp = []
    for city in cities:
        choice = inp(
            f"Enter the distance between your home city {address} and {city}. Or enter 'random' or 'random all': ",
            "You should enter a number or 'random' or 'random all: '",
            convert = lambda el: int(el) if el.isnumeric() else str(el),
            key = lambda el: el in ['random', 'random all'] or isinstance(el, int)
        )
        if choice == 'random all':
            for _ in range(len(cities) - len(temp)): temp.append(np.random.randint(110, 1100))
            break
        elif choice == 'random': temp.append(np.random.randint(110, 1100))
        else: temp.append(choice)
    temp.append(0)
    
    distances = pd.concat([distances, pd.Series(temp)], axis = 1, ignore_index=True)
    for i in range(len(cities)):
        distances[i] = distances[i].replace([np.nan], temp[i])
    distances.to_csv('./data/distances.csv', header=None, index= False)
    cities.append(address)
    pd.DataFrame(cities).to_csv('./data/cities.csv', header=None, index= False)
    return [cities, distances]
    
