# -*- coding: utf-8 -*-

# RsmScreen implementation generated from reading ui file 'rsm_screen.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from screen import Screen

from rsm import RSM

INPUT_X = 30
INPUT_Y_START = 450
ASPIRACJE_TEXT = "Aktualny zbiór punktów aspiracji: "
STATUS_QUO_TEXT = "Aktualny zbiór punktów status-quo: "
MAX_POINTS = 5

class Point:
    def __init__(self,point : list,criteria_chosen):
        self.point = point
        self.criteria_chosen = criteria_chosen
        print(self.criteria_chosen)
        self.minimize()

        
    def minimize(self):

        for idx,val in enumerate(self.point):
            if self.criteria_chosen[idx]  in ['Maksymalna prędkość', 'Pojemność bagażnika', 'Moc silnika', 'Pojemność silnika']:
                self.point[idx] = -val
                
    def get_point(self):
        return self.point

class Ui_RsmScreen:
    def __init__(self, RsmScreen,gui,criteria):
        self.criteria = sorted(criteria)
        self.gui = gui
        self.trashcan = QtGui.QIcon("trashcan.png")
        RsmScreen.setObjectName("RsmScreen")
        RsmScreen.resize(781, 878)
        
        self.centralwidget = QtWidgets.QWidget(RsmScreen)
        self.centralwidget.setObjectName("centralwidget")
        
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 801, 881))
        self.background.setText("")
        self.background.setPixmap(QtGui.QPixmap("background.jpg"))
        self.background.setScaledContents(True)
        self.background.setObjectName("background")
        
        self.tytul = QtWidgets.QLabel(self.centralwidget)
        self.tytul.setGeometry(QtCore.QRect(180, 400, 421, 61))
        self.tytul.setStyleSheet("border-color: rgb(159, 255, 124);")
        self.tytul.setObjectName("tytul")
        
        ''' Napisać funkcje tworzące pola na tworzenie punktów aspiracji i status quo. Można przerobić interfejs dla topsis.'''
        self.make_interface()
        
        self.status_quo = QtWidgets.QLabel(self.centralwidget)
        self.status_quo.setGeometry(QtCore.QRect(INPUT_X + 460, INPUT_Y_START+50, 220, 130))
        self.status_quo.setObjectName("status_quo")
        self.status_quo.setText(STATUS_QUO_TEXT+"\n[]")
        self.status_quo.setStyleSheet("color: white;")
        self.status_quo.setFont(QtGui.QFont("Arial",8))
        self.status_quo.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        
        self.aspiracje = QtWidgets.QLabel(self.centralwidget)
        self.aspiracje.setGeometry(QtCore.QRect(INPUT_X + 460, INPUT_Y_START+200, 220, 130))
        self.aspiracje.setObjectName("aspiracje")
        self.aspiracje.setText(ASPIRACJE_TEXT +"\n[]")
        self.aspiracje.setStyleSheet("color: white;")
        self.aspiracje.setFont(QtGui.QFont("Arial",8))
        self.aspiracje.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        
        self.menu = QtWidgets.QPushButton(self.centralwidget)
        self.menu.setGeometry(QtCore.QRect(20, 320, 111, 41))
        self.menu.setObjectName("menu_rsm")
        self.menu.clicked.connect(lambda: self.gui.show_main())
        
        self.type_info = QtWidgets.QLabel(self.centralwidget)
        self.type_info.setGeometry(INPUT_X+70,INPUT_Y_START-75,140,20)
        self.type_info.setText("Utwórz punkt:")
        self.type_info.setStyleSheet("color: white;")
        self.type_info.setFont(QtGui.QFont("Arial",8))
        
        self.clear_asp = QtWidgets.QPushButton(self.centralwidget)
        self.clear_asp.setGeometry(QtCore.QRect(INPUT_X+420,INPUT_Y_START+200,30,30))
        self.clear_asp.setIcon(self.trashcan)
        self.clear_asp.setIconSize(self.trashcan.actualSize(0.8*self.clear_asp.size()))
        self.clear_asp.clicked.connect(lambda: self.clear_asp_points())
        
        self.clear_quo = QtWidgets.QPushButton(self.centralwidget)
        self.clear_quo.setGeometry(QtCore.QRect(INPUT_X+420,INPUT_Y_START+50,30,30))
        self.clear_quo.setIcon(self.trashcan)
        self.clear_quo.setIconSize(self.trashcan.actualSize(0.8*self.clear_quo.size()))
        self.clear_quo.clicked.connect(lambda: self.clear_quo_points())
        
        RsmScreen.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RsmScreen)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 783, 26))
        self.menubar.setObjectName("menubar")
        RsmScreen.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RsmScreen)
        self.statusbar.setObjectName("statusbar")
        RsmScreen.setStatusBar(self.statusbar)

        self.retranslateUi(RsmScreen)
        QtCore.QMetaObject.connectSlotsByName(RsmScreen)

    def retranslateUi(self, RsmScreen):
        _translate = QtCore.QCoreApplication.translate
        RsmScreen.setWindowTitle(_translate("RsmScreen", "RsmScreen"))
        self.tytul.setText(_translate("RsmScreen", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#ffffff;\">Metoda RSM</span></p><p align=\"center\"><br/></p></body></html>"))

        self.menu.setText(_translate("RsmScreen", "Menu"))
        
    def make_interface(self):
        self.quo_list = [0 for _ in self.criteria]
        self.asp_list = [0 for _ in self.criteria]
        self.quo_points = []
        self.asp_points = []
        self.inputs = [0 for _ in self.criteria]
        self.crits = []

        self.asp_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.asp_checkbox.setGeometry(QtCore.QRect(INPUT_X,INPUT_Y_START-50,140,41))
        self.asp_checkbox.setObjectName("asp_checkbox")
        self.asp_checkbox.setText("Aspiracji")
        self.asp_checkbox.setStyleSheet("color: yellow;")
        self.asp_checkbox.stateChanged.connect(lambda: self.switch_aspiration())
        
        self.quo_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.quo_checkbox.setGeometry(QtCore.QRect(INPUT_X+140,INPUT_Y_START-50,140,41))
        self.quo_checkbox.setObjectName("quo_checkbox")
        self.quo_checkbox.setText("Status-quo")
        self.quo_checkbox.setStyleSheet("color: yellow;")
        self.quo_checkbox.stateChanged.connect(lambda: self.switch_quo())
        
        self.search = QtWidgets.QPushButton(self.centralwidget)
        self.search.setGeometry(QtCore.QRect(345, 810,100,28))
        self.search.setText("Szukaj")
        font = QtGui.QFont("Arial",10)
        font.setBold(True)
        self.search.setFont(font)
        self.search.clicked.connect(lambda: self.do_rsm())
        
        self.enter_idx = 1
        for i,crit in enumerate(sorted(self.criteria)):
            crit_label = QtWidgets.QLabel(self.centralwidget)
            crit_label.setGeometry(QtCore.QRect(INPUT_X, INPUT_Y_START+i*50, 140, 41))
            crit_label.setObjectName(crit)
            crit_label.setText(f"{crit}:")
            crit_label.setStyleSheet("color: white;")
            self.crits.append(crit_label)
            
            input = QtWidgets.QLineEdit(self.centralwidget)
            input.setGeometry(QtCore.QRect(INPUT_X+150,INPUT_Y_START+i*50,100,40))
            input.setObjectName(f"weight_{crit}")
            input.setStyleSheet("color: black;")
            input.setFont(QtGui.QFont("Arial",12))
            input.setText("")
            input.setEnabled(False)
            self.inputs[i] = input
            self.inputs[i].textChanged.connect(lambda _,idx = i: self.validate_input_edit(idx))
            
            self.enter_idx += 1
            
        self.enter = QtWidgets.QPushButton(self.centralwidget)
        self.enter.setGeometry(QtCore.QRect(INPUT_X+70,INPUT_Y_START+self.enter_idx*50-30,101,28))
        self.enter.setObjectName("enter")
        self.enter.setText("Wprowadż")
        self.enter.clicked.connect(lambda: self.create_point())

    def switch_aspiration(self):
        if self.asp_checkbox.isChecked():
            self.quo_checkbox.setChecked(False)
        self.enable_inputs()
    
    def switch_quo(self):
        if self.quo_checkbox.isChecked():
            self.asp_checkbox.setChecked(False)
        self.enable_inputs()

    def create_point(self):
        flag = True
        for idx,inp in enumerate(self.inputs):
            text = inp.text()
            try:
                input = float(text)
            except:
                self.error_input_type()
                return 
            if self.asp_checkbox.isChecked():
                if len(self.asp_points) < MAX_POINTS:
                    self.update_aspiration_points(idx,input)
                    self.flag = False
                elif flag is True:
                    self.error_too_many_points()
                    flag = False
            elif self.quo_checkbox.isChecked():
                if len(self.quo_points) < MAX_POINTS:
                    self.update_status_quo_points(idx,input)
                elif flag is True:
                    self.error_too_many_points()
                    flag = False
                                
    def validate_input_edit(self,idx):
        text = self.inputs[idx].text()
        try:
            number = float(text)
            self.inputs[idx].setStyleSheet("background-color: #00ff00;")
            return number
        except ValueError:
            if len(text) == 0:
                self.inputs[idx].setStyleSheet("background-color: #ffffff;")
            else:
                self.inputs[idx].setStyleSheet("background-color: #ff0000;")
            return None
    
    def error_input_type(self):
        msg = QtWidgets.QMessageBox()
        msg.setText("Wszystkie kryteria muszą być liczbą dodatnią.")
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.exec_()
        
    def enable_inputs(self):
        if self.asp_checkbox.isChecked() or self.quo_checkbox.isChecked():
            for idx in range(len(self.criteria)):
                self.inputs[idx].setEnabled(True)
            self.enter.setEnabled(True)
        else:
            for idx in range(len(self.criteria)):
                self.inputs[idx].setEnabled(False)
            self.enter.setEnabled(False)
            
    def update_aspiration_points(self,idx,input):
        self.asp_list[idx] = input
        if  0 not in self.asp_list and len(self.asp_points) < MAX_POINTS:
            point = Point(self.asp_list,self.criteria)
            self.asp_points.append(point.get_point())
            self.asp_list = [0 for _ in self.criteria]
            self.aspiracje.setText(ASPIRACJE_TEXT + '\n'+ '\n'.join(map(str,self.asp_points)))
            for text_edit in self.inputs:
                text_edit.setStyleSheet("background-color: #ffffff;")
                text_edit.clear()
            
    def update_status_quo_points(self,idx,input):
        self.quo_list[idx] = input
        if  0 not in self.quo_list and len(self.quo_points) < MAX_POINTS:
            point = Point(self.quo_list,self.criteria)
            self.quo_points.append(point.get_point())
            self.quo_list = [0 for _ in self.criteria]
            self.status_quo.setText(STATUS_QUO_TEXT + '\n'+ '\n'.join(map(str,self.quo_points)))
            for text_edit in self.inputs:
                text_edit.setStyleSheet("background-color: #ffffff;")
                text_edit.clear()
    
    def error_too_many_points(self):
        msg = QtWidgets.QMessageBox()
        msg.setText(f"Można stworzyc maksymalnie {MAX_POINTS} punktów\naspiracji i status-quo")
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.exec_()
    
    def error_zero_points(self):
        msg = QtWidgets.QMessageBox()
        msg.setText("Proszę utworzyć przynajmniej 1 punkt aspiracji i status-quo")
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.exec_()

    def go_to_ranking(self):
        if len(self.asp_points) >= 1 and len(self.quo_points) >= 1:
            self.gui.show_ranking(Screen.RSM,self.criteria)
        else:
            self.error_zero_points()
    
    def clear_asp_points(self):
        self.asp_points.clear()
        self.aspiracje.setText(ASPIRACJE_TEXT +"\n[]")
        
    def clear_quo_points(self):
        self.quo_points.clear()
        self.status_quo.setText(STATUS_QUO_TEXT +"\n[]")
        
    def do_rsm(self):
        self.gui.database.update_parameters(self.criteria)
        self.ranking = RSM(self.gui.database,self.quo_points,self.asp_points)
        print(self.ranking.get_rank())