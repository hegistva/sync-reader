
import pathlib
import os
import json

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

SETTINGS = {}
APP_FOLDER = os.path.join(pathlib.Path.home(), 'booktranslate')
if not os.path.exists(APP_FOLDER):
    os.makedirs(APP_FOLDER)    
SETTINGS_FILE = os.path.join(pathlib.Path.home(), 'booktranslate', 'settings.json')
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, 'r') as f:
        SETTINGS.update(json.load(f))

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        minWidth = parent.width() * 0.8 if not parent is None else 600
        self.setMinimumWidth(minWidth)
        layout = QtWidgets.QVBoxLayout(self)

        grid = QtWidgets.QGridLayout()
        layout.addLayout(grid)
        
        book_location = SETTINGS.get('book_location', os.path.join(APP_FOLDER, 'books'))
        self.book_location = QtWidgets.QLineEdit(book_location)
        grid.addWidget(QtWidgets.QLabel("Book Location"), 0, 0)
        grid.addWidget(self.book_location, 0, 1)
        grid.addWidget(QtWidgets.QPushButton("..."), 0, 2)
        self.setWindowTitle('Application Settings')
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
def showSettings(parent):
    dialog = SettingsDialog(parent)
    result = dialog.exec_()
    if result == QtWidgets.QDialog.Accepted:
        SETTINGS.update({'book_location': dialog.book_location.text()})
        with open(SETTINGS_FILE, 'w') as f:
            f.write(json.dumps(SETTINGS))        



            
