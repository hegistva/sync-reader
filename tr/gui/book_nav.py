# module to manage the book navigator tree

import os
import glob
import json
from PyQt5 import QtWidgets, Qt, QtGui
from settings import Config
from tr.books import book_manager
from tr.books import books

import model
import res

TREE_VIEW = None
MAIN_WINDOW = None
MODEL = QtGui.QStandardItemModel()
SEL_MODEL = None

# initalize a tree 
def initNavigator(treeView, parent):
    # initialize tree view
    global TREE_VIEW, MAIN_WINDOW, SEL_MODEL
    TREE_VIEW = treeView
    MAIN_WINDOW = parent
    TREE_VIEW.setSelectionBehavior(Qt.QAbstractItemView.SelectItems)
    TREE_VIEW.setSelectionMode(Qt.QAbstractItemView.SingleSelection)
    TREE_VIEW.setEditTriggers(Qt.QAbstractItemView.NoEditTriggers)
    TREE_VIEW.setModel(MODEL)    
    TREE_VIEW.setUniformRowHeights(True)
    SEL_MODEL = TREE_VIEW.selectionModel()
    SEL_MODEL.selectionChanged.connect(MAIN_WINDOW.selectionChanged)
    # refresh contents
    refresh()

def refresh():
    
    lpath = Config.value(Config.LIBRARY) # book location

    MODEL.clear()
    MODEL.setHorizontalHeaderLabels(['Book/Language/Chapter', ''])

    bookfiles = glob.glob(lpath+"/*.json")
    for bookf in bookfiles:
        bi = model.BookInfo.fromJsonFile(bookf)
        book_node = QtGui.QStandardItem(res.book_icon, bi.bookid)
        book_node.setData(bi)
        MODEL.appendRow(book_node)

        for tr in bi.translations:
            # Create Language Node
            lang_node = QtGui.QStandardItem(res.lang_icon, tr.language)
            lang_node.setData(tr)
            book_node.appendRow(lang_node)
            for chapter in tr.chapters:
                # Create Chapter Node
                chnum = chapter.idx
                chapter_title = model.CHAPTER_CAPTION[tr.language] + ' %04d' % chnum
                ch_icon = res.play_icon if chapter.downloaded else res.dl_icon
                chapter_node = QtGui.QStandardItem(ch_icon, chapter_title) 
                chapter.treeNode = chapter_node
                chapter_node.setData(chapter)
                lang_node.appendRow(chapter_node)
    # adjust column sizes on the tree view
    TREE_VIEW.resizeColumnToContents(0)
    TREE_VIEW.resizeColumnToContents(1)

