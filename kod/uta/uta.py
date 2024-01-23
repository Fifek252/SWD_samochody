from typing import List, Union, Tuple, Dict
import numpy as np
from math import inf

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from gui.car import Cars

""" _____________
|  ________  |    o   o
| |  |____|  |    \__/
| |__________|____\ /
|__________________/
"""

class UTA:
    """
    Class creates ranking using UTA method
    """
    def __init__(self, cars: Cars, ch_coeffs: List[List[float]]):
        self.cars = cars 
        self.ch_coeffs = ch_coeffs

    def get_rank(self) -> Dict[Union[int, str], List[Union[int, float]]]:
        """
        Function creates ranking of top 20 cars
        :return: dictionary mapping car's id to its score function value in decreasing order
        """
        scores = self.__get_scores()
        rank = [(None, inf) for _ in range(20)]
        for key, val in scores.items():
            for i in range(20):
                if rank[i][1] > val:
                    for j in range(20-i-1):
                        rank[-(j+1)] = rank[-(j+2)]
                    rank[i] = (key, val)
                    break
            

                a = (x0-x1)/(y0-y1)
                b = y0-a*x0
                score += (a*x_norm + b)/l
            scores[key] = score
        return scores
        

X = {
    'Bruce Lee': [4, 4, 5],
    'Sławomir Borewicz': [5, 4, -3],
    'Alf': [-2, 0, -2],
    'Bruce Willis': [0, 1, 5],
    'Królik Bugs': [2, 1, 6],
    'Clint Eastwood': [1, -3, 1],
    'Chuck Norris': [4, 1, 2],
    'Darth Vader': [3, 2, 3],
    'Kevin McCallister': [3, 3, 5],
    'Steven Seagal': [3, -1, 6],
    'Ojciec Mateusz': [-1, 1, 3],
    'Saxton Hale': [0, -1, 5],
    'Król Julian': [4, -2, 2],
    'John Rambo': [-1, 3, 4]
    }

test_base = Cars(X, [True, True, True])
test_base.update_parameters([True, False, True])

solver = UTA(test_base, [0.4, 1])

print(solver.get_rank())



            return (a*x_norm + b)/4
        
        for m, var in enumerate(Uc):
            Uglobal[m] += uFunN(var)

