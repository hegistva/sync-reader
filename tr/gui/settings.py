
import pathlib
import os
import json

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

BOOK_LOCATION = 'book_location'
AUTO_SCROLL = 'auto_scroll'
SKIP_INTRO = 'skip_intro'
AUTO_PLAY = 'auto_play'

LIBRARY = 'lib'
CONTENT = 'content'

SETTINGS = {}
# default settings
SETTINGS[AUTO_PLAY] = True
SETTINGS[AUTO_SCROLL] = True
SETTINGS[SKIP_INTRO] = True

APP_FOLDER = os.path.join(pathlib.Path.home(), 'booktranslate')
os.makedirs(APP_FOLDER, exist_ok=True)    
SETTINGS_FILE = os.path.join(pathlib.Path.home(), 'booktranslate', 'settings.json')
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, 'r') as f:
        SETTINGS.update(json.load(f))

class Config:
    APP_FOLDER, BOOK_LOCATION, LIBRARY, CONTENT, AUTO_SCROLL, SKIP_INTRO, AUTO_PLAY = range(7)
    @classmethod
    def value(cls, s):
        if s == cls.APP_FOLDER:
            return APP_FOLDER
        elif s == cls.BOOK_LOCATION:
            return SETTINGS[BOOK_LOCATION]
        elif s == cls.AUTO_SCROLL:
            return SETTINGS[AUTO_SCROLL]
        elif s == cls.AUTO_PLAY:
            return SETTINGS[AUTO_PLAY]
        elif s == cls.SKIP_INTRO:
            return SETTINGS[SKIP_INTRO]
        elif s == cls.LIBRARY:
            return os.path.join(SETTINGS[BOOK_LOCATION], LIBRARY)
        elif s == cls.CONTENT:
            return os.path.join(SETTINGS[BOOK_LOCATION], CONTENT)
        else:
            raise RuntimeError('Unkonw GUI setting')
        
class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        minWidth = parent.width() * 0.6 if not parent is None else 600
        self.setMinimumWidth(minWidth)
        layout = QtWidgets.QVBoxLayout(self)

        grid = QtWidgets.QGridLayout()
        layout.addLayout(grid)
        
        book_location = SETTINGS.get(BOOK_LOCATION, os.path.join(APP_FOLDER, 'books'))        
        os.makedirs(book_location, exist_ok=True)

        self.book_location = QtWidgets.QLineEdit(book_location)
        grid.addWidget(QtWidgets.QLabel("Book Location"), 0, 0)
        grid.addWidget(self.book_location, 0, 1)        
        self.selectorButton = QtWidgets.QPushButton("...")
        self.selectorButton.clicked.connect(self.selectPath)
        grid.addWidget(self.selectorButton, 0, 2)
        # skip intro
        grid.addWidget(QtWidgets.QLabel("Skip Chapter Introduction"), 1, 0)
        self.skipIntro = QtWidgets.QCheckBox()
        self.skipIntro.setChecked(SETTINGS.get(SKIP_INTRO, True))
        grid.addWidget(self.skipIntro, 1, 2)
        # auto-scroll
        grid.addWidget(QtWidgets.QLabel("Auto-scroll"), 2, 0)
        self.autoScroll = QtWidgets.QCheckBox()
        self.autoScroll.setChecked(SETTINGS.get(AUTO_SCROLL, True))
        grid.addWidget(self.autoScroll, 2, 2)
        # auto-play
        grid.addWidget(QtWidgets.QLabel("Auto-play"), 3, 0)
        self.autoPlay = QtWidgets.QCheckBox()
        self.autoPlay.setChecked(SETTINGS.get(AUTO_PLAY, True))
        grid.addWidget(self.autoPlay, 3, 2)

        self.setWindowTitle('Application Settings')
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def selectPath(self):
        options = QtWidgets.QFileDialog.DontResolveSymlinks | QtWidgets.QFileDialog.ShowDirsOnly
        file = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Book Location", self.book_location.text(), options=options)
        if file:
            self.book_location.setText(file)
        
def showSettings(parent):
    dialog = SettingsDialog(parent)
    result = dialog.exec_()
    if result == QtWidgets.QDialog.Accepted:
        SETTINGS.update({BOOK_LOCATION: dialog.book_location.text()})
        
        skip_intro = dialog.skipIntro.isChecked()
        SETTINGS.update({SKIP_INTRO: skip_intro})
        # TODO: use events
        parent.ui.player.skipIntro = skip_intro

        auto_scroll = dialog.autoScroll.isChecked()
        SETTINGS.update({AUTO_SCROLL: auto_scroll})
        # TODO: use events
        parent.ui.readerWidget.autoScroll = auto_scroll

        auto_play = dialog.autoPlay.isChecked()
        SETTINGS.update({AUTO_PLAY: auto_play})
        # TODO: use events
        parent.autoPlay = auto_play

        with open(SETTINGS_FILE, 'w') as f:
            f.write(json.dumps(SETTINGS))



            
