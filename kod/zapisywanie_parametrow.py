class Variant:
    def __init__(self):
        self.__minimalize = []               # przechowuje informacje czy minimalizować dane kryterium
        self.__criteria = []
        self.params = []                # lista zmodyfikowanych kryteriów (w zaleznosci od min/max)


    def update_parameters(self, parameters: dict[list[float]], minimalize: list[bool], criteria: list[bool]):
        self.__criteria = criteria
        self.__minimalize = minimalize


        for samochod in parameters.values():  #iteracja po listach parametrow samochodu

            nowe_kryteria = []  #wyznacz nowe kryteria (min/max/None)
            for index_kryterium, kryterium in enumerate(samochod):
                if criteria[index_kryterium]:
                    if minimalize[index_kryterium]:
                        nowe_kryteria.append(kryterium)
                    else:
                        nowe_kryteria.append(-kryterium)
                else:
                    nowe_kryteria.append(None)

            self.params.append(nowe_kryteria)

    def get_parameters(self):
        return [self.params, self.__criteria, self.__minimalize]

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
min = [True, True, False]
criteria = [True, True, True]
test_class = Variant()
test_class.update_parameters(zbior_decyzji, min, criteria)

print(test_class.params)