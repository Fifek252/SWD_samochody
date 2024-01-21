from typing import List, Union, Tuple, Dict
import numpy as np
from math import inf
import sys
import os

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

    def get_rank(self) -> Dict[int, List[Union[int, float]]]:
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
        return {id: self.cars.get_all_parameters()[id] for id, val in reversed(rank) if id is not None}

    def __get_scores(self) -> Dict[int, float]:
        """
        Function calculates score function for each car
        :return: dictionary mapping car's id to its score function value
        """
        params = self.cars.get_parameters()
        n = 0
        for key in params.keys():
            n = len(params[key])
            break

        gi = [inf for _ in range(n)]
        ga = [0 for _ in range(n)]

        for val in params.values():
            for i in range(n):
                if val[i] < gi[i]:
                    gi[i] = val[i]
                if val[i] > ga[i]:
                    ga[i] = val[i]

        scores = {}

        for key, val in params.items():
            score = 0
            for i, x in enumerate(val):
                diff = abs(ga[i] - gi[i])
                x_norm = (x-gi[i])/diff
                coeffs = self.ch_coeffs
                if x_norm < 0:
                    x_norm = abs(x_norm)
                    coeffs = coeffs.reversed()

                x0 = 0
                y0 = 1
                x1 = 0
                y1 = 1
                l = len(coeffs)

                for c in coeffs:
                    x0 = x1
                    x1 += 1/l
                    y0 = y1
                    y1 = c
                    if x_norm <= x1:
                        break
            
                a = (x0-x1)/(y0-y1)
                b = y0-a*x0
                score += (a*x_norm + b)/l
            scores[key] = score
        return scores
        

X = {0: [4, 4, 5],
                          1: [5, 4, -3],
                          2: [-2, 0, -2],
                          3: [0, 1, 5],
                          4: [2, 1, 6],
                          5: [1, -3, 1],
                          6: [4, 1, 2],
                          7: [3, 2, 3],
                          8: [3, 3, 5],
                          9: [3, -1, 6],
                          10: [-1, 1, 3],
                          11: [0, -1, 5],
                          12: [4, -2, 2],
                          13: [-1, 3, 4]}

test_base = Cars(X, [True, True, True])
test_base.update_parameters([True, False, True])

solver = UTA(test_base, [0.4, 1])

print(solver.get_rank())





