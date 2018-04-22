# module to manage the book navigator tree

import os
import glob
import json
from PyQt5 import QtWidgets, Qt, QtGui
from reader_rc import ICONS
from settings import Config
from tr.books import book_manager
from tr.books import books

import model

TREE_VIEW = None
MAIN_WINDOW = None
MODEL = QtGui.QStandardItemModel()

dl_icon = QtGui.QIcon(os.path.join(ICONS, 'download.svg'))
book_icon = QtGui.QIcon(os.path.join(ICONS, 'book.svg'))
lang_icon = QtGui.QIcon(os.path.join(ICONS, 'language.svg'))
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
    TREE_VIEW.clicked.connect(lambda idx: MAIN_WINDOW.select(idx))
    # refresh contents
    refresh()

def refresh():
    
    lpath = Config.value(Config.LIBRARY) # book location

    MODEL.clear()
    MODEL.setHorizontalHeaderLabels(['Book/Language/Chapter', ''])

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
                chapter_title = model.CHAPTER_CAPTION[tr.language] + ' %04d' % chnum
                ch_icon = play_icon if chapter.downloaded else dl_icon
                chapter_node = QtGui.QStandardItem(ch_icon, chapter_title)               
                chapter_node.setData(chapter)
                lang_node.appendRow(chapter_node)
    # adjust column sizes on the tree view
    TREE_VIEW.resizeColumnToContents(0)
    TREE_VIEW.resizeColumnToContents(1)

