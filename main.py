from gui import Gui
from car import Cars

if __name__ == "__main__":
    database = Cars("bazadanych.xlsx")
    gui = Gui(database)
    gui.run()