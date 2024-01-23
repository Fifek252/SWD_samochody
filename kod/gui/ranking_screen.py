# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ranking_screen.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from screen import Screen
from gui.car import Cars

class Ui_RankingScreen:
    def __init__(self, RankingScreen,gui,method,criteria,database):
        self.gui = gui
        self.method = method
        self.criteria = criteria
        self.ranking = []
        self.show_nr = 10                   # Pokaż tyle aut z czołówki rankingu
        
        RankingScreen.setObjectName("RankingScreen")
        RankingScreen.resize(781, 878)
        self.centralwidget = QtWidgets.QWidget(RankingScreen)
        self.centralwidget.setObjectName("centralwidget")
        
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 801, 881))
        self.background.setText("")
        self.background.setPixmap(QtGui.QPixmap("kod\\gui\\background.jpg"))
        self.background.setScaledContents(True)
        self.background.setObjectName("label")
        
        self.tytul = QtWidgets.QLabel(self.centralwidget)
        self.tytul.setGeometry(QtCore.QRect(170, 390, 421, 61))
        self.tytul.setStyleSheet("border-color: rgb(159, 255, 124);")
        self.tytul.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tytul.setObjectName("tytul")
        
        self.menu = QtWidgets.QPushButton(self.centralwidget)
        self.menu.setGeometry(QtCore.QRect(20, 317, 111, 41))
        self.menu.setObjectName("menu")
        self.menu.clicked.connect(lambda: self.gui.show_main())
        
        RankingScreen.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RankingScreen)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 759, 26))
        self.menubar.setObjectName("menubar")
        RankingScreen.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RankingScreen)
        self.statusbar.setObjectName("statusbar")
        RankingScreen.setStatusBar(self.statusbar)
        
        self.method_type = QtWidgets.QLabel(self.centralwidget)
        self.method_type.setGeometry(QtCore.QRect(30, 480, 200, 16))
        self.method_type.setObjectName("method_type")
        self.method_type.setFont(QtGui.QFont("Arial",8))
        self.method_type.setStyleSheet("color: white;")
        self.method_type.setText(f"Wynik metody: {self.method.name}")
        
        self.return_btn = QtWidgets.QPushButton(self.centralwidget)
        self.return_btn.setGeometry(QtCore.QRect(20, 360, 111, 41))
        self.return_btn.setObjectName("return_btn")
        self.return_btn.setText("Powrót")
        self.return_btn.clicked.connect(lambda: self.back_to_method())
        
        ''' Teraz kod zależny od tego, z jakiego ekranu przychodzimy, czyli którą metodę wybraliśmy
        Na razie zrobiłem tylko dla topsis, i to nic nie liczy tylko printuje 10 pierwszych rzeczy z tej bazy'''
        if self.method == Screen.TOPSIS:
            for _,row in self.gui.database.head(self.show_nr).iterrows():
                self.ranking.append(row.tolist())
            self.display_ranking()
            
        elif self.method == Screen.RSM:
            for _,row in self.gui.database.head(self.show_nr).iterrows():
                self.ranking.append(row.tolist())
            self.display_ranking()
        
        elif self.method == Screen.SP:
            for _,row in self.gui.database.head(self.show_nr).iterrows():
                self.ranking.append(row.tolist())
            self.display_ranking()
        
        elif self.method == Screen.UTA:
            for _,row in self.gui.database.head(self.show_nr).iterrows():
                self.ranking.append(row.tolist())
            self.display_ranking()
        

        self.retranslateUi(RankingScreen)
        QtCore.QMetaObject.connectSlotsByName(RankingScreen)

    def retranslateUi(self, RankingScreen):
        _translate = QtCore.QCoreApplication.translate
        RankingScreen.setWindowTitle(_translate("RankingScreen", "RankingScreen"))
        self.tytul.setText(_translate("RankingScreen", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#ffffff;\">Ranking</span></p></body></html>"))
        self.menu.setText(_translate("RankingScreen", "Menu"))
    
    def display_ranking(self):
        self.ranking_list = QtWidgets.QLabel(self.centralwidget)
        self.ranking_list.setGeometry(250,480,100,200)
        self.ranking_list.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        to_display = "\n".join(" | ".join(map(str, row)) for row in self.ranking)
        self.ranking_list.setText(to_display)
        self.ranking_list.setStyleSheet("color: white;")
        
    def back_to_method(self):
        if self.method == Screen.TOPSIS:
            self.gui.show_topsis(self.criteria)
        elif self.method == Screen.RSM:
            self.gui.show_rsm(self.criteria)
        elif self.method == Screen.SP:
            self.gui.show_sp(self.criteria)
        elif self.method == Screen.UTA:
            self.gui.show_uta(self.criteria)