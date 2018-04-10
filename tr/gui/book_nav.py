# module to manage the book navigator tree

import os
from PyQt5 import QtWidgets, Qt, QtGui
from reader_rc import ICONS

TREE_VIEW = None
MODEL = QtGui.QStandardItemModel()
MODEL.setHorizontalHeaderLabels(['Book/Chapter', ''])

class Chapter(object):
    def __init__(self, book, language, chapter):
        self.book = book
        self.language = language
        self.chapter = chapter

    def __str__(self):
        return "Book: %s, Language: %s, Chapter: %s"  % (self.book, self.language, self.chapter)

# initalize a tree 
def initNavigator(treeView, parent):
    global TREE_VIEW, MODEL
    TREE_VIEW = treeView

    TREE_VIEW.setSelectionBehavior(Qt.QAbstractItemView.SelectItems)
    TREE_VIEW.setSelectionMode(Qt.QAbstractItemView.SingleSelection)
    TREE_VIEW.setEditTriggers(Qt.QAbstractItemView.NoEditTriggers)
    TREE_VIEW.setModel(MODEL)
    TREE_VIEW.setUniformRowHeights(True)

    dl_icon = QtGui.QIcon(os.path.join(ICONS, 'download.svg'))
    book_icon = QtGui.QIcon(os.path.join(ICONS, 'book.svg'))
    lang_icon = QtGui.QIcon(os.path.join(ICONS, 'language.svg'))
    track_icon = QtGui.QIcon(os.path.join(ICONS, 'track.svg'))
    play_icon = QtGui.QIcon(os.path.join(ICONS, 'play.svg'))

    book = '20000LeaguesUnderTheSea'
    book_itm = QtGui.QStandardItem(book_icon, book)
    MODEL.appendRow(book_itm)

    lang_eng = QtGui.QStandardItem(lang_icon, 'eng')
    lang_fra = QtGui.QStandardItem(lang_icon, 'fra')
    book_itm.appendRows([lang_eng, lang_fra])

    for i in range(21):
        chapter = i + 1
        chapter_title = 'Chapter %04d' % chapter
        chapter_eng = QtGui.QStandardItem(track_icon, chapter_title)
        button_eng = QtGui.QStandardItem()                
        lang_eng.appendRow([chapter_eng, button_eng])
        button = QtWidgets.QPushButton()
        button.setIcon(dl_icon)
        button.clicked.connect(parent.download)
        ch = Chapter(book, 'eng', chapter)
        button.setProperty('chapter', ch)        
        chapter_eng.setData(ch)
        # button.setStyleSheet("background-color: orange")
        TREE_VIEW.setIndexWidget(button_eng.index(), button)
        chapter_title = 'Chapitre %04d' % chapter
        chapter_fra = QtGui.QStandardItem(track_icon, chapter_title)
        button_fra = QtGui.QStandardItem()
        lang_fra.appendRow([chapter_fra, button_fra])
        button = QtWidgets.QPushButton()
        button.setIcon(play_icon)
        ch = Chapter(book, 'fra', chapter)
        button.setProperty('chapter', ch)
        chapter_fra.setData(ch)
        # button.setStyleSheet("background-color: green")
        button.clicked.connect(parent.play)
        TREE_VIEW.setIndexWidget(button_fra.index(), button)
    
    TREE_VIEW.resizeColumnToContents(0)
    TREE_VIEW.resizeColumnToContents(1)

    TREE_VIEW.clicked.connect(clicked)

def clicked(idx):
    ch = TREE_VIEW.model().itemFromIndex(idx).data()
    if ch:
        print("chapter clicked: %s" % ch)

