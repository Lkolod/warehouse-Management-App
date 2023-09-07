
import logging
from PyQt5.QtCore import Qt, QModelIndex, QAbstractTableModel,pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget

class log_model(QAbstractTableModel):

    data_changed = pyqtSignal()

    def __init__(self, log_file, max_entries):
        super().__init__()
        self.log_file = log_file
        self.max_entries = max_entries
        self.log_lines = self.get_log_lines()

    def rowCount(self, parent=QModelIndex()):
        return len(self.log_lines)

    def columnCount(self, parent=QModelIndex()):
        return 1  # Displaying only one column for log entries

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self.log_lines[index.row()].strip()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return "historia zmian"

    def get_log_lines(self):
        try:
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
            return lines[-self.max_entries:]
        except FileNotFoundError:
            return []
    
    def get_item(self, row):
        log_entry = self.log_lines[row].strip() if 0 <= row < len(self.log_lines) else ""
        return log_entry
    
    def refresh_data(self):
        self.log_lines = self.get_log_lines()
        self.data_changed.emit()  # Emit signal to refresh the view