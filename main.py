from car import Cars
from topsis import MetodaTopsis
from safety_principle import SP


if __name__ == "__main__":
    database = Cars("bazadanych.xlsx")
    database.update_parameters(['Pojemność silnika', 'Przebieg', 'Średnie spalanie', 'Cena'])
    Test = MetodaTopsis(database.get_parameters(), [0.5, 1, 1, 0.2])
    print(Test.run_algorithm())


    A0 = [[480000, -50, 47000, 5.5]]
    A1 = [[121000, -88, 27000, 1.6]]

    solver = SP(database.get_parameters(), A0, A1)
    print(solver.get_rank())