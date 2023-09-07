import sys
import hashlib
from PyQt5 import QtGui
from login_ui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication ,QMessageBox
from PyQt5.QtCore import pyqtSignal


class login(QtWidgets.QWidget):

    login_successful = pyqtSignal(str,str)


    def __init__(self, parent=None):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)      
        self.ui.label_2.mouseMoveEvent = self.moveWindow
        self.ui.label_3.mouseMoveEvent = self.moveWindow
        self.ui.pushButton_2.clicked.connect(self.close)
        self.ui.pushButton.clicked.connect(self.loginn)
        self.ui.pushButton.setFocusPolicy(Qt.NoFocus)
        self.logged = False
        self.show()
        self.data = {}
        

    def loginn(self):
        msg = QMessageBox()
        username = self.ui.lineEdit.text().strip()
        password = self.ui.lineEdit_2.text().strip()
        self.read_pass()


        if username in self.data.keys():
            if self.hash_password(password) == self.data[username]['hash_password']:
                admin = self.data[username]['admin_rights']
                self.login_successful.emit(username,admin)
                self.write_pass()
            else:
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("ERROR") 
                msg.setText('niepoprawne hasło / login')
                msg.exec_()
        else:
             msg.setIcon(QMessageBox.Critical)
             msg.setWindowTitle("ERROR") 
             msg.setText('niepoprawne hasło / login')
             msg.exec_()


    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.clickPos = event.globalPos()


    def moveWindow(self,event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.clickPos)
            self.clickPos = event.globalPos()
            event.accept()

    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.loginn()
            

    def read_pass(self):
        with open('hasla.kld', 'r') as file:
            ppl = file.read().splitlines()
            for item in ppl: 
                item2 = item.split(',')
                if len(item2) >= 3:
                    self.data[item2[0]] = {'hash_password' : item2[1], 'admin_rights': item2[2]}


    def write_pass(self):
        with open('hasla.kld', 'w') as file:
            for item in self.data:
                file.write(item+',')
                for item2 in self.data[item]:
                   file.write(self.data[item][item2]+',')
                file.write('\n')
                   

    def hash_password(self,password_to_hash):

        h = hashlib.new('md5')
        password_to_hash = bytes(password_to_hash, 'csisolatingreek')
        h.update(password_to_hash)
        return h.hexdigest()
    
    
    def add_user(self,nazwa,haslo,admin_rights):

        haslo = self.hash_password(haslo)
        self.data[nazwa] = {'hash_password' : haslo, 'admin_rights': admin_rights}


    def del_user(self,nazwa):

        self.data.pop(nazwa)