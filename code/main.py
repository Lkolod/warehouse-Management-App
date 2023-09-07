
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow  
from Custom_Widgets.Widgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView
from data import *
from login_form import *
from dialog3_functional import *
from dialog4_functional import *
from guii_interface import *
from dodaj_func import *
from usun_func import *
from logs import *
from data_log import *

class invalidFormat(Exception):
    "Raised when the format of the data is wrong"
    pass

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)

        self.data5 = pandasModel(df)
        #for displaying data
        self.data = pandasModel(df2)
        #for filtering by the nr 
        self.data3 = pandasModel(df4)
        #for filtering by name
        self.data2 = pandasModel(df3)

        

        log_file = 'logs.log'
        max_log_entries = 200

        self.data_disp_log = log_model(log_file,max_log_entries)

        # Configure logging
        log_handler = logging2(log_file, max_log_entries)
        log_formatter = logging.Formatter('%(asctime)s; %(message)s', datefmt='%Y-%m-%d %H:%M')
        log_handler.setFormatter(log_formatter)

        self.logger = logging.getLogger('my_logger')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(log_handler)


        self.user = None
        self.nrprodcenta = None
        self.sel_row = None
        self.sel_column = None

        ### login form 
        self.loginn = login()
        self.ui = Ui_MainWindow()

        ### if username and password is correct switch to the main window
        self.loginn.login_successful.connect(self.switch_window)
  
        self.ui.setupUi(self)
        self.ui.tableView.setModel(self.data)
        self.ui.tableView2.setModel(self.data_disp_log)
        
        # disable the selection of a button using tab key
        self.ui.pushButton.setFocusPolicy(Qt.NoFocus)
        self.ui.open_close_side_bar_btn.setFocusPolicy(Qt.NoFocus)
        self.ui.pushButton_3.setFocusPolicy(Qt.NoFocus)
        self.ui.pushButton_5.setFocusPolicy(Qt.NoFocus)
        self.ui.pushButton_6.setFocusPolicy(Qt.NoFocus)
        self.ui.pushButton_7.setFocusPolicy(Qt.NoFocus)
        self.ui.pushButton_8.setFocusPolicy(Qt.NoFocus)
        self.ui.wyloguj.setFocusPolicy(Qt.NoFocus)
        self.ui.historia.setFocusPolicy(Qt.NoFocus)
        #Left Menu toggle button
        self.ui.open_close_side_bar_btn.clicked.connect(lambda: self.slideLeftMenu())
        
        
        ## resizing the header
        self.ui.tableView.setColumnWidth(0, 600)
        self.ui.tableView.setColumnWidth(2, 150)

        self.ui.lineEdit.textChanged.connect(self.filter)
        self.ui.lineEdit.textChanged.connect(self.filter_for_log)
        self.ui.lineEdit_2.textChanged.connect(self.filter2)
        self.ui.lineEdit_2.returnPressed.connect(self.on_enter_pressed)

        ################################
        # conecct the back button and the selection of form page
        self.ui.pushButton.clicked.connect(self.go_back)
        ###########################
        # new item button
        self.ui.pushButton_3.clicked.connect(self.form_page)


        ##################################
        #push button of page 2 "akceptuj" and "anuluj
        self.ui.pushButton_2.clicked.connect(self.accept)
        self.ui.pushButton_7.clicked.connect(self.go_back)
        
        # connect to the row selection
        self.ui.tableView.selectionModel().selectionChanged.connect(self.sel_change)

        self.data5.dataChanged.connect(self.save_changes_table)
        self.data5.wrongDataEntered.connect(lambda: self.create_war_mess('podaj właściwe dane','error',12))
        self.data5.dataChanged2.connect(self.create_log)

        ############# pobierz button
        self.ui.pushButton_6.clicked.connect(self.pobierz)
        self.ui.pushButton_5.clicked.connect(self.wprowadz)

        self.ui.pushButton_8.clicked.connect(self.toggle_edit_mode)
        self.edit_mode = False
        self.update_edit_mode()

        ############ wyloguj button
        self.ui.wyloguj.clicked.connect(self.log_out)


        ############ historia button 
        self.ui.historia.clicked.connect(self.hisory_page)

        ####### dodaj i usuń uzytkownika button

        self.ui.dodaj.clicked.connect(self.new_user)
        self.ui.usun.clicked.connect(self.delete_user)
        self.data_disp_log.data_changed.connect(self.update_table_view)
        self.add_items_magazyn()

        self.ui.comboBox_m.currentTextChanged.connect(self.add_coresponding_item)
        

    def add_items_magazyn(self):
        self.item = ['A','B','C']
        self.ui.comboBox_m.addItems(self.item)
        self.ui.comboBox_entity.addItems(['a','aa','b','bb','c','cc'])


    def add_coresponding_item(self):
        items_for_A = ['a','aa','b','bb','c','cc']
        items_for_B = ['d','dd','e','ee','f','ff']
        items_for_C = ['g','gg','h','hh','i','ii']
        
        if self.ui.comboBox_m.currentText() == self.item[0]:
            self.ui.comboBox_entity.clear()
            self.ui.comboBox_entity.addItems(items_for_A)

        elif self.ui.comboBox_m.currentText() == self.item[1]:
            self.ui.comboBox_entity.clear()
            self.ui.comboBox_entity.addItems(items_for_B)

        elif self.ui.comboBox_m.currentText() == self.item[2]:
            self.ui.comboBox_entity.clear()
            self.ui.comboBox_entity.addItems(items_for_C)
        else:
            self.ui.comboBox_entity.clear()


    def create_log_mes(self,message):
        self.logger.info(message)
        self.data_disp_log.refresh_data()
        self.ui.tableView2.setModel(self.data_disp_log)

    def update_table_view(self):
        self.ui.tableView2.viewport().update()

    def create_log(self,old_val,row,col,new_val):
        Nazwa,stan,Magazyn,Regał = self.data5.getDatabyRow(row)
        column = self.data5.get_col_name(col)
        self.create_log_mes('dokonano zmiany w : {nazwa} zamieniono {old_val} na {new_val} ({column})| uzytkownik: {user}'.format(nazwa = Nazwa,old_val=old_val,new_val=new_val,column=column, user = self.user))


    
    def save_changes_table(self):
   
            df2.update(self.data5._data[['Nazwa', 'Nr części', 'Stan magazynowy', 'magazyn', 'regał']])
            df3.update(self.data5._data[['Nazwa']])
            df4.update(self.data5._data[['Nr części', 'Nr części producenta']])

            self.data.updateModel(self.data5._data)
            self.data2.updateModel(self.data5._data)
            self.data3.updateModel(self.data5._data)
            self.data5.save()
        
   
    def toggle_edit_mode(self):
        self.ui.tableView.clearSelection()
        self.edit_mode = not self.edit_mode
        self.update_edit_mode()
        

    def new_user(self):
        self.open_new_user_dialog()
    

    def open_new_user_dialog(self):
        dialog = dodaj(self)
        dialog.setModal(True)
        dialog.show()
        dialog.ui.comboBox.setStyleSheet("background-color: #ffffff")
        dialog.ui.buttonBox.accepted.connect(lambda: self.add_new_user(dialog.ui.lineEdit.text(),dialog.ui.lineEdit_2.text(),dialog.ui.comboBox.currentText()))
        dialog.exec_()


    def add_new_user(self,name, password,rights):
        if rights == 'administrator':
            rights = '1'
        else:
            rights = '0'

        if ',' not in name:
            if name != '' and password !='':
                if name not in self.loginn.data.keys():
                    self.loginn.add_user(name,password,rights)
                    text = 'pomyślnie utworzono użytkownika: ' +name + '   hasło: '+password
                    self.loginn.write_pass()
                    self.create_inf_mess(text,'dodano użytkownika',10)
                    self.create_log_mes('dodano uzytkownika: {nazwa} | uzytkownik: {user}'.format(nazwa = name, user = self.user))
                
                else:
                    text = 'podany login już istnieje'
                    self.create_war_mess(text,'errors',10)
            else:
                text = 'haslo/nazwa nie może być puste'
                self.create_war_mess(text,'errors',10)

        else:
            text = 'nazwa nie może zawierać znaku: , '
            self.create_war_mess(text,'errors',10)


    def delete_user(self):
        self.open_delete_user_dialog()
 

    def delete_userr(self,text):
        self.loginn.del_user(text)
        text2 = 'pomyślnie usunięto  użytkownika: ' +text
        self.create_log_mes('usunieto uzytkownika: {nazwa} | uzytkownik: {user}'.format(nazwa = text, user = self.user))
        self.loginn.write_pass()
        self.create_inf_mess(text2,'usunięto użytkownika',10)
  

    def open_delete_user_dialog(self):
        dialog = usun(self)
        dialog.setModal(True)
        dialog.show()
        
        for item in self.loginn.data.keys():
            if self.loginn.data[item]['admin_rights'] != '2':
                dialog.ui.comboBox.addItem(item)
                
        dialog.ui.comboBox.setStyleSheet("background-color: #ffffff")
        dialog.ui.buttonBox.accepted.connect(lambda: self.delete_userr(dialog.ui.comboBox.currentText()))
        dialog.exec_()


    def update_edit_mode(self):
        
        if self.edit_mode:
            
            # Switch to "edit mode"
            self.ui.tableView.setModel(self.data5)
            self.ui.tableView.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
            self.ui.pushButton_8.setStyleSheet(
                """
                QPushButton {
                    color: #7393B3;
                }
                QPushButton:hover {
                    color: #7393B3;  /* Change the hover color to red */
                }
                """
            )
            
        
        else:
            
            # Switch to "view mode"
            self.ui.tableView.setModel(self.data)
            self.ui.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.ui.pushButton_8.setStyleSheet(
                """
                QPushButton {
                    color: #ffffff;  /* Set the default text color for the button */
                }
                
                QPushButton:hover {
                    color: #7393B3;  /* Change the hover color to red */
                }
                """
            )
        self.ui.tableView.selectionModel().selectionChanged.connect(self.sel_change)
        self.ui.tableView.clearSelection()

    
    #function which return selected rows in table
    def sel_change(self, selected):
        if selected.indexes():
        # Get the row and column of the selected index
            self.selected_index = selected.indexes()[0]
            self.sel_row =  self.selected_index.row()
            self.sel_column =  self.selected_index.column()
            self.original_data = self.data5.getItem(self.sel_row, self.sel_column)

        else:
            self.sel_row = None
            self.sel_column = None
            self.original_data = None


    def wprowadz(self):
        if self.sel_row != None:
            self.open_dialog_4_wyprowadz()
            
        else:
            text = "brak zaznaczonego rzędu"
            title = "błąd"
            self.create_war_mess(text,title,10)

 
    def pobierz(self):
        
        if self.sel_row != None:
            self.open_dialog_4()
           
        else:

            text = "brak zaznaczonego rzędu"
            title = "błąd"
            self.create_war_mess(text,title,10)


    def save_changes(self,ilosc,stan,nazwa):
 
        if str(ilosc).isnumeric():
            if int(ilosc) > int(stan):
                text = "Zbyt mały stan magazynowy"
                self.create_war_mess(text,'błąd ilości',10)

            else:
                self.data.change_qty(self.sel_row,-int(ilosc))
                self.data5.change_qty(self.sel_row,-int(ilosc))
                self.data5.save()
                
                self.create_log_mes('pobrano z magazynu {nazwa} w ilosci: {ilosc} | uzytkownik: {user}'.format(nazwa = nazwa, ilosc = ilosc, user = self.user))
                text = "pomyślnie pobrano "+ str(ilosc) +' szt.'
                title = "pobierz z magazynu"   
                self.create_inf_mess(text,title,12)    
   
        else:
            text = "w polu ilość do pobrania wpisz wartosc numeryczną"
            title = "błąd numeryczny"
            self.create_war_mess(text,title,10)


    def save_changes2(self,ilosc,nazwa):
 
        if str(ilosc).isnumeric():
 
            self.data.change_qty(self.sel_row,int(ilosc))
            self.data5.change_qty(self.sel_row,int(ilosc))
            self.data5.save()
            text = "pomyślnie wprowadzono "+ str(ilosc) +' szt.'
            self.create_log_mes('wprowadzono na magazyn {nazwa} w ilosci: {ilosc} | uzytkownik: {user}'.format(nazwa = nazwa, ilosc = ilosc, user = self.user))
            

            title = "wprowadź na magazyn"
            self.create_inf_mess(text,title,12)    
   
        else:
            text = "w polu ilość do pobrania wpisz wartosc numeryczną"
            title = "błąd numeryczny"
            self.create_war_mess(text,title,10)


    def check_if_ok(self,stan1,stan2,il,Nazwa):
        stan = [0,0,0,0,0,0]
        tekst = ['','','','','','']

        if Nazwa in self.data.returnlist('Nazwa'):
            text = 'przedmiot o podanej nazwie już istnieje'
            title = 'błąd nazwy'
            self.create_war_mess(text,title,10)
            return False
        
        elif(Nazwa == ''):
            text = 'podaj nazwę przedmiotu'
            title = 'błąd nazwy'
            self.create_war_mess(text,title,10)
            return False
        
        if stan1.isnumeric() and stan2.isnumeric():
            if int(stan1) >= int(stan2):
                text = 'stan maksymalny nie może być mniejszy od stanu minimalnego'
                title = 'bład stanu maksymalnego'
                self.create_war_mess(text,title,10)
                return False
        
        if stan1.isnumeric() == False:
            tekst[0] = 'w oknie stan minimalny podaj liczbe'
            stan[0]= 1
        elif (int(stan1) <=0):
            tekst[3] =  'wprowadzana liczba produku musi być wieksza od 0'
            stan[3] = 1

        if stan2.isnumeric() == False:
            tekst[1] = 'w oknie stan maksymalny podaj liczbe'
            stan[1] = 1

        elif (int(stan2) <= 0):
            tekst[4] =  'wprowadzony stan minimalny musi być wieksza od 0'
            stan[4] = 1

        if il.isnumeric() == False:
            tekst[2] =  'w oknie ilość podaj liczbe'
            stan[2] = 1
          
        elif (int(il) <=0):
            tekst[5] =  'wprowadzony stan maksymalny musi być wieksza od 0'
            stan[5] = 1

        text =''
        for i in range(len(stan)):
            if stan[i] == 1:
                text += tekst[i] +'\n'
            
        if any(stan) != 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.NoIcon)
            font = QFont()
            font.setPointSize(12)
            msg.setFont(font)
            msg.setText(text)
            msg.setWindowTitle('błąd')
            msg.exec_()

        else: return True


    def accept(self):
        Nazwa = self.ui.lineEdit_8.text()
        Magazyn = self.ui.comboBox_m.currentText()
        regał = self.ui.comboBox_entity.currentText()
        ilość = self.ui.lineEdit_4.text()
        typ_czesci = self.ui.comboBox.currentText()
        stan_min = self.ui.lineEdit_5.text()
        stan_max = self.ui.lineEdit_3.text()
        nr_prod = self.ui.lineEdit_9.text()
        
        if self.check_if_ok(stan_min,stan_max,ilość,Nazwa) == True:
            self.data5.AddItem(Nazwa,ilość,stan_min,stan_max,typ_czesci,Magazyn,regał,nr_prod)
            self.data.beginInsertRows(QModelIndex(), 0, 0)
            self.data.AddItem2(Nazwa,ilość,Magazyn,regał)
            self.data3.AddItem4(nr_prod)
            self.data2.AddItem3(Nazwa)
            self.data.endInsertRows()
            self.ui.lineEdit_2.setDisabled(False)
            self.data5.save()  
            self.create_log_mes('Dodano: {Nazwa} w ilosci: {ilosc} ,magazyn: {magazyn} ,regal: {regal}, stan_min: {stan_min}, stan_max: {stan_min} ,nr_prod: {nr_prod}  | uzytkownik: {user}'.format(Nazwa = Nazwa, ilosc = ilość ,magazyn = Magazyn, regal = regał,stan_min = stan_min ,stan_max = stan_max,nr_prod = nr_prod, user =self.user))    
            text = 'Pomyślnie dodano: ' + Nazwa + ' w ilośći: ' + ilość + '\n' +'lokalizacja:' + ' \nMagazyn: ' + Magazyn + ', regał: ' + regał +'\n' + 'Stan minimalny: ' +stan_min +' Stan maksymalny: '+ stan_max 
            self.create_inf_mess(text,'wprowadź na magazyn', 12)
            self.ui.lineEdit_2.setText('')
            self.ui.stackedWidget.setCurrentWidget(self.ui.page)
        else:
            pass
    

    def create_inf_mess(self,text,title,font2):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        font = QFont()
        font.setPointSize(font2)
        msg.setFont(font)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()


    def create_war_mess(self,text,title,font2):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        font = QFont()
        font.setPointSize(font2)
        msg.setFont(font)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.exec_()

    ##################################
    # clear the data and swtich to second page with form
    def form_page(self):

        self.ui.tableView.clearSelection()
        self.ui.lineEdit_2.setDisabled(True)
        self.ui.lineEdit.setText('')
        self.ui.lineEdit_2.setText('')
        self.ui.lineEdit_3.setText('')
        self.ui.lineEdit_4.setText('')
        self.ui.lineEdit_5.setText('')
        self.ui.comboBox_m.setCurrentIndex(0)
        self.ui.comboBox_entity.setCurrentIndex(0)
        self.ui.lineEdit_8.setText('')
        self.ui.lineEdit_9.setText('')
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
        

    def hisory_page(self):
        self.ui.tableView.clearSelection()
        self.ui.stackedWidget.setCurrentWidget(self.ui.page3)


    ########################################
    # for the text line 1
    def filter(self, filter_text):

        for i in range(self.data2.rowCount()):
            for j in range(self.data2.columnCount()):
                item = self.data2.getItem(i,j)
                match = filter_text.lower() not in item.lower()
                self.ui.tableView.setRowHidden(i, match)
                if not match:
                    break     
                
                  
    ########################################
    # for the text line 2
    def filter2(self, filter_text):

        for i in range(self.data3.rowCount()):
            for j in range(self.data3.columnCount()):
                item = self.data3.getItem(i,j)
                match = filter_text.lower() != item.lower()
                self.ui.tableView.setRowHidden(i, match)
                if filter_text == '':
                    self.update_list()
                if not match:
                    break  


    def filter_for_log(self,text):
        for i in range(self.data_disp_log.rowCount()):  
                item = self.data_disp_log.get_item(i)
                item = item.split('|')
                item2 = item[0]
                item2 = item2.split(';')
                item2 = item2[0]
                item = item[1].split(':')
                item = item[1].replace(" ", "")
                match = (str(text).lower() not in str(item2).lower()) and (str(text).lower() not in str(item).lower())
                self.ui.tableView2.setRowHidden(i, match)

                

    def on_enter_pressed(self):
        try:
            if (str(self.ui.lineEdit_2.text()) not in self.data3.returnlist('Nr części')) or (str(self.ui.lineEdit_2.text()) not in self.data3.returnlist('Nr części producenta')):
                self.ui.lineEdit_2.setDisabled(True)
                if self.is_table_empty() == True:    
                    self.open_dialog_search()
                
            else:
                pass
        except: invalidFormat


    def is_table_empty(self):
        proxy_model = self.ui.tableView.model()
        if proxy_model is not None:
            visible_rows = 0
            for row in range(proxy_model.rowCount()):
                if not self.ui.tableView.isRowHidden(row):
                    visible_rows += 1
            return visible_rows == 0
        return True


    def open_dialog_4(self):
        dialog4 = dialog4_func(self)
        dialog4.ui.label.setText('podaj ilość do pobrania')
        Naz ,stan ,mag , reg = self.data5.getDatabyRow(self.sel_row)
        text = 'Wybrałeś: ' + '\n' + str(Naz) + '\nStan magazynowy: ' + str(stan) + '\n' +'lokalizacja: \n' + 'Magazyn: ' +str(mag) +'  Regał: ' + str(reg)
        dialog4.ui.buttonBox.accepted.connect(lambda: self.save_changes(dialog4.ui.comboBox.currentText(), stan,Naz))
        dialog4.ui.label_2.setText(text)
        dialog4.exec_()


    def open_dialog_4_wyprowadz(self):
        dialog4 = dialog4_func(self)
        dialog4.ui.label.setText('podaj ilość do wprowadzenia')
        Naz ,stan ,mag , reg = self.data5.getDatabyRow(self.sel_row)
        text = 'Wybrałeś: ' + '\n' + str(Naz) + '\nStan magazynowy: ' + str(stan) + '\n' +'lokalizacja: \n' + 'Magazyn: ' +str(mag) +'  Regał: ' + str(reg)
        dialog4.ui.buttonBox.accepted.connect(lambda: self.save_changes2(dialog4.ui.comboBox.currentText(),Naz))
        dialog4.ui.label_2.setText(text)
        dialog4.exec_()


    def open_dialog_search(self):
        Dialog3 = dialog3_func(self)
        Dialog3.ui.buttonBox.rejected.connect(self.go_back)
        Dialog3.ui.buttonBox.accepted.connect(lambda: self.on_dialog_search_accepted(Dialog3))
        Dialog3.close_button.connect(self.go_back)
        Dialog3.escapePressed.connect(self.go_back)
        Dialog3.exec_()


    def on_dialog_search_accepted(self, dialog):
        text = self.ui.lineEdit_2.text()
        self.ui.lineEdit_9.setText(text)
        self.ui.lineEdit.setText('')
        self.ui.lineEdit_2.setText('')
        self.ui.lineEdit_3.setText('')
        self.ui.lineEdit_4.setText('')
        self.ui.lineEdit_5.setText('')
        self.ui.comboBox_m.setCurrentIndex(0)
        self.ui.comboBox_entity.setCurrentIndex(0)
        self.ui.lineEdit_8.setText('')
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)

    ########################################
    #expand menu
    def slideLeftMenu(self):
        # Get current left menu width
        width = self.ui.side_menu_container.width()
        # If minimized
        if width == 0:
            # Expand menu
            newWidth = 160
            self.ui.open_close_side_bar_btn.setIcon(QtGui.QIcon(u":/icons/icons/chevron-left.svg"))
        # If maximized
        else:
            # Restore menu
            newWidth = 0
            self.ui.open_close_side_bar_btn.setIcon(QtGui.QIcon(u":/icons/icons/align-left.svg"))

        # Animate the transition
        self.animation = QPropertyAnimation(self.ui.side_menu_container, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()


    #############################################
    # fucntion to go back button 
    def go_back(self):
        
        #print(os.path.getsize('logs.log'))
        self.ui.tableView.clearFocus()
        self.ui.lineEdit_2.setDisabled(False)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)
        self.ui.lineEdit.setText('')
        self.ui.lineEdit_2.setText('')
        self.update_list()


    ## iterate through data in table and unhide it 
    def update_list(self):
        for i in range(self.data.rowCount()):
            self.ui.tableView.setRowHidden(i, False)
    

    def switch_window(self,user,info):
        self.loginn.hide()
        self.user = user
        if info == '1':
            self.show()
            self.ui.lineEdit.setText('')
            self.ui.lineEdit_2.setText('')
            self.ui.pushButton_8.show()
            self.ui.pushButton_3.show()
            self.ui.historia.show()
            self.ui.dodaj.hide()
            self.ui.usun.hide()

        elif info == '2':
            self.show()
            self.ui.lineEdit.setText('')
            self.ui.lineEdit_2.setText('')
            self.ui.pushButton_3.show()
            self.ui.pushButton_8.show()
            self.ui.historia.show()
            self.ui.dodaj.show()
            self.ui.usun.show()
        else:
            self.show()
            self.ui.pushButton_3.hide()
            self.ui.pushButton_8.hide()
            self.ui.lineEdit.setText('')
            self.ui.lineEdit_2.setText('')
            self.ui.historia.hide()
            self.ui.dodaj.hide()
            self.ui.usun.hide()

    def log_out(self):
        self.hide()
        self.loginn.show()
        self.loginn.ui.lineEdit.setText('')
        self.loginn.ui.lineEdit_2.setText('')
        self.loginn.ui.lineEdit.setFocus()
        self.edit_mode = False
        self.update_edit_mode()
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.slideLeftMenu()


    
if __name__== "__main__":
    
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
    
    
#################
# wylogowujac sie ma wyjsc z trybu edycji 
