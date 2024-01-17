from PyQt5 import  QtWidgets
from PyQt5.QtWidgets import QStackedWidget
import sys
import pandas as pd

from screen import Screen

from MainWindow import Ui_MainScreen
from TopsisScreen import Ui_TopsisScreen
from ranking_screen import Ui_RankingScreen
from rsm_screen import Ui_RsmScreen

class Gui:
    '''
    klasa zarządzająca działaniem gui
    i wyświetlaniem poszczególnych ekranów
    '''
    def __init__(self) -> None:
        '''
        inicjalizacja ekranu
        ustalenie wielkości okna
        inicjalizacja stosu ekranów
        '''
        self.app = QtWidgets.QApplication(sys.argv)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setFixedHeight(876)
        self.stacked_widget.setFixedWidth(783)
        self.database = pd.read_excel("kod\\gui\\test_data_base.xlsx")

    def show_main(self):
        window = QtWidgets.QMainWindow()
        Ui_MainScreen(window, self)
        self.stacked_widget.addWidget(window)
        self.stacked_widget.setCurrentWidget(window)
        self.stacked_widget.show()

    def show_topsis(self, criteria):
        window = QtWidgets.QMainWindow()
        Ui_TopsisScreen(window, self,criteria)
        self.stacked_widget.addWidget(window)
        self.stacked_widget.setCurrentWidget(window)
        self.stacked_widget.show()
        
    def show_rsm(self,criteria):
        window = QtWidgets.QMainWindow()
        Ui_RsmScreen(window, self,criteria)
        self.stacked_widget.addWidget(window)
        self.stacked_widget.setCurrentWidget(window)
        self.stacked_widget.show()
    
    def show_ranking(self,method : Screen,criteria):
        window = QtWidgets.QMainWindow()
        Ui_RankingScreen(window,self,method,criteria)
        self.stacked_widget.addWidget(window)
        self.stacked_widget.setCurrentWidget(window)
        self.stacked_widget.show()
            
        
    def run(self):
        self.show_main()
        sys.exit(self.app.exec_())
        

if __name__ == "__main__":
    gui = Gui()
    gui.run()
    