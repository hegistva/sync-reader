# module to manage the book navigator tree

from PyQt5 import QtWidgets, Qt, QtGui

TREE_VIEW = None
MODEL = QtGui.QStandardItemModel()
MODEL.setHorizontalHeaderLabels(['Book/Chapter', 'Status'])

# initalize a tree 
def init(treeView):
    global TREE_VIEW, MODEL
    TREE_VIEW = treeView

    TREE_VIEW.setSelectionBehavior(Qt.QAbstractItemView.SelectItems)
    TREE_VIEW.setModel(MODEL)
    TREE_VIEW.setUniformRowHeights(True)

    book = QtGui.QStandardItem('20000LeaguesUnderTheSea')
    lang_eng = QtGui.QStandardItem('eng')
    lang_fra = QtGui.QStandardItem('fra')
    book.appendRows([lang_eng, lang_fra])

    MODEL.appendRow(book)
