# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TopsisScreen.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from screen import Screen

INPUT_X = 30
INPUT_Y_START = 600

class Ui_TopsisScreen:
    def __init__(self, TopsisScreen,gui,criteria):
        self.gui = gui
        self.criteria = criteria
        
        TopsisScreen.setObjectName("TopsisScreen")
        TopsisScreen.resize(781, 878)
        self.centralwidget = QtWidgets.QWidget(TopsisScreen)
        self.centralwidget.setObjectName("centralwidget")
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 801, 881))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("kod\\gui\\background.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        
        self.tytul_topsis = QtWidgets.QLabel(self.centralwidget)
        self.tytul_topsis.setGeometry(QtCore.QRect(190, 450, 421, 61))
        self.tytul_topsis.setStyleSheet("border-color: rgb(159, 255, 124);")
        self.tytul_topsis.setObjectName("tytul_topsis")
        
        self.info_topsis = QtWidgets.QLabel(self.centralwidget)
        self.info_topsis.setGeometry(QtCore.QRect(10, 490, 761, 41))
        self.info_topsis.setObjectName("info_topsis")

        self.menu = QtWidgets.QPushButton(self.centralwidget)
        self.menu.setGeometry(QtCore.QRect(20, 400, 111, 41))
        self.menu.setObjectName("menu")
        self.menu.clicked.connect(lambda: self.gui.show_main())
        
        ''' Tworzenie pól na wpisywanie wag w zależności od zaznaczonych na MainWIndow kryteriów'''
        self.make_interface()
        
        self.rownowazne = QtWidgets.QCheckBox(self.centralwidget)
        self.rownowazne.setGeometry(INPUT_X,INPUT_Y_START-50,100,20)
        self.rownowazne.setStyleSheet("color: yellow")
        self.rownowazne.setObjectName("rowne_wagi")
        self.rownowazne.setText("Równoważne")
        self.rownowazne.stateChanged.connect(lambda: self.make_even_weights())
        
        self.weights_text = QtWidgets.QLabel(self.centralwidget)
        self.weights_text.setGeometry(INPUT_X+350,INPUT_Y_START,500,41)
        self.weights_text.setObjectName("wprowadzone_wagi")
        self.weights_text.setStyleSheet("color: white;")
        self.weights_text.setText(f"Wagi: {self.weights}\nSuma wag: {sum(self.weights)}")
        self.weights_text.setFont(QtGui.QFont("Arial",10))
        
        self.search = QtWidgets.QPushButton(self.centralwidget)
        self.search.setGeometry(QtCore.QRect(INPUT_X+350,INPUT_Y_START + 100,151,28))
        self.search.setText("Szukaj")
        font = QtGui.QFont("Arial",10)
        font.setBold(True)
        self.search.setFont(font)
        self.search.clicked.connect(lambda: self.go_to_ranking())
        
        TopsisScreen.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TopsisScreen)
        self.menubar.setGeometry(QtCore.QRect(0,0,783,26))
        self.menubar.setObjectName("menubar")
        TopsisScreen.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(TopsisScreen)
        self.statusbar.setObjectName("statusbar")
        TopsisScreen.setStatusBar(self.statusbar)

        self.retranslateUi(TopsisScreen)
        QtCore.QMetaObject.connectSlotsByName(TopsisScreen)

    def retranslateUi(self, TopsisScreen):
        _translate = QtCore.QCoreApplication.translate
        TopsisScreen.setWindowTitle(_translate("TopsisScreen", "TopsisScreen"))
        self.tytul_topsis.setText(_translate("TopsisScreen", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#ffffff;\">Metoda Topsis</span></p><p align=\"center\"><br/></p></body></html>"))
        self.info_topsis.setText(_translate("TopsisScreen", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600; color:#ffffff;\">Proszę nadać wagi wybranym kryteriom. Wagi muszą mieć łączną sumę 1!!!.<br/>Można też wybrać opcję, aby kryteria były równoważne.</span></p></body></html>"))
        self.menu.setText(_translate("TopsisScreen", "Menu"))
   
    def make_interface(self):
        self.inputs = [0 for _ in self.criteria]
        self.ok_buttons = []
        self.crits = []
        self.weights = [0 for _ in self.criteria]
        self.sum_weights = sum(self.weights)
        
        for i,crit in enumerate(sorted(self.criteria)):
            crit_label = QtWidgets.QLabel(self.centralwidget)
            crit_label.setGeometry(QtCore.QRect(INPUT_X, INPUT_Y_START+i*50, 140, 41))
            crit_label.setObjectName(crit)
            crit_label.setText(f"{crit}:")
            crit_label.setStyleSheet("color: white;")
            self.crits.append(crit_label)
            
            weight_input = QtWidgets.QLineEdit(self.centralwidget)
            weight_input.setGeometry(QtCore.QRect(INPUT_X+150,INPUT_Y_START+i*50,100,40))
            weight_input.setObjectName(f"weight_{crit}")
            weight_input.setStyleSheet("color: black;")
            weight_input.setFont(QtGui.QFont("Arial",12))
            weight_input.setText("")
            self.inputs[i] = weight_input
            self.inputs[i].textChanged.connect(lambda _,idx = i: self.inputs[idx].setStyleSheet("background-color: #ffffff;"))
            
            ok = QtWidgets.QPushButton(self.centralwidget)
            ok.setGeometry(QtCore.QRect(INPUT_X+255, INPUT_Y_START+i*50, 30, 30))
            ok.setObjectName(f"ok_{crit}")
            ok.setText(f"OK")
            self.ok_buttons.append(ok)
            ok.clicked.connect(lambda _,idx = i: self.assign_weight(idx))
    
    def make_even_weights(self):
        if self.rownowazne.isChecked():
            weight = 1/(len(self.criteria))
            for i in range(len(self.criteria)):
                self.inputs[i].setEnabled(False)
                self.ok_buttons[i].setEnabled(False)
            self.weights = [round(weight,3) for _ in self.criteria]
            self.sum_weights = 1
            self.weights_text.setText(f"Wagi: {self.weights}\nSuma wag: {self.sum_weights}")
        else:
            for i in range(len(self.criteria)):
                self.inputs[i].setEnabled(True)
                self.inputs[i].setText(f"{self.inputs[i].text()}")
                self.inputs[i].setStyleSheet("background-color: #ffffff;")
                self.ok_buttons[i].setEnabled(True)
            self.weights = [0 for _ in self.criteria]
            self.sum_weights = sum(self.weights)
            self.weights_text.setText(f"Wagi: {self.weights}\nSuma wag: {self.sum_weights}")

    def assign_weight(self,idx):
        x = self.inputs[idx].text()
        x = self.validate_weight(idx,x)
        if x is not None:
            self.inputs[idx].setStyleSheet("background-color: #00ff00;")
            self.weights[idx] = x
            self.sum_weights = round(sum(self.weights),3)
            self.weights_text.setText(f"Wagi: {self.weights}\nSuma wag: {self.sum_weights}")

    def validate_weight(self,idx,weight):
        try:
            number = float(weight)
            if not (number > 0 and number < 1):
                raise ValueError
            return number
        except ValueError:
            self.error_weight(idx)
            return None
    
    def error_weight(self,idx):
        msg = QtWidgets.QMessageBox()
        self.inputs[idx].setStyleSheet("background-color: #ffffff;")
        msg.setText("Proszę podać liczbe między 0 a 1.\nSeparatorem dziesiętnym jest kropka")
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.exec_()
    
    def error_sum(self,error):
        msg = QtWidgets.QMessageBox()
        msg.setText(error)
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.exec_()

    def go_to_ranking(self):
        if self.sum_weights == 1 and 0 not in self.weights:
            self.gui.show_ranking(Screen.TOPSIS)
        elif self.sum_weights != 1:
            self.error_sum("Suma wag kryteriów musi wynosić 1,\naby można było zastosować metodę topsis")
        elif 0 in self.weights:
            self.error_sum("Proszę nadać niezerową wagę wszystkim wybranym kryteriom.\nW celu usunięcia kryterium można wrócić do Menu.")

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     TopsisScreen = QtWidgets.QWidget()
#     ui = Ui_TopsisScreen()
#     ui.setupUi(TopsisScreen)
#     TopsisScreen.show()
#     sys.exit(app.exec_())
