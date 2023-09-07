from dodaj import *
from PyQt5.QtCore import Qt

class dodaj(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.installEventFilter(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)