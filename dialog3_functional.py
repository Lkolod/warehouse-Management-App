from PyQt5.QtCore import Qt
from dialog3 import *


class dialog3_func(QtWidgets.QDialog):


    
    escapePressed = QtCore.pyqtSignal()
    close_button = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog3()
        self.ui.setupUi(self)
        self.installEventFilter(self)
        

    def eventFilter(self, source, event):
        if source == self and event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Escape:
            self.escapePressed.emit()
            self.accept()
            return True  # Event handled, do not propagate further
        return super().eventFilter(source, event)

    def closeEvent(self, event):
        # Call the "go back" function when the dialog is about to close
        self.escapePressed.emit()
     