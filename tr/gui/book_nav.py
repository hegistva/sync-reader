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
        book = json.load(open(bookf, 'r'))
        # Create Book Node
        book_id = book[book_manager.ID]
        book_node = QtGui.QStandardItem(book_icon, book_id)
        book_model = model.BookInfo(book_id)
        book_node.setData(book_model)
        MODEL.appendRow(book_node)

        for lang, tr in book[books.TRANSLATIONS].items():
            # Create Language Node
            lang_node = QtGui.QStandardItem(lang_icon, lang)
            tr_url = tr[books.URL]
            tr_title = tr[books.TITLE]
            tr_model = model.TranslationInfo(book_id, lang, tr_title, tr_url)
            book_model.addTranslation(tr_model)
            lang_node.setData(tr_model)
            book_node.appendRow(lang_node)
            for idx, chapter in enumerate(tr[books.CHAPTERS]):
                # Create Chapter Node
                chnum = chapter[books.IDX]
                chapter_title = CHAPTER_CAPTION[lang] + ' %04d' % chnum
                chapter_node = QtGui.QStandardItem(track_icon, chapter_title)
                chapter_model = model.ChapterInfo(chapter)
                tr_model.addChapter(chapter_model)
                chapter_node.setData(chapter_model)
                lang_node.appendRow(chapter_node)
                # btn_node = QtGui.QStandardItem()
                # lang_node.appendRow([chapter_node, btn_node])
                # btn = QtWidgets.QPushButton()
                # btn.setIcon(dl_icon)
                # btn.clicked.connect(MAIN_WINDOW.download)
                # btn.setProperty('model', chapter_model)                
                # TREE_VIEW.setIndexWidget(btn_node.index(), btn)
    # adjust column sizes on the tree view        
    TREE_VIEW.resizeColumnToContents(0)
    TREE_VIEW.resizeColumnToContents(1)

def clicked(idx):
    itm = TREE_VIEW.model().itemFromIndex(idx)
    m = itm.data()
    if m:
        print("chapter clicked: %s" % m)

