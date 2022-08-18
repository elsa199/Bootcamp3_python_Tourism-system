import sys
import numpy as np
from numpy import array as Array
from sko.GA import GA_TSP as __GA_TSP
from tools.swap import swap
from sko.tools import set_run_mode



def ga(cities: Array, distances: list, indexes: list, start: int) -> list:
    no_cities = len(cities)
    start -= 1 # index wise
    for el in indexes: #                        Check user numbers
        if el < 0 or el > no_cities:
            raise Exception()
    
    no_points = len(indexes) # Number of points

    if no_points == 1: # If user had one destination, there is no need to use Genetic Algorithm
        return [indexes, distances[start][indexes[0] - 1]]

    cut_distances = np.zeros([no_points, no_points]) # portion of distances we need.
    for indi, i in enumerate(indexes):
        for indj, j in enumerate(indexes):
            cut_distances[indi][indj] = distances[i - 1][j - 1]

            
    def distance(routine): # Objective Function which returns sum of distances
        '''The objective function. input routine, return total distance.
        distance(np.arange(num_points))
        '''
        num_points, = routine.shape
        d = distances[start][indexes[routine[0]] - 1] # Distance from start to first city in route
        d += sum([cut_distances[routine[i - 1]][routine[i]] for i in range(1, num_points)]) # Distance of the rest of the route
        return d
    
    ga_tsp = __GA_TSP(func=distance, n_dim=len(indexes), size_pop=50, max_iter=500, prob_mut=1)
    arrange, best_distance = ga_tsp.run()
    indexes = swap(indexes, arrange) # Arrange original indexes based on the arranged list
    
    if best_distance != 0: #                        Check Distance
        return [indexes, best_distance]
    else:
        raise Exception('You must choose cities, initiated with some city but your start city.')

if __name__ == "__main__":
    from data.points import cities, distances
    ga(cities, distances)