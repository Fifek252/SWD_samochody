from typing import List, Union, Dict, Tuple
import numpy as np
from math import inf
from car import Cars

""" _____________
|  ________  |    o   o
| |  |____|  |    \__/
| |__________|____\ /
|__________________/
"""

    
class RSM:
    """
    Class creates ranking using RSM method
    """
    def __init__(self, cars: Cars, A0: List[List[Union[float, int]]], A1: List[List[Union[float, int]]]):
        """
        :param cars: set of all cars
        :param A0: set of status quo points
        :param A1: set of destination points
        """
        self.cars = cars 
        self.U = cars.get_parameters()
        self.a0 = A0
        self.a1 = A1
        self.weights = []


    def get_rank(self) -> Dict[Union[int, str], List[Union[int, float]]]:
        """
        Function creates ranking of top 20 cars
        :return: dictionary mapping car's id to its score function value in decreasing order
        """
        
        self.a0 = self.__naiveOWDfilterA(self.a0)
        self.a1 = self.__naiveOWDfilterA(self.a1)
        self.__naiveOWDfilterU()

        self.__consistent_classes()

        self.__calculate_weights()

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


    def __naiveOWDfilterU(self):
        """
        Function deletes dominated points from all cars
        """
        n = 0
        for key in self.U.keys():
            n = len(self.U[key])
            break
        
        U = self.U.copy()
        keys_to_remove = []
        checked_keys = []

        for keyY in U.keys():
            for keyX in U.keys():
                if not (keyY == keyX or keyY in keys_to_remove or keyY in checked_keys or keyX in keys_to_remove or keyX in checked_keys):
                    if all(U[keyY][i] <= U[keyX][i] for i in range(n)):
                        if not all(U[keyY][i] == U[keyX][i] for i in range(n)):
                            keys_to_remove.append(keyX)
                    if all(U[keyY][i] >= U[keyX][i] for i in range(n)):
                        if not all(U[keyY][i] == U[keyX][i] for i in range(n)):
                            keys_to_remove.append(keyY)
                        break
            checked_keys.append(keyY)

        for key in keys_to_remove:
            U.pop(key)
        self.U = U 
    

    def __naiveOWDfilterA(self, A: List[List[Union[int, float]]]) -> List[List[Union[int, float]]]:
        """
        Function deletes dominated points from status quo and destination set
        :param A: list of status quo or destination points
        :return: list of undominated status quo or destination points 
        """
        m, n = len(A), len(A[0])
        X = A.copy()
        i = 0
        while i < m:
            del_Y = False
            j = i + 1
            while j < m:
                delY = True
                delX = True
                eq = True
                for k in range(n):
                    if X[i][k] != X[j][k]:
                        eq = False
                    if X[i][k] < X[j][k]:
                        delY = False
                    if X[i][k] > X[j][k]:
                        delX = False
                    if (not delX) and (not delY):
                        break
                if delX and not eq:
                    X.pop(j)
                    m -= 1
                if delY and not eq:
                    X.pop(i)
                    m -= 1
                if not (delY or delX):
                    j += 1
                if delY:
                    del_Y = True
            if not del_Y:
                j = 0
                while j < i:
                    delX = True
                    eq = True
                    for k in range(n):
                        if X[i][k] != X[j][k]:
                            eq = False
                        if X[i][k] > X[j][k]:
                            delX = False
                        if not delX:
                            break
                    if delX and not eq:
                        X.pop(j)
                        m -= 1
                        i -= 1
                    if not delX:
                        j += 1
                i += 1
        return X


    def __consistent_classes(self):
        """
        Function checks if set of cars, status quo and destination points are consistent with one other
        """
        A1c = [p1 for p1 in self.a1 if all(all(i <= j for i, j in zip(p1, p0)) for p0 in self.a0)]
        A0c = self.a0
        if len(A1c) == 0:
            A1c = self.a1
            A0c = [p0 for p0 in self.a0 if all(all(i <= j for i, j in zip(p1, p0)) for p1 in self.a1)]

        Uc = {k: v for k, v in self.U.items() if any(all(i <= j for i, j in zip(v, p0)) for p0 in self.a0) or
            any(all(i >= j for i, j in zip(v, p1)) for p1 in self.a1)}
        
        self.U = Uc
        self.a0 = A0c
        self.a1 = A1c

    def __calculate_weights(self):
        """
        Function calculates wages for RSM method purposes
        """
        areas = []
        n = len(self.a0[0])
        for p0 in self.a0:
            for p1 in self.a1:
                area = np.sqrt(np.sum([(p0[i]-p1[i])**2 for i in range(n)]))
                areas.append((area, p0, p1))

        full_area = np.sum([area[0] for area in areas])
        self.weights = [(area[0]/full_area, area[1], area[2]) for area in areas]

    
    def __get_scores(self) -> Dict[int, float]:
        """
        Function calculates score function for each car from U
        :return: dictionary mapping car's id to its score function value
        """
        scores = {}
        for key, val in self.U.items():
            res = 0
            for area in self.weights:
                dist_i = np.sqrt(np.sum([(i-j)**2 for i, j in zip(val, area[2])]))
                dist_a = np.sqrt(np.sum([(i-j)**2 for i, j in zip(val, area[1])]))
                res += area[0] * dist_a/(dist_a + dist_i)
            scores[key] = res
        
        return scores
    


