from PyQt5 import  QtWidgets
from PyQt5.QtWidgets import QStackedWidget
import sys

from screen import Screen

from MainWindow import Ui_MainScreen
from TopsisScreen import Ui_TopsisScreen

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
        self.widget = QStackedWidget()
        self.widget.setFixedHeight(876)
        self.widget.setFixedWidth(783)

    def show_main(self):
        window = QtWidgets.QMainWindow()
        Ui_MainScreen(window, self)
        if self.widget.indexOf(window) == -1:
            self.widget.addWidget(window)
        self.widget.setCurrentWidget(window)
        self.widget.show()

    def show_topsis(self, criteria):
        window = QtWidgets.QMainWindow()
        Ui_TopsisScreen(window, self,criteria)
        if self.widget.indexOf(window) == -1:
            self.widget.addWidget(window)
        self.widget.setCurrentWidget(window)
        self.widget.show()
        
    def run(self):
        self.show_main()
        sys.exit(self.app.exec_())
        

if __name__ == "__main__":
    gui = Gui()
    gui.run()
    