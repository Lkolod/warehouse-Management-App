import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt,pyqtSignal
from PyQt5.QtGui import QColor, QBrush

df = pd.read_excel('Zeszyt1.xlsx',index_col=None)
df.reset_index(drop=True, inplace=True)

df2 = df[['Nazwa','Nr części','Stan magazynowy','magazyn','regał']]
df3 = df[['Nazwa']]
df4 = df[['Nr części','Nr części producenta']]




class pandasModel(QAbstractTableModel):
    wrongDataEntered = pyqtSignal()
    dataChanged2 = pyqtSignal(str,int,int,str)

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        super().__init__()
        self._data = data
        self.old_val = ''


    def rowCount(self, parent=None):
        return self._data.shape[0]


    def columnCount(self, parnet=None):
        return self._data.shape[1]


    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                return str(self._data.iloc[index.row(), index.column()])
             
            elif role == Qt.BackgroundRole and index.column() == 2 and int(self._data.iloc[index.row(), index.column()]) < int(df.loc[index.row()]['Stan min']):
                color = QColor(255, 0, 0)  # Change color to your desired color
                return QBrush(color)
            
        return None 


    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


    def getItem(self,row,col):
        return str(self._data.iat[row,col])


    def setData(self, index, value, role):
        if role == Qt.EditRole:
            if value != '':

                if (index.column() == 0 and value in self._data['Nazwa'].tolist()):
                    if value == self._data.iloc[index.row(), index.column()]:
                        pass
                    else:
                        self.wrongDataEntered.emit() 
                        return False
                
                elif (index.column() == 1 and value.isnumeric() == False):
                    self.wrongDataEntered.emit() 
                    return False


                elif (index.column() == 2 and value.isnumeric() == False):
                    self.wrongDataEntered.emit() 
                    return False
                    
                elif (index.column() == 5 and value.isnumeric() == False) or (index.column() == 5  and int(value) >= int(self._data.iloc[index.row(), index.column() +1])):
                    self.wrongDataEntered.emit() 

                elif (index.column() == 6 and value.isnumeric() == False) or (index.column() == 6  and int(value) <= int(self._data.iloc[index.row(), index.column() -1])):
                    self.wrongDataEntered.emit() 

                else:
                    self.old_val = self._data.iloc[index.row(), index.column()]
                    self._data.iloc[index.row(), index.column()] = value
                    self.dataChanged.emit(index, index)
                    self.dataChanged2.emit(str(self.old_val), index.row(), index.column(),str(value))

            else:
                self.wrongDataEntered.emit() 
            
                  
            return True
        return False


    def flags(self, index):
        
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

        
    # for inserting the data with all columns
    def AddItem(self,nazwa,ilosc,stan_min,stan_max,Typ_części,magazyn,regał,nr_producenta):
        nr_czesci = self.maxi() +1 
        new_row = {'Nazwa':nazwa,'Nr części':nr_czesci ,'Stan magazynowy':ilosc,'Stan min':stan_min,'Stan maks':stan_max, 'Typ części':Typ_części, 'magazyn':magazyn,'regał':regał,'cena':1,'Nr części producenta':nr_producenta}
        self._data = pd.concat([self._data, pd.DataFrame([new_row])],ignore_index=True)
        

    # for insering data which purpose is only for display
    def AddItem2(self,nazwa,ilosc,magazyn,regał):

        nr_czesci = self.maxi() +1 
        new_row = {'Nazwa':nazwa,'Nr części':nr_czesci ,'Stan magazynowy':ilosc, 'magazyn':magazyn,'regał':regał}
        self._data = pd.concat([self._data, pd.DataFrame([new_row])],ignore_index=True)
        

    # for insering the data for filtering by name 
    def AddItem3(self,nazwa):
        new_row = {'Nazwa':nazwa}
        self._data = pd.concat([self._data, pd.DataFrame([new_row])],ignore_index=True)

    # for insering data for filtering by nr

    def AddItem4(self,nr_prod):
        nr_czesci = self.maxi() +1
        new_row = {'Nr części':nr_czesci,'Nr części producenta':nr_prod}
        self._data = pd.concat([self._data, pd.DataFrame([new_row])],ignore_index=True)


    def maxi(self):
        maxi = 0
        for i in self._data['Nr części'].tolist():
            i = str(i)
            if i.isnumeric():
                if int(i) > maxi:
                    maxi = int(i)
        return maxi
        

    def printdata(self):
        print(self._data)
    

    def returnlist(self,nazwa_col):
        return self._data[nazwa_col].tolist()
    

    def save(self):
        self._data.to_excel('Zeszyt1.xlsx', index=False)

    def getDatabyRow(self,row):
        Nazwa =  self._data.iloc[row]['Nazwa']
        stan = self._data.iloc[row]['Stan magazynowy']
        Magazyn =  self._data.iloc[row]['magazyn']
        Regał =  self._data.iloc[row]['regał']
        return Nazwa,stan,Magazyn,Regał
    

    def change_qty(self,row,ilosc):
        self._data['Stan magazynowy'][row] = int(self._data['Stan magazynowy'][row]) + int(ilosc)


    def get_col_name(self,col):
        column_name = self._data.columns[col]
        return column_name


    def updateModel(self, new_data):
        self._data = new_data
        self.layoutChanged.emit() 

    

