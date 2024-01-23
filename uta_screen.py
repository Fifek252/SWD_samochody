from PyQt5 import QtCore, QtGui, QtWidgets
from screen import Screen
from uta import UTA

INPUT_X = 30
INPUT_Y_START = 450

class Ui_UtaScreen:
    def __init__(self, UtaScreen,gui,criteria):
        self.gui = gui
        self.criteria = criteria
        self.trashcan = QtGui.QIcon("trashcan.png")

        self.centralwidget = QtWidgets.QWidget(UtaScreen)
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
        
        self.menu = QtWidgets.QPushButton(self.centralwidget)
        self.menu.setGeometry(QtCore.QRect(20, 360, 111, 41))
        self.menu.setObjectName("menu_uta")
        self.menu.clicked.connect(lambda: self.gui.show_main())
        
        UtaScreen.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(UtaScreen)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 783, 26))
        self.menubar.setObjectName("menubar")
        UtaScreen.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(UtaScreen)
        self.statusbar.setObjectName("statusbar")
        UtaScreen.setStatusBar(self.statusbar)
        
        self.make_interface()
        
        self.retranslateUi(UtaScreen)
        QtCore.QMetaObject.connectSlotsByName(UtaScreen)
    
    def retranslateUi(self, RankingScreen):
        _translate = QtCore.QCoreApplication.translate
        RankingScreen.setWindowTitle(_translate("UtaScreen", "UtaScreen"))
        self.tytul.setText(_translate("UtaScreen", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; color:#ffffff;\">Metoda UTA</span></p></body></html>"))
        self.menu.setText(_translate("UtaScreen", "Menu"))
        
    def make_interface(self):
        self.ranges = [0 for _ in self.criteria]
        self.set_ranges_lst = [0 for _ in self.criteria]
        self.labels = []
        
        self.ranges_label = QtWidgets.QLabel(self.centralwidget)
        self.ranges_label.setGeometry(INPUT_X,INPUT_Y_START-40,200,20)
        self.ranges_label.setObjectName("range_label")
        self.ranges_label.setText("Ilość przedziałów w kryterium:")
        self.ranges_label.setStyleSheet("color: white;")
        
        self.enter_idx = 1
        for i,crit in enumerate(sorted(self.criteria)):
            crit_label = QtWidgets.QLabel(self.centralwidget)
            crit_label.setGeometry(QtCore.QRect(INPUT_X, INPUT_Y_START+i*50, 140, 41))
            crit_label.setObjectName(crit)
            crit_label.setText(f"{crit}:")
            crit_label.setStyleSheet("color: white;")
            self.labels.append(crit_label)
            
            input = QtWidgets.QLineEdit(self.centralwidget)
            input.setGeometry(QtCore.QRect(INPUT_X+150,INPUT_Y_START+i*50,100,40))
            input.setObjectName(f"weight_{crit}")
            input.setStyleSheet("color: black;")
            input.setFont(QtGui.QFont("Arial",12))
            input.setText("")
            self.ranges[i] = input
            self.ranges[i].textChanged.connect(lambda _,idx = i: self.validate_range_edit(idx))
            
            self.enter_idx += 1
        
        self.enter = QtWidgets.QPushButton(self.centralwidget)
        self.enter.setGeometry(QtCore.QRect(INPUT_X+70,INPUT_Y_START+self.enter_idx*50-30,101,28))
        self.enter.setObjectName("enter")
        self.enter.setText("Zatwierdź")
        self.enter.clicked.connect(lambda: self.set_ranges())
        

    
    def validate_range_edit(self,idx):
        text = self.ranges[idx].text()
        try:
            number = int(text)
            if not (number > 0):
                raise ValueError
            self.ranges[idx].setStyleSheet("background-color: #00ff00;")
            return number
        except ValueError:
            if len(text) == 0:
                self.ranges[idx].setStyleSheet("background-color: #ffffff;")
            else:
                self.ranges[idx].setStyleSheet("background-color: #ff0000;")
            return None
    
    def validate_usefulness_edit(self,r,col):
        text = self.usefulness_fcn[r][col].text()
        try:
            number = float(text)
            if not (number > 0):
                raise ValueError
            if col == 0 and not (number > 0 and number < 1):
                raise ValueError
            self.usefulness_fcn[r][col].setStyleSheet("background-color: #00ff00;")
            
        except ValueError:
            if len(text) == 0:
                self.usefulness_fcn[r][col].setStyleSheet("background-color: #ffffff;")
            else:
                self.usefulness_fcn[r][col].setStyleSheet("background-color: #ff0000;")
            return None
    
    def set_ranges(self):
        flag = True
        for idx,inp in enumerate(self.ranges):
            text = inp.text()
            try:
                input = int(text)
                if input > 4:
                    input = 4
                self.set_ranges_lst[idx] = input + 1
            except:
                if flag is True:
                    self.error_ranges()
                    flag = False
                return 
        self._spawn_columns()
  
    def _spawn_columns(self):
        self.usefulness_fcn = []
        for row, nr_of_cols in enumerate(self.set_ranges_lst):
            usefulness_column = []
            for col in range(nr_of_cols):
                input = QtWidgets.QLineEdit(self.centralwidget)
                input.setGeometry(QtCore.QRect(INPUT_X + 300 + col*90,INPUT_Y_START+row*50 ,80,40))
                input.setObjectName(f"input_{row}{col}")
                input.setFont(QtGui.QFont("Arial",12))
                input.setText("")
                input.textChanged.connect(lambda _,colmn = col,r = row: self.validate_usefulness_edit(r,colmn))
                input.show()
                usefulness_column.append(input)
            self.usefulness_fcn.append(usefulness_column)      

        
        self.search = QtWidgets.QPushButton(self.centralwidget)
        self.search.setGeometry(QtCore.QRect(INPUT_X + 300,INPUT_Y_START+self.enter_idx*50-30,155,28))
        self.search.setText("Szukaj")
        font = QtGui.QFont("Arial",10)
        font.setBold(True)
        self.search.setFont(font)
        self.search.clicked.connect(lambda: self.do_uta())
        self.search.show()
        
  
    def error_ranges(self):
        msg = QtWidgets.QMessageBox()
        msg.setText("Liczba przedziałów musi być liczbą naturalną dodatnią.")
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.exec_()
    
    def error_first_row_sum(self):
        msg = QtWidgets.QMessageBox()
        msg.setText("Suma wartości z pierwszego rzędu musi wynosić 1.")
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.exec_()
    
    def error_give_all_inputs(self):
        msg = QtWidgets.QMessageBox()
        msg.setText("Proszę w każde okienko wpisać liczbę dodatnią.")
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.exec_()
        

    def go_to_ranking(self):
        self.final_usefulness = []
        for lst in self.usefulness_fcn:
            final_column = []
            for input in lst:
                try:
                    number = float(input.text())
                    final_column.append(number)
                    if not(number > 0):
                        raise ValueError
                except ValueError:
                    self.error_give_all_inputs()
                    return
            self.final_usefulness.append(final_column)
        first_row_sum = 0
        for lst in self.final_usefulness:
            first_row_sum += lst[0]
        if first_row_sum == 1:
            self.gui.show_ranking(Screen.UTA,self.criteria)
        else:
            self.error_first_row_sum()
            return
        
    def do_uta(self):
        self.gui.database.update_parameters(self.criteria)
        self.ranking = UTA(self.gui.database,self.usefulness_fcn)
        print(self.ranking.get_rank())
        
    