
import os
from PyQt5 import QtGui

ROOT = os.path.dirname(os.path.realpath(__file__))
ICONS = os.path.join(ROOT, 'icons')

dl_icon = QtGui.QIcon(os.path.join(ICONS, 'download.svg'))
book_icon = QtGui.QIcon(os.path.join(ICONS, 'book.svg'))
lang_icon = QtGui.QIcon(os.path.join(ICONS, 'language.svg'))
play_icon = QtGui.QIcon(os.path.join(ICONS, 'play.svg'))
