import math
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from gui.car import Cars

class MetodaTopsis:

    def __init__(self, cars: Cars):
        self.zbior_decyzji = cars.get_parameters()
        self.zbior_decyzji_Znormalizowany = {}
        self.zbior_niezdominowany_znormalizowany = {}
        self.wspolczynniki_skorigowane = []
        self.zbior_niezdominowany = {}

        self.punkt_idealny_znormalizowany = []
        self.punkt_antyidealny_znormalizowany = []

        self.zbior_rozwiazan = []   # indeksy rozwiazan od najlepszego do najgorszego


    def wyznaczZbiorNiezdominowany(self):
        przegladana_lista = self.zbior_decyzji.copy()

        for nazwa_punktu_Y, wartosc_Y in przegladana_lista.items():
            if przegladana_lista[nazwa_punktu_Y] is None:
                continue

            aktualna_wartosc = wartosc_Y
            aktualny_punkt = nazwa_punktu_Y
            podslownik = {k: przegladana_lista[k] for k in przegladana_lista.keys() if k > nazwa_punktu_Y}
            flaga = 0

            for nazwa_punktu_X, wartosc_X in podslownik.items():
                if przegladana_lista[nazwa_punktu_X] is None:
                    continue

                #sprawdz czy aktualny punkt punkt jest zdominowany
                if all(x >= y for x, y in zip(wartosc_X, aktualna_wartosc)):
                    # usun element z listy
                    przegladana_lista[nazwa_punktu_X] = None
                elif all(x <= y for x, y in zip(wartosc_X, aktualna_wartosc)):
                    przegladana_lista[aktualny_punkt] = None
                    flaga = 1
                    aktualna_wartosc = wartosc_X
                    aktualny_punkt = nazwa_punktu_X

            self.zbior_niezdominowany[aktualny_punkt] = aktualna_wartosc
            if not flaga:
                przegladana_lista[aktualny_punkt] = None


    def wyznaczPunktIdealny(self):
        parametr_min = []
        # stworz liste punktow idealnych
        for i in range(len(self.zbior_decyzji[1])):
            parametr_min.append(float('inf'))

        # wyznacz najlepsza (najmniejsza) wartosc w kazdej kolumnie

        for value in self.zbior_decyzji_Znormalizowany.values():
            for i in range(len(parametr_min)):
                if parametr_min[i] > value[i]:
                    parametr_min[i] = value[i]
        self.punkt_idealny_znormalizowany = parametr_min


    def wyznaczPunktAntyIdealny_nadir(self):
        parametr_max = []
        # stworz liste punktow antyidealnych
        for i in range(len(self.zbior_decyzji[1])):
            parametr_max.append(float('-inf'))

        # wyznacz najgorsza (najwieksza) wartosc w kazdej kolumnie zbioru niezdominowanego
        for value in self.zbior_niezdominowany_znormalizowany.values():
            for i in range(len(parametr_max)):
                if parametr_max[i] < value[i]:
                    parametr_max[i] = value[i]
        self.punkt_antyidealny_znormalizowany = parametr_max


    def utworzRankingRozwiazan(self):
        sorted_list = sorted(self.wspolczynniki_skorigowane, key=lambda x: x[1])

        ostateczne_rozwiazanie = {}
        for result in sorted_list:
            ostateczne_rozwiazanie[result[0]] = self.zbior_decyzji[result[0]]
        return ostateczne_rozwiazanie


    def wyznaczWspolczynnikSkorigowany(self):
        # dla wszystkich punktow niezdominowanych wyznacz wspolczynnik
        for id, wartosc in self.zbior_niezdominowany_znormalizowany.items():
            odleglosc_idealna = 0
            odleglosc_antyidealna = 0

            # odleglosc idealna
            for i in range(len(wartosc)):
                odleglosc_idealna += (wartosc[i] - self.punkt_idealny_znormalizowany[i]) ** 2

            # odleglosc antyidealna
            for i in range(len(wartosc)):
                odleglosc_antyidealna += (wartosc[i] - self.punkt_antyidealny_znormalizowany[i]) ** 2

            self.wspolczynniki_skorigowane.append([id, odleglosc_antyidealna/(odleglosc_antyidealna + odleglosc_idealna)])


    def normalizujZbior(self):
        suma_w_kolumnach = []
        norma = []
        for i in range(len(self.zbior_decyzji[1])):
            suma_w_kolumnach.append(0)
            norma.append(0)

        # sumuj kolumny
        for index, wartosc in self.zbior_decyzji.items():
            for i in range(len(self.zbior_decyzji[1])):
                suma_w_kolumnach[i] += (wartosc[i]**2)

        # oblicz norme dla kazdej kolumny
        for i in range(len(norma)):
            norma[i] = math.sqrt(suma_w_kolumnach[i])

        # znormalizuj wartosci w kolumnach zbioru decyzji
        for index, wartosc in self.zbior_decyzji.items():
            self.zbior_decyzji_Znormalizowany[index] = []
            for i in range(len(norma)):
                self.zbior_decyzji_Znormalizowany[index].append(wartosc[i] / norma[i])

        # znormalizuj wartosci w kolumnach zbioru niezdominowanego
        for index, wartosc in self.zbior_niezdominowany.items():
            self.zbior_niezdominowany_znormalizowany[index] = []
            for i in range(len(norma)):
                self.zbior_niezdominowany_znormalizowany[index].append(wartosc[i] / norma[i])


    def run_algorithm(self):
        TestClass.wyznaczZbiorNiezdominowany()
        TestClass.normalizujZbior()
        TestClass.wyznaczPunktIdealny()
        TestClass.wyznaczPunktAntyIdealny_nadir()
        TestClass.wyznaczWspolczynnikSkorigowany()
        return TestClass.utworzRankingRozwiazan()



if __name__ == '__main__':

    zbior_decyzji = {0: [4, 4, 5],
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

    test_base = Cars(zbior_decyzji, [True, True, True])
    test_base.update_parameters([True, True, True])
    TestClass = MetodaTopsis(test_base)
    print(TestClass.run_algorithm())
