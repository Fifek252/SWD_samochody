from typing import List, Union, Tuple, Dict
import numpy as np
from math import inf


class Variant:
    def __init__(self, id: int, parameters: List[Union[int, float]], minimalize: List[bool], criteria: List[bool]):
        self.__id = id
        self.__parameters = parameters
        self.__minimalize = minimalize
        self.__criteria = criteria
        self.params = []
        n = len(parameters)
        for i in range(n):
            if criteria[i]:
                if minimalize[i]:
                    self.params.append(parameters[i])
                else:
                    self.params.append(-parameters[i])

    def id(self):
        return self.__id
    
    def minimalize(self):
        return self.__minimalize


def UTA(U: List[List[Union[int, float]]], ch_coeffs: List[List[float]]) -> List[Tuple[List[Union[int, float]], float]]:
    Uc = U.copy()
    m = len(Uc)
    n = len(Uc[0])
    gi = [inf for _ in range(n)]
    ga = [0 for _ in range(n)]
    for i in range(m):
        for j in range(n):
            if Uc[i][j] < gi[j]:
                gi[j] = Uc[i][j]
            if Uc[i][j] > ga[j]:
                ga[j] = Uc[i][j]

    Uglobal = [0 for _ in range(m)]

    for i in range(n):
        def uFunN(x: Union[int, float]) -> float:
            diff = abs(ga[i] - gi[i])
            x_norm = (x - gi[i])/diff
            coeffs = ch_coeffs[i]
            x0 = 0
            y0 = 1
            x1 = 0
            y1 = 1
            l = len(coeffs)
            if x_norm < 0:
                x_norm = abs(x_norm)
                coeffs = coeffs.reversed()
            """
            Na razie tylko dla minimalizacji, możliwe że dla maksymalizacji trzeba odwrócić kolejność coeffs i przemnożyć wszystko przez -1
            """
            for c in coeffs:
                x0 = x1
                x1 += 1/l
                y0 = y1
                y1 -= c
                if x_norm <= x1:
                    break
            
            a = (x0-x1)/(y0-y1)
            b = y0-a*x0

            return (a*x_norm + b)/4
        
        for m, var in enumerate(Uc):
            Uglobal[m] += uFunN(var)
        




            
            

