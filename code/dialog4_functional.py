from PyQt5.QtCore import Qt
from dialog4 import *


class dialog4_func(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog4()
        self.ui.setupUi(self)
        self.installEventFilter(self)
        

