import numpy as np
from numpy import array as Array
from sko.GA import GA_TSP

def ga(cities: Array, distances: list) -> list:
    no_cities = len(cities)
    print('-------------------------------------')
    print(*[f'{el}: {index + 1}' for index, el in enumerate(cities)], sep=" -=- ", end='\n-------------------------------------\n\n')
    start = int(input("First please enter city code in which you are living or leaving: "))
    while True:
        try:
            indexes = [int(el) for el in input('Please enter your visiting cities as a sequence (e.g. 1 2 3): ').split()]
            for el in indexes: #                        Check user numbers
                if el < 0 or el > no_cities:
                    raise Exception()
            
            def distance(routine):
                '''The objective function. input routine, return total distance.
                distance(np.arange(num_points))
                '''
                routine = np.insert(routine, 0, start)
                num_points, = routine.shape
                d = [distances[routine[i - 1]][routine[i]] for i in range(1, num_points)]
                return sum(d)
                return sum([distance_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points)])

            ga_tsp = GA_TSP(func=distance, n_dim=len(indexes), size_pop=50, max_iter=500, prob_mut=1)
            arrange, best_distance = ga_tsp.run()

            for ind, el in enumerate(arrange):
                temp = indexes[el]
                indexes[el] = indexes[ind]
                indexes[ind] = temp


            if best_distance != 0: #                        Check Distance
                return [indexes, best_distance]
                break
            else:
                print("You can't go from start to start.")
                raise Exception()
        except Exception as err:
            print("Please enter as you're suppose to enter, or type quit to cancel the prompt.")
            print(err)
            start = input("Enter city code in which you are living or leaving again, or you can quit: ")
            if start == 'quit':
                break
            else:
                while True:
                    try:
                        start = int(start)
                        break
                    except:
                        pass

if __name__ == "__main__":
    from data.points import cities, distances
    ga(cities, distances)