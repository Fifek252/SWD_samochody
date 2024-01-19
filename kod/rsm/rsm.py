from typing import List, Union, Dict, Tuple
import numpy as np

""" _____________
|  ________  |    o   o
| |  |____|  |    \__/
| |__________|____\ /
|__________________/
"""


def naiveOWDfilter(X: List[List[Union[int, float]]]) -> List[List[Union[int, float]]]:
    """
    Function deletes dominated points from set X
    :param X: set of points
    :type X: List[List[Union[int, float]]]
    :return: set of points excluding dominated
    :type: List[List[Union[int, float]]]
    """
    m, n = len(X), len(X[0])
    Xcopy = X.copy()
    i = 0
    while i < m:
        del_Y = False
        j = i + 1
        while j < m:
            delY = True
            delX = True
            eq = True
            for k in range(n):
                if Xcopy[i][k] != Xcopy[j][k]:
                    eq = False
                if Xcopy[i][k] < Xcopy[j][k]:
                    delY = False
                if Xcopy[i][k] > Xcopy[j][k]:
                    delX = False
                if (not delX) and (not delY):
                    break
            if delX and not eq:
                Xcopy.pop(j)
                m -= 1
            if delY and not eq:
                Xcopy.pop(i)
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
                    if Xcopy[i][k] != Xcopy[j][k]:
                        eq = False
                    if Xcopy[i][k] > Xcopy[j][k]:
                        delX = False
                    if not delX:
                        break
                if delX and not eq:
                    Xcopy.pop(j)
                    m -= 1
                    i -= 1
                if not delX:
                    j += 1
            i += 1
    return Xcopy


def consistent_classes(U: List[List[Union[float, int]]], A0: List[List[Union[float, int]]],
                       A1: List[List[Union[float, int]]]) -> Tuple[List[List[Union[float, int]]],
                                                                   List[List[Union[float, int]]],
                                                                   List[List[Union[float, int]]]]:
    """
    Function checks if every set is consistent to one another
    :param U: set of all undominated points
    :type U: List[List[Union[int, float]]
    :param A0: set of undominated status quo points
    :type A0: List[List[Union[int, float]]
    :param A1: set of undominated destination points
    :type A1: List[List[Union[int, float]]
    :return: Uc
    :type: Tuple[List[List[Union[float, int]]], List[List[Union[float, int]]], List[List[Union[float, int]]]]
    """
    A1c = [p1 for p1 in A1 if all(all(i <= j for i, j in zip(p1, p0)) for p0 in A0)]
    A0c = A0
    if len(A1c) == 0:
        A1c = A1
        A0c = [p0 for p0 in A0 if all(all(i <= j for i, j in zip(p1, p0)) for p1 in A1)]

    Uc = [u for u in U if any(all(i <= j for i, j in zip(u, p0)) for p0 in A0) and
          any(all(i >= j for i, j in zip(u, p1)) for p1 in A1)]

    return Uc, A0c, A1c


def calculate_weights(A0: List[List[Union[float, int]]], A1: List[List[Union[float, int]]]) -> \
        List[Tuple[float, List[Union[int, float]], List[Union[int, float]]]]:
    """
    Function calculates weights for each rectangle created from status quo and destination point
    :param A0: set of status quo points
    :type A0: List[List[Union[float, int]]]
    :param A1: set of destination points
    :type A1: List[List[Union[float, int]]]
    :return: set of tuples mapping weight to pair of status quo and destination point
    :type: List[Tuple[float, List[Union[int, float]], List[Union[int, float]]]]
    """
    areas = []
    n = len(A0[0])
    for p0 in A0:
        for p1 in A1:
            area = np.sqrt(np.sum([(p0[i]-p1[i])**2 for i in range(n)]))
            areas.append((area, p0, p1))

    full_area = np.sum([area[0] for area in areas])
    weights = [(area[0]/full_area, area[1], area[2]) for area in areas]
    return weights


def scor_fcn(u: List[Union[int, float]], W: List[Tuple[float, List[Union[int, float]], List[Union[int, float]]]]) ->\
        float:
    """
    :param u: set of all points
    :type u: List[Union[int, float]]
    :param W: set of weights mapped to pair of status quo and destination points
    :type W: List[Tuple[float, List[Union[int, float]], List[Union[int, float]]]]
    :return: score function of point
    :type: float
    """
    res = 0
    for area in W:
        if all(i <= j for i, j in zip(u, area[1])) and all(i >= j for i, j in zip(u, area[2])):
            dist_i = np.sqrt(np.sum([(i-j)**2 for i, j in zip(u, area[2])]))
            dist_a = np.sqrt(np.sum([(i-j)**2 for i, j in zip(u, area[1])]))
            res += area[0] * dist_a/(dist_a + dist_i)
    return res


def RSM(U: List[List[Union[float, int]]], A0: List[List[Union[float, int]]], A1: List[List[Union[float, int]]]) -> \
    Dict[List[Union[float, int]], float]:
    """
    Function computing score function values of all points U between A0 and A1
    :param U: set of all points
    :type U: List[List[Union[int, float]]
    :param A0: set of status quo points
    :type A0: List[List[Union[int, float]]
    :param A1: set of destination points
    :type A1: List[List[Union[int, float]]
    :return: Dict mapping points to score function values
    :type: Dict[List[Union[float, int]], float]
    """
    if not all(isinstance(L, List) for L in [U, A0, A1]):
        raise ValueError("All parameters should be lists of lists of float or int")
    if not all(all(isinstance(L[i], list) for i in range(len(L))) for L in [U, A0, A1]):
        raise ValueError("All parameters should be lists of lists of float or int")
    if not all(all(all(isinstance(L[i][j], int) or isinstance(L[i][j], float) for j in range(len(L[i]))) \
                   for i in range(len(L))) for L in [U, A0, A1]):
        raise ValueError("All parameters should be lists of lists of float or int")

    Uc = U.copy()
    A0c = A0.copy()
    A1c = A1.copy()

    Uc = naiveOWDfilter(Uc)
    A0c = naiveOWDfilter(A0c)
    A1c = naiveOWDfilter(A1c)

    Uc, A0c, A1c = consistent_classes(Uc, A0c, A1c)

    W = calculate_weights(A0c, A1c)

    scors = {}

    for p in Uc:
        scors[p] = scor_fcn(p, W)

    return scors
