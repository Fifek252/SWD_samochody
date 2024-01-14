from PyQt5 import  QtWidgets
from PyQt5.QtWidgets import QStackedWidget
import sys

from enum import Enum, auto

from MainWindow import Ui_MainScreen
from TopsisScreen import Ui_TopsisScreen

class Screen(Enum):
    MAIN = auto()
    TOPSIS = auto()
    RSM = auto()
    UTA = auto()
    SP = auto()

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
        app = QtWidgets.QApplication(sys.argv)
        widget = QStackedWidget()
        widget.setFixedHeight(876)
        widget.setFixedWidth(783)
        sys.exit(app.exec_())

    def show_screen(self, screen: Screen) -> None:
        window = QtWidgets.QMainWindow()
        if screen == Screen.MAIN:
            self.show_main(window)
        if screen == Screen.TOPSIS:
            self.show_topsis(window)


    def show_main(self, window):
        Ui_MainScreen(window, self)
        self.widget.addWidget(window)
        self.widget.setCurrentWidget(window)
        self.widget.show()

    def show_topsis(self, window):
        Ui_TopsisScreen(window, self)
        self.widget.addWidget(window)
        self.widget.setCurrentWidget(window)
        self.widget.show()


if __name__ == "__main__":
    import sys
    gui = Gui()
    gui.show_screen(Screen.MAIN)