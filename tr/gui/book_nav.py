# module to manage the book navigator tree

import os
import glob
import json
from PyQt5 import QtWidgets, Qt, QtGui
from reader_rc import ICONS
from settings import Config
from tr.books import book_manager
from tr.books import books
from tr.libs.trans.utils import Lang
import model

TREE_VIEW = None
MAIN_WINDOW = None
MODEL = QtGui.QStandardItemModel()

CHAPTER_CAPTION = {
    Lang.ENG: 'Chapter',
    Lang.FRA: 'Chapitre'
}

dl_icon = QtGui.QIcon(os.path.join(ICONS, 'download.svg'))
book_icon = QtGui.QIcon(os.path.join(ICONS, 'book.svg'))
lang_icon = QtGui.QIcon(os.path.join(ICONS, 'language.svg'))
track_icon = QtGui.QIcon(os.path.join(ICONS, 'track.svg'))
play_icon = QtGui.QIcon(os.path.join(ICONS, 'play.svg'))

# initalize a tree 
def initNavigator(treeView, parent):
    # initialize tree view
    global TREE_VIEW, MAIN_WINDOW
    TREE_VIEW = treeView
    MAIN_WINDOW = parent
    TREE_VIEW.setSelectionBehavior(Qt.QAbstractItemView.SelectItems)
    TREE_VIEW.setSelectionMode(Qt.QAbstractItemView.SingleSelection)
    TREE_VIEW.setEditTriggers(Qt.QAbstractItemView.NoEditTriggers)
    TREE_VIEW.setModel(MODEL)
    TREE_VIEW.setUniformRowHeights(True)
    TREE_VIEW.clicked.connect(clicked)
    # refresh contents
    refresh()


def refresh():
    
    lpath = Config.value(Config.LIBRARY) # book location

    MODEL.clear()
    MODEL.setHorizontalHeaderLabels(['Book/Chapter', ''])

    bookfiles = glob.glob(lpath+"/*.json")
    for bookf in bookfiles:
        bi = model.BookInfo.fromJsonFile(bookf)
        book_node = QtGui.QStandardItem(book_icon, bi.bookid)
        book_node.setData(bi)
        MODEL.appendRow(book_node)

        for tr in bi.translations:
            # Create Language Node
            lang_node = QtGui.QStandardItem(lang_icon, tr.language)
            lang_node.setData(tr)
            book_node.appendRow(lang_node)
            for chapter in tr.chapters:
                # Create Chapter Node
                chnum = chapter.idx
                chapter_title = CHAPTER_CAPTION[tr.language] + ' %04d' % chnum
                chapter_node = QtGui.QStandardItem(track_icon, chapter_title)                
                chapter_node.setData(chapter)
                lang_node.appendRow(chapter_node)
    # adjust column sizes on the tree view
    TREE_VIEW.resizeColumnToContents(0)
    TREE_VIEW.resizeColumnToContents(1)

def clicked(idx):
    itm = TREE_VIEW.model().itemFromIndex(idx)
    m = itm.data()
    if m:
        print("chapter clicked: %s" % m)

