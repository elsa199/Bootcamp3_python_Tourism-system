import sys
import numpy as np
from numpy import array as Array
from sko.GA import GA_TSP as __GA_TSP
from tools.swap import swap
from sko.tools import set_run_mode



def ga(cities: Array, distances: list, indexes: list, start: int) -> list:
    no_cities = len(cities)
    start -= 1
    for el in indexes: #                        Check user numbers
        if el < 0 or el > no_cities:
            raise Exception()
    
    no_points = len(indexes)
    cut_distances = np.zeros([no_points, no_points])
    for indi, i in enumerate(indexes):
        for indj, j in enumerate(indexes):
            cut_distances[indi][indj] = distances[i - 1][j - 1]

            
    def distance(routine):
        '''The objective function. input routine, return total distance.
        distance(np.arange(num_points))
        '''
        # routine = np.insert(routine, 0, start) [1, 2, 0]
        num_points, = routine.shape
        d = distances[start][indexes[routine[0]] - 1] # Distance from start to first city in route
        d += sum([cut_distances[routine[i - 1]][routine[i]] for i in range(1, num_points)]) # Distance of the rest of the route
        return d
    # set_run_mode(distance, 'vectorization')
    ga_tsp = __GA_TSP(func=distance, n_dim=len(indexes), size_pop=50, max_iter=500, prob_mut=1)
    arrange, best_distance = ga_tsp.run()
    indexes = swap(indexes, arrange)
    
    if best_distance != 0: #                        Check Distance
        return [indexes, best_distance]
    else:
        raise Exception('You must choose cities, initiated with some city but your start city.')

if __name__ == "__main__":
    from data.points import cities, distances
    ga(cities, distances)