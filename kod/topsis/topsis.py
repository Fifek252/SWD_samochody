import math


class MetodaTopsis:

    def __init__(self):
        # self.zbior_decyzji = {1: [4, 4],
        #                  2: [5, 4],
        #                  3: [-2, 0],
        #                  4: [0, 1],
        #                  5: [2, 1],
        #                  6: [1, -3],
        #                 7: [4, 1],
        #                 8: [3, 2],
        #                 9: [3, 3],
        #                 10: [3, -1],
        #                 11: [-1, 1],
        #                 12: [0, -1],
        #                 13: [4, -2],
        #                 14: [-1, 3]}
        self.zbior_decyzji = {0: [4, 4, 5],
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

        self.waga_kryterium = []
        # tymczasowe rozwiazanie mozliwe do modyfikacji w przyszlosci
        for i in range(len(self.zbior_decyzji[0])):
            self.waga_kryterium.append(1)

        # ta opcja pozwala na wybor, czy dane kryterium ma byc maksymalizowane, czy minimalizowane
        # TODO: upewnic sie czy implementacja jest prawidlowa, na razie algorytm jest dostosowany
        # do znajdywania minimum, jezeli chcemy maksymalizowac kryterium, kolumna jest mnozona przez -1
        self.choose_min_max = []
        for i in range(len(self.zbior_decyzji[0])):
            self.choose_min_max.append(1)

        self.zbior_decyzjiZnormalizowany = {}
        self.zbiorniezdominowanyZnormalizowany = {}
        self.wspolczynniki_skorigowane = []
        self.zbior_niezdominowany = {}

        self.punkt_idealnyZnormalizowany = [0, 0]
        self.punkt_antyidealnyZnormalizowany = [0, 0]

        self.zbior_rozwiazan = []


    # modyfikuje tabele w zaleznosci, czy kryterium jest maksymalizowane, czy minimalizowane
    def okresl_kryterium_min_max(self):
        for index_punktu, punkt in self.zbior_decyzji.items():
            for index_kryterium, kryterium in enumerate(punkt):
                if self.choose_min_max[index_kryterium] == -1:
                    self.zbior_decyzji[index_punktu][index_kryterium] = punkt[index_kryterium] * -1


    # Algorytm z filtracja
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
        for value in self.zbior_decyzjiZnormalizowany.values():
            for i in range(len(parametr_min)):
                if parametr_min[i] > value[i]:
                    parametr_min[i] = value[i]

        self.punkt_idealnyZnormalizowany = parametr_min


    def wyznaczPunktAntyIdealny_nadir(self):
        parametr_max = []
        # stworz liste punktow antyidealnych
        for i in range(len(self.zbior_decyzji[1])):
            parametr_max.append(float('-inf'))

        # wyznacz najgorsza (najwieksza) wartosc w kazdej kolumnie zbioru niezdominowanego
        for value in self.zbiorniezdominowanyZnormalizowany.values():
            for i in range(len(parametr_max)):
                if parametr_max[i] < value[i]:
                    parametr_max[i] = value[i]

        self.punkt_antyidealnyZnormalizowany = parametr_max


    def utworzRankingRozwiazan(self):
        sorted_list = sorted(self.wspolczynniki_skorigowane, key=lambda x: x[1])

        # kolumny z kryterium maksymalizujacym sa na poczatku dzialania algorytmu mnozone
        # przez -1, aby wynik byl prawidlowy, nalezy z powrotem odwrucic
        self.okresl_kryterium_min_max()
        for result in sorted_list:
            print("najlepszy punkt: ", self.zbior_decyzji[result[0]])


    def wyznaczWspolczynnikSkorigowany(self):
        # dla wszystkich punktow niezdominowanych wyznacz wspolczynnik
        for index, wartosc in self.zbiorniezdominowanyZnormalizowany.items():
            odleglosc_idealna = 0
            odleglosc_antyidealna = 0

            # odleglosc idealna
            for i in range(len(wartosc)):
                odleglosc_idealna += self.waga_kryterium[i] * ((wartosc[i] - self.punkt_idealnyZnormalizowany[i])**2)

            # odleglosc antyidealna
            for i in range(len(wartosc)):
                odleglosc_antyidealna += self.waga_kryterium[i] * ((wartosc[i] - self.punkt_antyidealnyZnormalizowany[i]) ** 2)

            self.wspolczynniki_skorigowane.append([index, odleglosc_antyidealna/(odleglosc_antyidealna + odleglosc_idealna)])


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
            self.zbior_decyzjiZnormalizowany[index] = []
            for i in range(len(norma)):
                self.zbior_decyzjiZnormalizowany[index].append(wartosc[i]/norma[i])

        # znormalizuj wartosci w kolumnach zbioru niezdominowanego
        for index, wartosc in self.zbior_niezdominowany.items():
            self.zbiorniezdominowanyZnormalizowany[index] = []
            for i in range(len(norma)):
                self.zbiorniezdominowanyZnormalizowany[index].append(wartosc[i]/norma[i])


if __name__ == '__main__':
    TestClass = MetodaTopsis()

    # dostosuj kryteria minimalizacji/makssymalizacji
    TestClass.okresl_kryterium_min_max()

    TestClass.wyznaczZbiorNiezdominowany()
    print('zbior niezdominowany: ')
    print(TestClass.zbior_niezdominowany)

    TestClass.normalizujZbior()
    print(TestClass.zbior_decyzjiZnormalizowany)
    print('punkty niezdominowane znormalizowane: ')
    print(TestClass.zbiorniezdominowanyZnormalizowany)

    TestClass.wyznaczPunktIdealny()
    print('punkt idealny: ')
    print(TestClass.punkt_idealnyZnormalizowany)

    TestClass.wyznaczPunktAntyIdealny_nadir()
    print('punkt antyidealny: ')
    print(TestClass.punkt_antyidealnyZnormalizowany)

    TestClass.wyznaczWspolczynnikSkorigowany()
    print('wspl skorigowane: ')
    print(TestClass.wspolczynniki_skorigowane)

    print('ranking rozwiazan: ')
    TestClass.utworzRankingRozwiazan()
