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
        self.show_screen(Screen.MAIN)
        sys.exit(self.app.exec_())

    def show_screen(self, screen: Screen) -> None:
        window = QtWidgets.QMainWindow()
        if screen == Screen.MAIN:
            self.show_main(window)
        if screen == Screen.TOPSIS:
            self.topsis_screen = window
            self.show_topsis(window)

    def show_main(self, window):
        Ui_MainScreen(window, self)
        if self.widget.indexOf(window) == -1:
            self.widget.addWidget(window)
        self.widget.setCurrentWidget(window)
        self.widget.show()

    def show_topsis(self, window):
        Ui_TopsisScreen(window, self)
        if self.widget.indexOf(window) == -1:
            self.widget.addWidget(window)
        self.widget.setCurrentWidget(window)
        self.widget.show()


if __name__ == "__main__":
    gui = Gui()
    