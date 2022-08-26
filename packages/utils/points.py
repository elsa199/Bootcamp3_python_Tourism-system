import numpy as np
import pandas as pd
from packages.common.input import inp

def load_cities_data(just: str = 'both'):
    cities = [el[0] for el in pd.read_csv('./data/cities.csv', header=None).values.tolist()]
    if just == 'cities': return cities
    distances = pd.read_csv('./data/distances.csv', header=None)
    if just == 'distances': return distances
    if just == 'both': return [cities, distances]


def update_cities_data(cities: list, distances, address):
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
    
