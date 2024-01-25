from PyQt5 import  QtWidgets
from PyQt5.QtWidgets import QStackedWidget
import sys
import openpyxl

from screen import Screen

from MainWindow import Ui_MainScreen
from TopsisScreen import Ui_TopsisScreen
from ranking_screen import Ui_RankingScreen
from rsm_screen import Ui_RsmScreen
from sp_screen import Ui_SpScreen
from uta_screen import Ui_UtaScreen
from database import Ui_DatabaseScreen
from typing import Dict,Union,List
import pandas as pd


class Gui:
    '''
    klasa zarządzająca działaniem gui
    i wyświetlaniem poszczególnych ekranów
    '''
    def __init__(self,database) -> None:
        '''
        inicjalizacja ekranu
        ustalenie wielkości okna
        inicjalizacja stosu ekranów
        '''
        self.app = QtWidgets.QApplication(sys.argv)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setFixedHeight(876)
        self.stacked_widget.setFixedWidth(783)
        self.database = database

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
    
    def show_sp(self,criteria):
        window = QtWidgets.QMainWindow()
        Ui_SpScreen(window, self,criteria)
        self.stacked_widget.addWidget(window)
        self.stacked_widget.setCurrentWidget(window)
        self.stacked_widget.show()
    
    def show_uta(self,criteria):
        window = QtWidgets.QMainWindow()
        Ui_UtaScreen(window, self,criteria)
        self.stacked_widget.addWidget(window)
        self.stacked_widget.setCurrentWidget(window)
        self.stacked_widget.show()
    
    def show_ranking(self,method : Screen,criteria,ranking):
        window = QtWidgets.QMainWindow()
        Ui_RankingScreen(window,self,method,criteria,ranking)
        self.stacked_widget.addWidget(window)
        self.stacked_widget.setCurrentWidget(window)
        self.stacked_widget.show()
        
    def show_database(self):
        window = QtWidgets.QMainWindow()
        Ui_DatabaseScreen(window,self)
        self.stacked_widget.addWidget(window)
        self.stacked_widget.setCurrentWidget(window)
        self.stacked_widget.show()
            
        
    def run(self):
        self.show_main()
        sys.exit(self.app.exec_())
        

