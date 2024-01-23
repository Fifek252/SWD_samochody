from typing import List, Union, Dict, Tuple
import numpy as np
import math
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
        self.waga = {}


    def normalizujZbior(self):
        """
        Normalizacja zgodnie z algorytmem podanym na zajeciach
        """
        min_w_kolumnach = []
        max_w_kolumnach = []
        for i in range(len(self.U[1])):
            min_w_kolumnach.append(float('inf'))
            max_w_kolumnach.append(float('-inf'))

        # wyznacz najmniejszy i najwiekszy element w kazdaj kolumnie
        for parametry_auta in self.U.values():
            for index_kryterium, kryteria_auta in enumerate(parametry_auta):
                #minimum
                if kryteria_auta < min_w_kolumnach[index_kryterium]:
                    min_w_kolumnach[index_kryterium] = kryteria_auta

                #maksimum
                if kryteria_auta > max_w_kolumnach[index_kryterium]:
                    max_w_kolumnach[index_kryterium] = kryteria_auta

        # znormalizuj wartosci w kolumnach zbioru decyzji
        zbior_decyzji_Znormalizowany = {}
        for index, wartosc in self.U.items():
            zbior_decyzji_Znormalizowany[index] = []
            for i in range(len(wartosc)):
                f_x = (wartosc[i] - min_w_kolumnach[i])/ (max_w_kolumnach[i] - min_w_kolumnach[i])
                zbior_decyzji_Znormalizowany[index].append(f_x)

        self.U = zbior_decyzji_Znormalizowany


        # znormalizuj wartosci punktow docelowych
        for index_punktu in range(len(self.a1)):
            for index, wartosc in enumerate(self.a1[index_punktu]):
                f_x = (wartosc - min_w_kolumnach[index]) / (max_w_kolumnach[index] - min_w_kolumnach[index])
                self.a1[index_punktu][index] = f_x

        # znormalizuj wartosci punktow status-quo
        for index_punktu in range(len(self.a0)):
            for index, wartosc in enumerate(self.a0[index_punktu]):
                f_x = (wartosc - min_w_kolumnach[index]) / (max_w_kolumnach[index] - min_w_kolumnach[index])
                self.a0[index_punktu][index] = f_x


    def get_rank(self) -> Dict[int, List[Union[int, float]]]:
        """
        Function creates ranking of top 20 cars
        :return: dictionary mapping car's id to its score function value in decreasing order
        """
        # self.normalizujZbior()


        self.a0 = self.__naiveOWDfilterA(self.a0)
        self.a1 = self.__naiveOWDfilterA(self.a1)
        self.__naiveOWDfilterU()

        self.__consistent_classes()

        wyznaczone_punkty = self.wyznaczKrzywaSzkieletowa(self.a0[0], self.a1[0])
        self.oblicz_wage(wyznaczone_punkty)

        return self.utworzRankingRozwiazan()


    def oblicz_wage(self, wyznaczone_punkty):
        for indeks, samochod in self.U.items():
            najlepsza_odleglosc = float('inf')
            for punkt in wyznaczone_punkty:
                odleglosc_tymczasowa = self.oblicz_odleglosc(samochod, punkt)
                if najlepsza_odleglosc > odleglosc_tymczasowa:
                    najlepsza_odleglosc = odleglosc_tymczasowa

            if self.waga.get(indeks) is not None:
                self.waga[indeks] += najlepsza_odleglosc
            else:
                self.waga[indeks] = najlepsza_odleglosc


    def oblicz_odleglosc(self, samochod, punkt):
        # Sprawdź, czy wektory mają tę samą długość
        if len(samochod) != len(punkt):
            raise ValueError("Wektory muszą mieć tę samą długość")

        # Oblicz normę Czebyszewa
        suma_kwadratow_roznicy = sum((punkt[i] - samochod[i]) ** 2 for i in range(len(samochod)))
        norma = math.sqrt(suma_kwadratow_roznicy)

        #oblicz t(γij)
        suma_kwadratow_roznicy = sum((punkt[i] - self.a1[0][i]) ** 2 for i in range(len(self.a1[0])))
        tγij = math.sqrt(suma_kwadratow_roznicy)

        return (tγij + norma)


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
                if not (
                        keyY == keyX or keyY in keys_to_remove or keyY in checked_keys or keyX in keys_to_remove or keyX in checked_keys):
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

    #Krzywą szkieletową
    def wyznaczKrzywaSzkieletowa(self, status_quo, punkty_docelowe):
        #TODO: na razie tylko dla jednego punktu
        wszystkie_punkty = [status_quo.copy(), punkty_docelowe.copy()]

        status_quo_copy = status_quo.copy()
        punkty_docelowe_copy = punkty_docelowe.copy()

        #algorytm przedstawiony na zajęciach
        for j in range(len(status_quo) - 1):
            # wyznaczamy d
            d = []
            for i in range(len(status_quo)):
                di = (status_quo_copy[i] - punkty_docelowe_copy[i]) / 2
                d.append(di)
            d.sort()

            for i in range(len(status_quo)):
                if j-1 < i:
                    status_quo_copy[i] = status_quo_copy[i] - d[j]
                    punkty_docelowe_copy[i] = punkty_docelowe_copy[i] + d[j]

            wszystkie_punkty.append(status_quo_copy.copy())
            wszystkie_punkty.append(punkty_docelowe_copy.copy())

        return  wszystkie_punkty


    def utworzRankingRozwiazan(self):
        lista_wynikow = []
        for key, value in self.waga.items():
            lista_wynikow.append([key, value])

        sorted_list = sorted(lista_wynikow, key=lambda x: x[1])

        ostateczne_rozwiazanie = {}
        for result in sorted_list:
            ostateczne_rozwiazanie[result[0]] = self.U[result[0]]

        return ostateczne_rozwiazanie


if __name__ == '__main__':
    A0 = [[3, 5, 7, 6]]
    A1 = [[1, 1, 1, 1]]
    X = { 1: [2, 1, 2, 3],
           3: [1, 1, 5, 4],
           5: [1, 3, 1, 5],
           10: [1, 1, 3, 4],
           11: [1, 1, 5, 2]}

    test_base = Cars(X, [True, True, True, True])
    test_base.update_parameters([True, True, True, True])

    solver = RSM(test_base, A0, A1)
    print(solver.get_rank())
