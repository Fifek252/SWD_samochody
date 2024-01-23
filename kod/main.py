from gui.car import Cars
from topsis.topsis import MetodaTopsis
            
if __name__ == "__main__":
    database = Cars("bazadanych.xlsx", [False, True, False, False, True, True, False, False])
    database.update_parameters([False, True, False, False, True, True, False, False])
    Test = MetodaTopsis(database.get_parameters())
    print(Test.run_algorithm())