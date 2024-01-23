from car import Cars
from topsis import MetodaTopsis

if __name__ == "__main__":
    database = Cars("bazadanych.xlsx")
    database.update_parameters(['Pojemność silnika', 'Przebieg', 'Średnie spalanie', 'Cena'])
    Test = MetodaTopsis(database.get_parameters())
    print(Test.run_algorithm())